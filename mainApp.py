from settings import *


class WidgetAddUser(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("QFrame{background-color: rgb(0,0,0,200);}")

        self.widget = QWidget(self)
        self.widget.show()
        self.widget.setStyleSheet("border-radius: 20px")
        self.widget.resize(620, 400)

        self.label = QLabel(self.widget)
        self.label.setText("Введите данные для создания пользователя!")
        self.label.move(0, 0)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(620, 60)

        self.nameEdit = QLineEdit(self.widget)
        self.nameEdit.show()
        self.nameEdit.setStyleSheet(st)
        self.nameEdit.move(0, self.label.height())
        self.nameEdit.resize(620, 120)
        self.nameEdit.setPlaceholderText("логин")

        self.passwordEdit = QLineEdit(self.widget)
        self.passwordEdit.show()
        self.passwordEdit.setStyleSheet(st)
        self.passwordEdit.move(0, self.nameEdit.height() + self.nameEdit.y())
        self.passwordEdit.resize(620, 120)
        self.passwordEdit.setPlaceholderText("пароль")

        self.button_create = QPushButton(self.widget)
        self.button_create.resize(250, 100)
        self.button_create.setStyleSheet(st)
        self.button_create.show()
        self.button_create.setText("Создать")

        self.button_cancel = QPushButton(self.widget)
        self.button_cancel.resize(250, 100)
        self.button_cancel.setStyleSheet(st)
        self.button_cancel.show()
        self.button_cancel.setText("Отмена")

    def resize_event(self):
        self.widget.move(self.width() // 2 - self.widget.width() // 2, self.height() // 2 - self.widget.height() // 2)
        self.button_create.move(self.widget.width() // 2 - self.button_create.width(),
                             self.passwordEdit.height() + self.passwordEdit.y())
        self.button_cancel.move(self.widget.width() // 2,
                             self.passwordEdit.height() + self.passwordEdit.y())


class WidgetCharacteristic(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setProperty("houdiniStyle", True)
        self.table.setIconSize(QSize(400, 500))
        self.table.setStyleSheet(
            """
            QTableWidget::item:pressed,QTableWidget::item:selected{border:3px solid rgb(104,79,243);color: rgb(104,79,243); border-radius: 10px}
            QTableWidget{border: 3px solid green; border-radius: 20px; padding: 5px 5px 5px 5px}""")
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        self.table.show()

        self.button_back = QPushButton(self.table)
        self.button_back.show()
        self.button_back.setText("Назад")
        self.button_back.resize(200, 60)

    def update_(self, ch):
        ch1 = ch["text"]
        ch2 = ch["img"]
        self.table.setRowCount(len(ch1) + len(ch2))
        self.table.setRowHeight(4, 100)
        self.table.setRowHeight(5, 300)
        index = 0

        for i in ch1:
            it = QTableWidgetItem(i)
            it.setFlags(Qt.ItemIsEnabled)
            it2 = QTableWidgetItem(ch1[i])
            it2.setForeground(QColor(104,79,243))
            self.table.setItem(index, 0, it)
            self.table.setItem(index, 1, it2)
            index += 1
        for i in ch2:
            it = QTableWidgetItem(i)
            it.setFlags(Qt.ItemIsEnabled)
            it2 = QTableWidgetItem()
            it2.setFlags(Qt.ItemIsEnabled)
            icon = QIcon(ch2[i])
            it2.setIcon(icon)
            it2.setSizeHint(QSize(100, 100))
            self.table.setItem(index, 0, it)
            self.table.setItem(index, 1, it2)
            index += 1

    def resize_event(self):
        self.table.resize(self.width() - 40, self.height() - 100)
        self.table.move(20, 20)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, self.table.width() - 320)
        self.button_back.move(0, self.table.height() - 60)


class Data:
    def __init__(self):
        self.conn = sqlite3.connect(r'data_ad.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   id INT PRIMARY KEY,
                   name TEXT,
                   password TEXT,
                   date TEXT);
                """)
        self.conn.commit()

    def add_value(self, name, password):
        self.cur.execute("SELECT * FROM users;")
        id_ = len(self.cur.fetchall())
        value = (id_, name, password, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?);", value)
        self.conn.commit()

    def get_value(self):
        self.cur.execute("SELECT * FROM users;")
        results = self.cur.fetchall()
        self.conn.commit()
        return results

    def remove_value(self, index):
        if index != -1:
            self.cur.execute(f"DELETE from users where id = {index}")
            self.cur.execute(f"UPDATE users SET id=id-1 WHERE id > {index}")
            self.conn.commit()


class AdminWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(1300, 900)
        self.setStyleSheet(base_style)
        self.server = args[0].server
        self.admin_data = Data()

        self.timer = QTimer()
        self.timer.setInterval(20000)
        self.timer.timeout.connect(self.timer_event)
        self.timer.start()

        self.widget_users = QWidget(self)
        self.widget_settings = QWidget(self)
        self.widget_descript = QWidget(self)

        self.widget_characteristic = WidgetCharacteristic(self)
        self.widget_characteristic.button_back.clicked.connect(self.open_window_users)

        self.table = QTableWidget(self.widget_users)  # Create a table
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["id", "Имя", "Пароль", "Дата"])
        self.table.verticalHeader().hide()
        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setProperty("houdiniStyle", True)
        self.table.setStyleSheet("""QTableWidget{border: 3px solid green; border-radius: 20px; padding: 5px 5px 60px 5px}""")
        self.table.doubleClicked.connect(self.open_characteristic)
        self.users = []
        self.table.show()

        self.button_change = QPushButton(self.table)
        self.button_change.show()
        self.button_change.setText("Изменить")
        self.button_change.resize(200, 60)

        self.button_characteristic = QPushButton(self.table)
        self.button_characteristic.show()
        self.button_characteristic.setText("Характеристика")
        self.button_characteristic.resize(300, 60)
        self.button_characteristic.clicked.connect(self.open_characteristic)

        self.button_delete = QPushButton(self.table)
        self.button_delete.show()
        self.button_delete.setText("Удалить")
        self.button_delete.resize(200, 60)
        self.button_delete.setStyleSheet(style_close2)
        self.button_delete.clicked.connect(self.remove_user)

        self.button_add = QPushButton(self.table)
        self.button_add.show()
        self.button_add.setText("Добавить")
        self.button_add.resize(200, 60)
        self.button_add.setStyleSheet(style_add)

        self.buttons_init()
        self.widget_add_user = WidgetAddUser(self)
        self.widget_add_user.button_create.clicked.connect(self.create_user)
        self.widget_add_user.button_cancel.clicked.connect(self.open_window_users)
        self.button_add.clicked.connect(self.widget_add_user.show)

        self.open_window_users()
        self.update()

    def timer_event(self):
        self.update()

    def create_user(self):
        self.admin_data.add_value(self.widget_add_user.nameEdit.text(), self.widget_add_user.passwordEdit.text())
        self.server.ftp_send("data_ad.db")
        self.open_window_users()
        self.update()

    def remove_user(self):
        self.admin_data.remove_value(self.table.currentRow())
        self.server.ftp_send("data_ad.db")
        self.update()


    def buttons_init(self):
        self.button_users = QPushButton(self)
        self.button_settings = QPushButton(self)
        self.button_descript = QPushButton(self)
        self.button_users.setText("Пользователи")
        self.button_settings.setText("Настройки")
        self.button_descript.setText("О приложении")

        self.number_buttons = 3

        self.button_users.clicked.connect(self.open_window_users)
        self.button_settings.clicked.connect(self.open_window_settings)
        self.button_descript.clicked.connect(self.open_window_descript)
        self.buttons_menu = [self.button_users, self.button_settings, self.button_descript]
        for b in self.buttons_menu:
            b.show()

    def open_characteristic(self):
        self.update()
        index = self.table.currentRow()
        if index != -1:
            self.users[index].update_characteristic()
            self.widget_characteristic.show()
            self.widget_characteristic.update_(self.users[index].characteristic)
            self.widget_users.hide()

    def update(self):
        if self.isHidden():
            return
        self.server.ftp_load("data_ad.db")
        results = self.admin_data.get_value()
        self.users.clear()
        if results:
            for i, elem in enumerate(results):
                self.users.append(User(elem[1], elem[2], elem[3]))

        currentRow, currentColumn = self.table.currentRow(), self.table.currentColumn()

        self.table.setRowCount(len(self.users))
        index = 0
        for i in self.users:
            self.table.setItem(index, 0, QTableWidgetItem(str(index)))
            self.table.setItem(index, 1, QTableWidgetItem(i.name))
            self.table.setItem(index, 2, QTableWidgetItem(i.password))
            self.table.setItem(index, 3, QTableWidgetItem(i.date))
            index += 1

        self.table.setCurrentCell(currentRow, currentColumn)

    def resize_event(self):
        w, h = self.width() // self.number_buttons, 65
        x, y = 0, 0
        step = 0
        for b in self.buttons_menu:
            b.resize(w, h)
            b.move(x + step, y)
            step += w

        self.widget_users.resize(self.width(), self.height() - h)
        self.widget_users.move(0, h)
        self.widget_settings.resize(self.width(), self.height() - h)
        self.widget_settings.move(0, h)
        self.widget_add_user.resize(self.size())
        self.widget_add_user.move(0, 0)
        self.widget_descript.resize(self.width(), self.height() - h)
        self.widget_descript.move(0, h)
        self.widget_characteristic.resize(self.width(), self.height() - h)
        self.widget_characteristic.move(0, h)
        self.table.resize(self.widget_users.width() - 40, self.widget_users.height() - 40)
        self.table.move(20, 20)
        w_c = (self.table.width() - 146) // (self.table.columnCount() - 1)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, w_c)
        self.table.setColumnWidth(2, w_c)
        self.table.setColumnWidth(3, w_c)

        self.button_change.move(0, self.table.height() - 60)
        self.button_characteristic.move(self.button_change.width(), self.table.height() - 60)
        self.button_delete.move(self.button_change.width() + self.button_characteristic.width(), self.table.height() - 60)
        self.button_add.move(self.button_change.width() + self.button_delete.width() + self.button_characteristic.width(), self.table.height() - 60)

        self.widget_characteristic.resize_event()
        self.widget_add_user.resize_event()

    def open_window_users(self):
        self.widget_users.show()
        self.widget_settings.hide()
        self.widget_descript.hide()
        self.widget_characteristic.hide()
        self.widget_add_user.hide()

    def open_window_settings(self):
        self.widget_users.hide()
        self.widget_settings.show()
        self.widget_descript.hide()
        self.widget_characteristic.hide()
        self.widget_add_user.hide()

    def open_window_descript(self):
        self.widget_users.hide()
        self.widget_settings.hide()
        self.widget_characteristic.hide()
        self.widget_add_user.hide()
        self.widget_descript.show()


class WidgetLogin(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widget = QWidget(self)
        self.widget.show()
        self.widget.resize(620, 400)

        self.label = QLabel(self.widget)
        self.label.setText("Введите данные для входа!")
        self.label.move(0, 0)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(620, 60)

        self.nameEdit = QLineEdit(self.widget)
        self.nameEdit.show()
        self.nameEdit.setStyleSheet(st)
        self.nameEdit.move(0, self.label.height())
        self.nameEdit.resize(620, 120)
        self.nameEdit.setPlaceholderText("логин")

        self.passwordEdit = QLineEdit(self.widget)
        self.passwordEdit.show()
        self.passwordEdit.setStyleSheet(st)
        self.passwordEdit.move(0, self.nameEdit.height() + self.nameEdit.y())
        self.passwordEdit.resize(620, 120)
        self.passwordEdit.setPlaceholderText("пароль")

        self.button_log = QPushButton(self.widget)
        self.button_log.resize(200, 100)
        self.button_log.setStyleSheet(st)
        self.button_log.show()
        self.button_log.setText("Вход")

        self.data = Data()

    def check_login(self):
        if self.nameEdit.text() and self.passwordEdit.text():
            users = [[a[1], a[2]] for a in self.data.get_value()]
            user = [self.nameEdit.text(), self.passwordEdit.text()]
            if user[0] == "admin" and user[1] == "12345678":
                return 1
            elif user in users:
                return user
            else:
                self.label.setText(errorFormat.format("Логин или пароль неверны!"))
                return False
        self.label.setText(errorFormat.format("Есть пустые строки!"))
        return False

    def resize_event(self):
        self.widget.move(self.width() // 2 - self.widget.width() // 2, self.height() // 2 - self.widget.height() // 2)
        self.button_log.move(self.widget.width() // 2 - self.button_log.width() // 2, self.passwordEdit.height() + self.passwordEdit.y())


class WidgetForm(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = QFrame(self)
        self.widget.setStyleSheet("QFrame{border: 3px solid green; border-radius: 20px;}")

        self.nameEdit = QLineEdit(self.widget)
        self.nameEdit.show()
        self.nameEdit.move(0, 10)
        self.nameEdit.setStyleSheet("font-size: 40px; margin: 10px 20px 10px 20px;")
        self.nameEdit.setPlaceholderText("Имя")

        self.surnameEdit = QLineEdit(self.widget)
        self.surnameEdit.show()
        self.surnameEdit.setStyleSheet("font-size: 40px; margin: 10px 20px 10px 20px;")
        self.surnameEdit.setPlaceholderText("Фамилия")

        self.name2Edit = QLineEdit(self.widget)
        self.name2Edit.show()
        self.name2Edit.setStyleSheet("font-size: 40px; margin: 10px 20px 10px 20px;")
        self.name2Edit.setPlaceholderText("Отчество")

        self.experienceEdit = QLineEdit(self.widget)
        self.experienceEdit.show()
        self.experienceEdit.setStyleSheet("font-size: 40px; margin: 10px 20px 10px 20px;")
        self.experienceEdit.setPlaceholderText("Опыт работы")

        self.descriptEdit = QTextEdit(self.widget)
        self.descriptEdit.show()
        self.descriptEdit.setStyleSheet("font-size: 40px; margin: 10px 20px 10px 20px; border:3px solid rgb(83,184,35)")
        self.descriptEdit.setPlaceholderText("Описание")
        self.descriptEdit.verticalScrollBar().hide()

        self.pathEdit = QLineEdit(self.widget)
        self.pathEdit.show()
        self.pathEdit.setStyleSheet("font-size: 40px; margin: 10px 20px 10px 20px;")
        self.pathEdit.setPlaceholderText("Изображение")

        self.buttonPath = QPushButton(self.widget)
        self.buttonPath.show()
        self.buttonPath.setText("Выбрать")
        self.buttonPath.clicked.connect(lambda: None)

        self.buttonSave = QPushButton(self.widget)
        self.buttonSave.show()
        self.buttonSave.setText("Сохранить")
        self.buttonSave.clicked.connect(self.save)

        self.buttonCancel = QPushButton(self.widget)
        self.buttonCancel.show()
        self.buttonCancel.setText("Отмена")
        self.buttonCancel.setStyleSheet(style_close2)

    def save(self):
        if self.nameEdit.text() and self.surnameEdit.text() and self.name2Edit.text() and self.experienceEdit.text() and self.descriptEdit.toPlainText() and self.pathEdit.text():
            self.conn = sqlite3.connect(r'data_ad.db')
            self.cur = self.conn.cursor()
            name_ = f'{self.user[0]}{self.user[1]}'
            tab = f"""CREATE TABLE IF NOT EXISTS {name_}(
                               id INT PRIMARY KEY,
                               name1 TEXT,
                               name2 TEXT,
                               name3 TEXT,
                               experience TEXT,
                               descript TEXT,
                               img BLOB);
                            """
            self.cur.execute(tab)
            tab = f"SELECT * FROM {name_};"
            self.cur.execute(tab)
            id_ = len(self.cur.fetchall())
            value = (id_,
                     self.nameEdit.text(),
                     self.surnameEdit.text(),
                     self.name2Edit.text(),
                     self.experienceEdit.text(),
                     self.descriptEdit.toPlainText(),
                     convert_to_binary_data(self.pathEdit.text()))
            tab = f"INSERT INTO {name_} VALUES(?, ?, ?, ?, ?, ?, ?);"
            self.cur.execute(tab, value)
            self.conn.commit()

            self.server.ftp_send("data_ad.db")

    def set_user(self, user):
        self.user = user

    def resize_event(self):
        self.widget.resize(self.width() - 100, self.height() - 100)
        self.widget.move(self.width() // 2 - self.widget.width() // 2, self.height() // 2 - self.widget.height() // 2)
        self.nameEdit.resize(self.widget.width(), 80)
        self.surnameEdit.resize(self.widget.width(), 80)
        self.surnameEdit.move(0, self.nameEdit.height() + self.nameEdit.y())
        self.name2Edit.resize(self.widget.width(), 80)
        self.name2Edit.move(0, self.surnameEdit.height() + self.surnameEdit.y())
        self.experienceEdit.resize(self.widget.width(), 80)
        self.experienceEdit.move(0, self.name2Edit.height() + self.name2Edit.y())
        self.descriptEdit.resize(self.widget.width(), 240)
        self.descriptEdit.move(0, self.experienceEdit.height() + self.experienceEdit.y())
        self.pathEdit.resize(self.widget.width() - 150, 80)
        self.pathEdit.move(0, self.descriptEdit.height() + self.descriptEdit.y())
        self.buttonPath.resize(150, 80)
        self.buttonPath.move(self.widget.width() - 160, self.descriptEdit.height() + self.descriptEdit.y())
        self.buttonSave.resize(200, 80)
        self.buttonSave.move(10, self.pathEdit.height() + self.pathEdit.y())
        self.buttonCancel.resize(200, 80)
        self.buttonCancel.move(210, self.pathEdit.height() + self.pathEdit.y())


class AppWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(base_style)
        self.server = Server()

        self.widget_login = WidgetLogin(self)
        self.widget_login.button_log.clicked.connect(self.log)
        self.widget_form = WidgetForm(self)
        self.widget_admin = AdminWidget(self)

        self.widget_login.show()
        self.widget_form.hide()
        self.widget_admin.hide()
        self.update()

    def log(self):
        self.server.ftp_load("data_ad.db")
        check = self.widget_login.check_login()
        if check == 1:
            ex.setWindowTitle("Панель администратора")
            ex.resize(1300, 900)
            self.widget_login.hide()
            self.widget_admin.show()
        elif check:
            ex.setWindowTitle(f"Заполнение формы - {check[0]}")
            ex.resize(1000, 900)
            self.widget_login.hide()
            self.widget_form.show()
            self.widget_form.buttonCancel.clicked.connect(self.active_log)
            self.widget_form.set_user(check)

    def active_log(self):
        self.widget_login.nameEdit.setText(""), self.widget_login.passwordEdit.setText("")
        self.widget_login.show()
        self.widget_form.hide()
        self.widget_admin.hide()

    def update(self):
        pass

    def resizeEvent(self, event):
        self.widget_form.resize(self.size())
        self.widget_login.resize(self.size())
        self.widget_admin.resize(self.size())

        self.widget_login.resize_event()
        self.widget_form.resize_event()
        self.widget_admin.resize_event()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FramelessWindow()
    ex.setWindowTitle("Вход")
    ex.resize(1000, 700)
    ex.setIconSize(60)
    ex.show()
    ex.setWidget(AppWidget())
    ex.setWindowIcon(QIcon("icon_main.ico"))

    sys.exit(app.exec_())