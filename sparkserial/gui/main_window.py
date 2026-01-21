import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QGroupBox, QLabel, QComboBox, 
                             QPushButton, QPlainTextEdit, QLineEdit, QStatusBar,
                             QCheckBox, QSplitter, QListWidget, QListWidgetItem,
                             QDialog, QFormLayout, QDialogButtonBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QIcon, QTextCursor
import serial
from sparkserial.core.serial_manager import SerialManager
from sparkserial.core.command_manager import CommandManager
from sparkserial.gui.styles import get_stylesheet
import os
import json

class CommandDialog(QDialog):
    def __init__(self, parent=None, command_info=None):
        super().__init__(parent)
        self.setWindowTitle("Add Command" if not command_info else "Edit Command")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Get Version")
        if command_info:
            self.name_input.setText(command_info.get('name', ''))
            
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("e.g., AT+VER")
        if command_info:
            self.command_input.setText(command_info.get('command', ''))
            
        self.hex_check = QCheckBox("Send as Hex")
        if command_info:
            self.hex_check.setChecked(command_info.get('is_hex', False))
            
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Command:", self.command_input)
        form_layout.addRow("", self.hex_check)
        
        layout.addLayout(form_layout)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "command": self.command_input.text().strip(),
            "is_hex": self.hex_check.isChecked()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_manager = SerialManager()
        self.command_manager = CommandManager()
        self.current_worker = None
        
        self.init_ui()
        self.apply_styles()
        self.refresh_ports()

    def init_ui(self):
        self.setWindowTitle("SparkSerial Pro")
        self.setMinimumSize(900, 600)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left Panel Tool Widget
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(400)  # Increased slightly more for complex port names

        # Connection Settings (Compact)
        config_group = QGroupBox("Configuration")
        config_grid = QGridLayout()
        config_grid.setSpacing(10)  # Increased spacing for clarity
        config_grid.setContentsMargins(10, 15, 10, 10)
        config_grid.addWidget(QLabel("Port:"), 0, 0)
        port_row = QHBoxLayout()
        self.port_combo = QComboBox()
        # Remove rigid fixed heights, use standard sizing
        port_row.addWidget(self.port_combo, 1)
        refresh_btn = QPushButton("↻")
        refresh_btn.setToolTip("Refresh Ports")
        refresh_btn.setFixedWidth(40)
        refresh_btn.clicked.connect(self.refresh_ports)
        port_row.addWidget(refresh_btn)
        config_grid.addLayout(port_row, 0, 1, 1, 3)

        # Baud & Data Bits
        config_grid.addWidget(QLabel("Baud:"), 1, 0)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        self.baud_combo.setCurrentText("9600")
        config_grid.addWidget(self.baud_combo, 1, 1)

        config_grid.addWidget(QLabel("Data:"), 1, 2)
        self.data_combo = QComboBox()
        self.data_combo.addItems(["5", "6", "7", "8"])
        self.data_combo.setCurrentText("8")
        config_grid.addWidget(self.data_combo, 1, 3)

        # Parity & Stop Bits
        config_grid.addWidget(QLabel("Parity:"), 2, 0)
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(["None", "Even", "Odd", "Mark", "Space"])
        config_grid.addWidget(self.parity_combo, 2, 1)

        config_grid.addWidget(QLabel("Stop:"), 2, 2)
        self.stop_combo = QComboBox()
        self.stop_combo.addItems(["1", "1.5", "2"])
        config_grid.addWidget(self.stop_combo, 2, 3)

        # Flow Control
        config_grid.addWidget(QLabel("Flow:"), 3, 0)
        self.flow_combo = QComboBox()
        self.flow_combo.addItems(["None", "RTS/CTS", "XON/XOFF"])
        config_grid.addWidget(self.flow_combo, 3, 1, 1, 3)

        config_group.setLayout(config_grid)
        left_layout.addWidget(config_group)

        # Connect/Disconnect Button
        self.connect_btn = QPushButton("Connect Device")
        self.connect_btn.setObjectName("connectButton")
        self.connect_btn.setMinimumHeight(40)  # Make it prominent
        self.connect_btn.clicked.connect(self.toggle_connection)
        left_layout.addWidget(self.connect_btn)

        # Saved Commands (Now on left)
        saved_group = QGroupBox("Command Shortcuts")
        saved_group_layout = QVBoxLayout()
        saved_group_layout.setContentsMargins(10, 15, 10, 10)
        
        self.commands_list = QListWidget()
        self.commands_list.itemDoubleClicked.connect(self.load_saved_command)
        saved_group_layout.addWidget(self.commands_list)
        
        cmd_btns = QHBoxLayout()
        add_cmd_btn = QPushButton("Add")
        add_cmd_btn.clicked.connect(self.add_command_dialog)
        edit_cmd_btn = QPushButton("Edit")
        edit_cmd_btn.clicked.connect(self.edit_command_dialog)
        del_cmd_btn = QPushButton("Delete")
        del_cmd_btn.clicked.connect(self.delete_command)
        
        # Consistent industry styling
        for btn in [add_cmd_btn, edit_cmd_btn, del_cmd_btn]:
            btn.setMinimumHeight(32)
        
        cmd_btns.addWidget(add_cmd_btn)
        cmd_btns.addWidget(edit_cmd_btn)
        cmd_btns.addWidget(del_cmd_btn)
        saved_group_layout.addLayout(cmd_btns)
        
        saved_group.setLayout(saved_group_layout)
        left_layout.addWidget(saved_group)

        # Right Panel: Terminal and Tools
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Terminal Settings
        term_settings = QHBoxLayout()
        self.autoscroll_check = QCheckBox("Autoscroll")
        self.autoscroll_check.setChecked(True)
        self.hex_view_check = QCheckBox("Hex View")
        self.timestamp_check = QCheckBox("Timestamps")
        self.logging_check = QCheckBox("Log to File")
        self.logging_check.toggled.connect(self.toggle_logging)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_terminal)
        
        term_settings.addWidget(self.autoscroll_check)
        term_settings.addWidget(self.hex_view_check)
        term_settings.addWidget(self.timestamp_check)
        term_settings.addWidget(self.logging_check)
        term_settings.addStretch()
        term_settings.addWidget(clear_btn)
        
        right_layout.addLayout(term_settings)

        # Terminal Output
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        right_layout.addWidget(self.terminal)

        # Input Area
        input_group = QGroupBox("Send Command")
        input_layout = QVBoxLayout()
        
        send_row = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.returnPressed.connect(self.send_command)
        
        self.line_ending_combo = QComboBox()
        self.line_ending_combo.addItems(["None", "CR", "LF", "CR+LF"])
        self.line_ending_combo.setCurrentText("CR+LF")
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_command)
        
        send_row.addWidget(self.command_input)
        send_row.addWidget(self.line_ending_combo)
        send_row.addWidget(send_btn)
        
        input_layout.addLayout(send_row)
        
        options_row = QHBoxLayout()
        self.send_hex_check = QCheckBox("Send as Hex")
        self.log_sent_check = QCheckBox("Log Sent")
        self.log_sent_check.setChecked(True)
        options_row.addWidget(self.send_hex_check)
        options_row.addWidget(self.log_sent_check)
        options_row.addStretch()
        
        input_layout.addLayout(options_row)
        input_group.setLayout(input_layout)
        right_layout.addWidget(input_group)

        # Add panels to main layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 1) # Terminal panel gets more space
        main_layout.addWidget(splitter)
        
        self.refresh_commands_list()

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Disconnected")
        
        # Logging State
        self.log_file = None
        self.log_path = None

    def apply_styles(self):
        self.setStyleSheet(get_stylesheet())

    def refresh_ports(self):
        current_port = self.port_combo.currentText()
        self.port_combo.clear()
        ports = self.serial_manager.get_available_ports()
        self.port_combo.addItems(ports)
        if current_port in ports:
            self.port_combo.setCurrentText(current_port)

    def toggle_connection(self):
        if self.current_worker:
            self.disconnect_serial()
        else:
            self.connect_serial()

    def toggle_logging(self, enabled):
        if enabled:
            from PyQt6.QtWidgets import QFileDialog
            from datetime import datetime
            
            default_name = f"serial_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            initial_path = os.path.join(os.getcwd(), "logs", default_name)
            
            # Ensure logs directory exists as a default suggestion
            if not os.path.exists("logs"):
                os.makedirs("logs")

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Select Log File Location",
                initial_path,
                "Text Files (*.txt);;All Files (*)"
            )

            if file_path:
                try:
                    self.log_path = file_path
                    self.log_file = open(self.log_path, "a", encoding="utf-8")
                    self.status_bar.showMessage(f"Logging to: {os.path.basename(self.log_path)}")
                except Exception as e:
                    self.status_bar.showMessage(f"Logging Error: {str(e)}")
                    self.logging_check.setChecked(False)
            else:
                # User cancelled the dialog
                self.logging_check.setChecked(False)
        else:
            if self.log_file:
                self.log_file.close()
                self.log_file = None
                self.status_bar.showMessage("Logging stopped")

    def connect_serial(self):
        port = self.port_combo.currentText()
        if not port:
            self.status_bar.showMessage("Error: No port selected")
            return

        settings = {
            'port': port,
            'baudrate': int(self.baud_combo.currentText()),
            'bytesize': int(self.data_combo.currentText()),
            'parity': getattr(serial, f"PARITY_{self.parity_combo.currentText().upper()}"),
            'stopbits': {
                "1": serial.STOPBITS_ONE,
                "1.5": serial.STOPBITS_ONE_POINT_FIVE,
                "2": serial.STOPBITS_TWO
            }[self.stop_combo.currentText()],
            'flowcontrol': self.flow_combo.currentText()
        }

        self.current_worker = self.serial_manager.connect(settings)
        if self.current_worker:
            self.current_worker.data_received.connect(self.handle_data)
            self.current_worker.error_occurred.connect(self.handle_error)
            self.current_worker.connection_status.connect(self.update_connection_ui)
            
            self.connect_btn.setText("Disconnect")
            self.connect_btn.setObjectName("disconnectButton")
            self.apply_styles()
            self.status_bar.showMessage(f"Connected to {port}")

    def disconnect_serial(self):
        self.serial_manager.disconnect()
        self.current_worker = None
        self.connect_btn.setText("Connect")
        self.connect_btn.setObjectName("connectButton")
        self.apply_styles()
        self.status_bar.showMessage("Disconnected")

    @pyqtSlot(bool)
    def update_connection_ui(self, connected):
        if not connected:
            self.disconnect_serial()

    @pyqtSlot(bytes)
    def handle_data(self, data):
        from datetime import datetime
        now = datetime.now()
        
        if self.hex_view_check.isChecked():
            text = " ".join([f"{b:02X}" for b in data]) + " "
        else:
            try:
                text = data.decode('utf-8', errors='replace')
            except:
                text = str(data)

        timestamp_str = now.strftime("[%H:%M:%S.%f] ")[:-4] + "] "
        
        # Display logic
        display_text = text
        if self.timestamp_check.isChecked():
            if not self.terminal.toPlainText() or self.terminal.toPlainText().endswith('\n'):
                display_text = timestamp_str + display_text
            display_text = display_text.replace('\n', f'\n{timestamp_str}')

        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.terminal.insertPlainText(display_text)
        
        if self.autoscroll_check.isChecked():
            self.terminal.verticalScrollBar().setValue(self.terminal.verticalScrollBar().maximum())

        # Logging logic
        if self.log_file:
            log_entry = text
            if self.timestamp_check.isChecked() or True: # Always timestamp logs for better utility
                if not hasattr(self, '_log_at_newline') or self._log_at_newline:
                    log_entry = f"RX {timestamp_str}{log_entry}"
                log_entry = log_entry.replace('\n', f'\nRX {timestamp_str}')
                self._log_at_newline = text.endswith('\n')
            
            self.log_file.write(log_entry)
            self.log_file.flush()

    @pyqtSlot(str)
    def handle_error(self, message):
        self.status_bar.showMessage(f"Error: {message}")
        self.disconnect_serial()

    def send_command(self):
        if not self.current_worker:
            self.status_bar.showMessage("Error: Not connected")
            return

        command = self.command_input.text()
        if not command:
            return

        try:
            if self.send_hex_check.isChecked():
                data = bytes.fromhex(command.replace(" ", ""))
            else:
                data = command.encode('utf-8')
                
            # Add line ending
            ending = self.line_ending_combo.currentText()
            line_end = b''
            if ending == "CR":
                line_end = b'\r'
            elif ending == "LF":
                line_end = b'\n'
            elif ending == "CR+LF":
                line_end = b'\r\n'
            
            full_data = data + line_end

            self.current_worker.send_data(full_data)
            
            # Log sent command
            if self.log_file and self.log_sent_check.isChecked():
                from datetime import datetime
                ts = datetime.now().strftime("[%H:%M:%S.%f] ")[:-4] + "] "
                sent_text = command
                if self.send_hex_check.isChecked():
                    sent_text = f"HEX({command})"
                self.log_file.write(f"TX {ts}{sent_text}\n")
                self.log_file.flush()
                self._log_at_newline = True

            self.command_input.clear()
        except Exception as e:
            self.status_bar.showMessage(f"Send Error: {str(e)}")

    def clear_terminal(self):
        self.terminal.clear()

    # Saved Commands Methods
    def refresh_commands_list(self):
        self.commands_list.clear()
        for cmd in self.command_manager.get_commands():
            display_text = f"{cmd['name']} : {cmd['command']}"
            item = QListWidgetItem(display_text)
            tooltip = f"Command: {cmd['command']}\nType: {'Hex' if cmd['is_hex'] else 'Text'}"
            item.setToolTip(tooltip)
            self.commands_list.addItem(item)

    def add_command_dialog(self):
        dialog = CommandDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['name'] and data['command']:
                self.command_manager.add_command(data['name'], data['command'], data['is_hex'])
                self.refresh_commands_list()
            else:
                QMessageBox.warning(self, "Invalid Input", "Name and Command cannot be empty.")

    def edit_command_dialog(self):
        index = self.commands_list.currentRow()
        if index < 0:
            QMessageBox.information(self, "Selection Required", "Please select a command to edit.")
            return
            
        cmd_info = self.command_manager.get_commands()[index]
        dialog = CommandDialog(self, cmd_info)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['name'] and data['command']:
                self.command_manager.update_command(index, data['name'], data['command'], data['is_hex'])
                self.refresh_commands_list()

    def delete_command(self):
        index = self.commands_list.currentRow()
        if index < 0:
            return
            
        confirm = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete '{self.command_manager.get_commands()[index]['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.command_manager.delete_command(index)
            self.refresh_commands_list()

    def load_saved_command(self, item):
        index = self.commands_list.row(item)
        cmd_info = self.command_manager.get_commands()[index]
        self.command_input.setText(cmd_info['command'])
        self.send_hex_check.setChecked(cmd_info['is_hex'])

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
