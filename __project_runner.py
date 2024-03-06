import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt App with PyQt5")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        tree_view = QTreeView()
        model = QFileSystemModel()
        model.setRootPath("")
        tree_view.setModel(model)
        layout.addWidget(tree_view)

        properties_panel = QWidget()
        properties_layout = QVBoxLayout()
        properties_panel.setLayout(properties_layout)

        properties_label = QLabel("Properties Panel")
        properties_layout.addWidget(properties_label)

        layout.addWidget(properties_panel)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

