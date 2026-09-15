from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox
from PyQt6.QtCore import Qt
from sparkserial.gui.styles import get_stylesheet

class ConverterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tools - Base Converter")
        self.setMinimumWidth(300)
        self.setLayout(QVBoxLayout())
        
        self.setStyleSheet(get_stylesheet())
        
        self.updating = False
        
        form_layout = QFormLayout()
        
        self.dec_input = QLineEdit()
        self.dec_input.setPlaceholderText("Decimal value")
        
        self.hex_input = QLineEdit()
        self.hex_input.setPlaceholderText("Hex value (e.g. FF)")
        
        self.bin_input = QLineEdit()
        self.bin_input.setPlaceholderText("Binary value (e.g. 1010)")
        
        self.ascii_input = QLineEdit()
        self.ascii_input.setPlaceholderText("ASCII char")
        self.ascii_input.setMaxLength(1)  # Limit to 1 char for scalar conversion
        
        form_layout.addRow("Decimal:", self.dec_input)
        form_layout.addRow("Hexadecimal:", self.hex_input)
        form_layout.addRow("Binary:", self.bin_input)
        form_layout.addRow("ASCII:", self.ascii_input)
        
        self.layout().addLayout(form_layout)
        
        # Close button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.close)
        self.layout().addWidget(buttons)
        
        # Connect signals
        self.dec_input.textChanged.connect(self.on_dec_changed)
        self.hex_input.textChanged.connect(self.on_hex_changed)
        self.bin_input.textChanged.connect(self.on_bin_changed)
        self.ascii_input.textChanged.connect(self.on_ascii_changed)

    def on_dec_changed(self, text):
        if self.updating: return
        if not text:
            self.clear_all(exclude='dec')
            return
            
        try:
            value = int(text)
            self.update_fields(value, exclude='dec')
        except ValueError:
            pass

    def on_hex_changed(self, text):
        if self.updating: return
        if not text:
            self.clear_all(exclude='hex')
            return
            
        try:
            # Handle 0x prefix or spaces
            clean_text = text.replace("0x", "").replace(" ", "")
            if not clean_text: return
            value = int(clean_text, 16)
            self.update_fields(value, exclude='hex')
        except ValueError:
            pass

    def on_bin_changed(self, text):
        if self.updating: return
        if not text:
            self.clear_all(exclude='bin')
            return
            
        try:
            # Handle 0b prefix or spaces
            clean_text = text.replace("0b", "").replace(" ", "")
            if not clean_text: return
            value = int(clean_text, 2)
            self.update_fields(value, exclude='bin')
        except ValueError:
            pass

    def on_ascii_changed(self, text):
        if self.updating: return
        if not text:
            self.clear_all(exclude='ascii')
            return
            
        try:
            value = ord(text[0])
            self.update_fields(value, exclude='ascii')
        except (ValueError, IndexError):
            pass

    def update_fields(self, value, exclude=None):
        self.updating = True
        try:
            if exclude != 'dec':
                self.dec_input.setText(str(value))
            
            if exclude != 'hex':
                self.hex_input.setText(f"{value:X}")
                
            if exclude != 'bin':
                self.bin_input.setText(f"{value:b}")
                
            if exclude != 'ascii':
                if 32 <= value <= 126:
                    self.ascii_input.setText(chr(value))
                else:
                    self.ascii_input.setText("")
        except Exception:
            pass
        finally:
            self.updating = False

    def clear_all(self, exclude=None):
        self.updating = True
        if exclude != 'dec': self.dec_input.clear()
        if exclude != 'hex': self.hex_input.clear()
        if exclude != 'bin': self.bin_input.clear()
        if exclude != 'ascii': self.ascii_input.clear()
        self.updating = False
