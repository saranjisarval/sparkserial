import sys
import os
from PyQt6.QtWidgets import QApplication
from sparkserial.gui.main_window import MainWindow

def set_macos_app_details():
    if sys.platform == "darwin":
        try:
            # Set App Name in Dock/Menu
            from Cocoa import NSBundle
            bundle = NSBundle.mainBundle()
            if bundle:
                info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                if info:
                    info['CFBundleName'] = "SparkSerial Pro"
                    info['CFBundleDisplayName'] = "SparkSerial Pro"

            # Set Dock Icon
            from AppKit import NSApp, NSImage
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
            if os.path.exists(icon_path):
                image = NSImage.alloc().initWithContentsOfFile_(icon_path)
                if image:
                    NSApp.setApplicationIconImage_(image)
        except Exception as e:
            print(f"macOS specific setup failed: {e}")

def main():
    # Set the application ID for better process management
    # No-op on macOS for name but helps overall
    import ctypes
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("antigravity.sparkserial.1.0")
        
    app = QApplication(sys.argv)
    app.setApplicationName("SparkSerial Pro")
    
    # Needs to be called after QApplication init for NSApp to exist
    set_macos_app_details()
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
