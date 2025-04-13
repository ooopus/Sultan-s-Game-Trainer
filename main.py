import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import AttributeEditor

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = AttributeEditor()
    editor.show()
    sys.exit(app.exec())
