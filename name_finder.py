from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QScrollArea, QScrollBar
from PyQt5.QtGui import QFont, QIcon, QPainter, QBrush, QColor, QFontDatabase
from PyQt5.QtCore import Qt
import sys, os

class ModernFileExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Folder list maker by satyam")
        self.setGeometry(300, 150, 600, 400)
        self.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")

        layout = QVBoxLayout()
        
        self.label = QLabel("DirScan – Scan directories instantly\U0001F4C2 ")
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.label)
        
        self.btn_select = QPushButton("Select Directory")
        self.btn_select.setFont(QFont("Arial", 12))
        self.btn_select.setStyleSheet("""
            background-color: #333333;
            color: #FFFFFF;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        """)
        self.btn_select.clicked.connect(self.open_directory)
        layout.addWidget(self.btn_select)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont("Arial", 11))
        self.text_area.setStyleSheet("""
            background-color: #252526;
            color: #FFFFFF;
            padding: 10px;
            border-radius: 10px;
            border: none;
        """)
        
        self.text_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setWidget(self.text_area)
        
        # Improve scrollbar style
        self.scroll_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #333;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        layout.addWidget(self.scroll_area)
        
        button_layout = QHBoxLayout()
        
        self.btn_save = QPushButton("Save on Desktop")
        self.btn_save.setFont(QFont("Arial", 12))
        self.btn_save.setStyleSheet("""
            background-color: #444444;
            color:rgb(255, 255, 255);
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        """)
        self.btn_save.clicked.connect(self.save_file_list)
        button_layout.addWidget(self.btn_save)

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setFont(QFont("Arial", 12))
        self.btn_exit.setStyleSheet("""
            background-color: #880808;
            color: #FFFFFF;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        """)
        self.btn_exit.clicked.connect(self.close)
        button_layout.addWidget(self.btn_exit)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.text_area.clear()
            self.file_list = os.listdir(directory)
            for index, file in enumerate(self.file_list, start=1):
                self.text_area.append(f"{index}. {file}")
            self.current_directory = directory

    def save_file_list(self):
        if hasattr(self, 'file_list') and self.file_list:
            directory_name = os.path.basename(self.current_directory)
            filename = f"{directory_name}_directory_list.txt"
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
            
            if not os.path.exists(os.path.dirname(desktop_path)):
                onedrive_desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", filename)
                desktop_path = onedrive_desktop if os.path.exists(os.path.dirname(onedrive_desktop)) else desktop_path
            
            try:
                with open(desktop_path, "w", encoding="utf-8") as file:
                    for index, file_name in enumerate(self.file_list, start=1):
                        file.write(f"{index}. {file_name}\n")  # Add sequence number before filename
                    
                self.text_area.append(f"\n ✅ SUCCESS ✅\n File list saved on your desktop as {filename}")
            except Exception as e:
                self.text_area.append(f"\n❌ Error saving file: {str(e)}")
        else:
            self.text_area.append("\n⚠️ No directory selected!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = ModernFileExplorer()
    ex.show()
    sys.exit(app.exec_())
