def get_stylesheet():
    return """
    QMainWindow {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }
    
    QWidget {
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 13px;
    }

    QGroupBox {
        border: 1px solid #45475a;
        border-radius: 8px;
        margin-top: 20px;
        padding-top: 20px;
        font-weight: bold;
        color: #89b4fa;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }

    QLabel {
        color: #bac2de;
    }

    QComboBox, QLineEdit, QPlainTextEdit {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 4px;
        padding: 4px;
        color: #cdd6f4;
    }

    QComboBox {
        padding-left: 10px;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 1px solid #45475a;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid #89b4fa;
    }

    QComboBox QAbstractItemView {
        background-color: #313244;
        color: #cdd6f4;
        selection-background-color: #45475a;
        selection-color: #89b4fa;
        border: 1px solid #45475a;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        min-height: 30px;
        padding-left: 10px;
    }

    QComboBox:hover, QLineEdit:hover {
        border: 1px solid #89b4fa;
    }

    QPushButton {
        background-color: #45475a;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        color: #cdd6f4;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #585b70;
    }

    QPushButton#connectButton {
        background-color: #a6e3a1;
        color: #11111b;
    }

    QPushButton#connectButton:hover {
        background-color: #94e2d5;
    }

    QPushButton#disconnectButton {
        background-color: #f38ba8;
        color: #11111b;
    }

    QPushButton#disconnectButton:hover {
        background-color: #eba0ac;
    }

    QPlainTextEdit {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        selection-background-color: #89b4fa;
        selection-color: #1e1e2e;
    }

    QStatusBar {
        background-color: #181825;
        color: #bac2de;
    }

    QScrollBar:vertical {
        border: none;
        background: #1e1e2e;
        width: 10px;
        margin: 0px;
    }

    QScrollBar::handle:vertical:hover {
        background: #585b70;
    }

    QListWidget {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 4px;
        color: #cdd6f4;
        padding: 5px;
        outline: none;
    }

    QListWidget::item {
        padding: 8px;
        border-bottom: 1px solid #45475a;
    }

    QListWidget::item:selected {
        background-color: #45475a;
        color: #89b4fa;
        border-radius: 4px;
    }

    QListWidget::item:hover {
        background-color: #3b3d52;
    }

    QDialog {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }

    QTabWidget::pane {
        border: 1px solid #45475a;
        top: -1px;
        background: #1e1e2e;
    }

    QTabBar::tab {
        background: #313244;
        color: #cdd6f4;
        padding: 8px 12px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background: #1e1e2e;
        border-bottom: 2px solid #89b4fa;
    }
    """
