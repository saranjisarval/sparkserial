from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from sparkserial.gui.styles import get_stylesheet


class WhatsNewDialog(QDialog):
    """Small popup shown the first time the app is opened after an upgrade,
    summarizing what changed in the version(s) the user skipped straight to."""

    def __init__(self, parent=None, release_notes=None):
        super().__init__(parent)
        self.setWindowTitle("What's New in SparkSerial Pro")
        self.setMinimumWidth(420)
        self.setMaximumHeight(480)
        self.setStyleSheet(get_stylesheet())

        layout = QVBoxLayout(self)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        for version_str, highlights in release_notes or []:
            version_label = QLabel(f"<b>Version {version_str}</b>")
            content_layout.addWidget(version_label)

            items_html = "".join(f"<li>{self._escape(h)}</li>" for h in highlights)
            notes_label = QLabel(f"<ul style='margin-top:2px;'>{items_html}</ul>")
            notes_label.setWordWrap(True)
            content_layout.addWidget(notes_label)

        content_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    @staticmethod
    def _escape(text):
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
