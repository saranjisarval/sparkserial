def get_stylesheet():
    return """
    QMainWindow {
        background-color: #1e1e1e;
        color: #d4d4d4;
    }
    
    QWidget {
        font-family: 'Helvetica Neue', 'Arial', sans-serif;
        font-size: 13px;
    }

    QGroupBox {
        border: 1px solid #3c3c3c;
        border-radius: 6px;
        margin-top: 20px;
        padding-top: 15px;
        font-weight: bold;
        color: #007acc; /* Industry standard blue */
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }

    QLabel {
        color: #cccccc;
    }

    QComboBox, QLineEdit, QPlainTextEdit {
        background-color: #252526;
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        padding: 4px;
        color: #d4d4d4;
    }

    QComboBox:focus, QLineEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #007acc;
    }

    QComboBox {
        padding-left: 10px;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 1px solid #3c3c3c;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid #cccccc;
    }

    QComboBox QAbstractItemView {
        background-color: #252526;
        color: #d4d4d4;
        selection-background-color: #04395e;
        selection-color: #ffffff;
        border: 1px solid #3c3c3c;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        min-height: 25px;
        padding-left: 10px;
    }

    QComboBox:hover, QLineEdit:hover {
        border: 1px solid #007acc;
    }

    QPushButton {
        background-color: #3c3c3c;
        border: none;
        border-radius: 3px;
        padding: 6px 16px;
        color: #ffffff;
    }

    QPushButton:hover {
        background-color: #4c4c4c;
    }

    QPushButton:pressed {
        background-color: #2c2c2c;
    }

    QPushButton#connectButton {
        background-color: #2ea043; /* GitHub Green */
        color: #ffffff;
    }

    QPushButton#connectButton:hover {
        background-color: #3fb950;
    }

    QPushButton#disconnectButton {
        background-color: #da3633; /* GitHub Red */
        color: #ffffff;
    }

    QPushButton#disconnectButton:hover {
        background-color: #f85149;
    }

    QPlainTextEdit {
        font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
        font-size: 12px;
        background-color: #1e1e1e;
        border: 1px solid #3c3c3c;
        selection-background-color: #264f78;
        selection-color: #ffffff;
    }

    QStatusBar {
        background-color: #007acc;
        color: #ffffff;
    }

    QScrollBar:vertical {
        border: none;
        background: #1e1e1e;
        width: 12px;
        margin: 0px;
    }

    QScrollBar::handle:vertical {
        background: #424242;
        min-height: 20px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical:hover {
        background: #686868;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }

    QListWidget {
        background-color: #252526;
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        color: #d4d4d4;
        padding: 5px;
        outline: none;
    }

    QListWidget::item {
        padding: 5px;
        border-bottom: 1px solid #3c3c3c;
    }

    QListWidget::item:selected {
        background-color: #04395e;
        color: #ffffff;
        border-radius: 3px;
    }

    QListWidget::item:hover {
        background-color: #2a2d2e;
    }

    QDialog {
        background-color: #1e1e1e;
        color: #d4d4d4;
    }
    
    /* Checkbox Styling - Industry Standard with Checkmark */
    QCheckBox {
        color: #d4d4d4;
        spacing: 8px;
        padding: 4px;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #6e6e6e;
        border-radius: 3px;
        background: #252526;
    }

    QCheckBox::indicator:unchecked:hover {
        border-color: #007acc;
        background: #2a2d2e;
    }

    QCheckBox::indicator:checked {
        background-color: #007acc;
        border: 2px solid #007acc;
    }

    QCheckBox::indicator:checked:hover {
        background-color: #1e8ad2;
        border-color: #1e8ad2;
    }

    /* Splitter styling */
    QSplitter::handle {
        background-color: #3c3c3c;
    }

    QSplitter::handle:horizontal {
        width: 2px;
    }

    QSplitter::handle:vertical {
        height: 2px;
    }

    QSplitter::handle:hover {
        background-color: #007acc;
    }

    /* Tooltip */
    QToolTip {
        background-color: #252526;
        color: #d4d4d4;
        border: 1px solid #3c3c3c;
        padding: 4px;
    }
    """
