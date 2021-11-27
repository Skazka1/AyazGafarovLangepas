import sqlite3
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox

import auth
import reg
from project import *

with sqlite3.connect('users.db') as con:
    cur = con.cursor()
    result = cur.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT,
    password INTEGER
    )""").fetchall()


class Interface(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.white_theme = True
        self.ui.home.clicked.connect(self.home)
        self.ui.reload.clicked.connect(self.reload)
        self.ui.back.clicked.connect(self.back)
        self.ui.search.clicked.connect(self.search)
        self.ui.history.clicked.connect(self.history)

        self.ui.back.setToolTip('Назад')
        self.ui.reload.setToolTip('Обновить')
        self.ui.home.setToolTip('Главная')
        self.ui.search.setToolTip('Поиск')
        self.ui.history.setToolTip('Пользователи')

        # Инициализация WebView
        self.web = QtWebEngineWidgets.QWebEngineView()
        self.ui.gridLayout.addWidget(self.web, 1, 0, 1, 7)

    def home(self):
        home_page = QtCore.QUrl('https://www.google.com/')
        self.web.load(home_page)

    def reload(self):
        self.web.reload()

    def back(self):
        self.web.back()

    def search(self, event):
        text = self.ui.lineEdit.text()

        if not text.startswith('http'):
            text = QtCore.QUrl('https://www.google.com/search?q=' + text)

        else:
            text = QtCore.QUrl(text)

        self.web.load(text)

    def history(self):
        windows = auth_window(self)
        windows.show()




class auth_window(QtWidgets.QMainWindow):
    def __init__(self, parent=Interface):
        super().__init__(parent, QtCore.Qt.Window)
        self.auth = auth.Ui_Formauth()
        self.auth.setupUi(self)
        self.setWindowModality(2)

        self.auth.signin.clicked.connect(self.check_inf)
        self.auth.create.clicked.connect(self.reg)

    def reg(self):
        windows = auth_window(self)
        windows.close()
        window = reg_window(self)
        window.show()

    def check_inf(self):
        log = self.auth.Login.text()
        passw = self.auth.password.text()
        passw = int(passw)
        with sqlite3.connect('users.db') as con:
            cur = con.cursor()
            value = cur.execute(f'SELECT * FROM users WHERE login="{log}";').fetchall()
            if value != [] and value[0][2] == passw:
                QMessageBox.about(self, "Успешно!", "Вы вошли в систему!")

            else:
                QMessageBox.about(self, "Ошибка", "Проверьте введённые данные!")


class reg_window(QtWidgets.QMainWindow):
    def __init__(self, parent=auth_window):
        super().__init__(parent, QtCore.Qt.Window)
        self.reg = reg.Ui_Formreg()
        self.reg.setupUi(self)
        self.setWindowModality(2)
        self.reg.signup.clicked.connect(self.register)
        self.reg.pushButton_2.clicked.connect(self.close)

    def register(self):
        login = self.reg.log.text()
        password = self.reg.passw.text()
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        value = cur.execute(f'SELECT * FROM users WHERE login="{login}";').fetchall()
        print(value)
        if value != []:
            print('NET')
            QMessageBox.about(self, "Ошибка", "Данное имя пользователя уже используется")
        elif value == []:
            cur.execute(f'INSERT INTO users (login, password) VALUES ("{login}", "{password}")')
            print('DA')
            con.commit()
            QMessageBox.about(self, "Успешно", "Данные о пользователи внесены")

        cur.close()
        con.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Interface()
    myapp.show()
    sys.exit(app.exec_())
