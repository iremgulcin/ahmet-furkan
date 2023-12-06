import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

app = QApplication(sys.argv)

view = QWebEngineView()
view.setWindowTitle("Samsung Innovation Campus Sağlık Paneli")
view.load(QUrl('http://127.0.0.1:5000/'))
view.show()

sys.exit(app.exec_())
