import platform, socket, re, uuid, json, psutil, logging
import os
from PyQt5.QtWidgets import QGraphicsColorizeEffect
import subprocess as sp
import sys
import sqlite3
from datetime import datetime
import subprocess
from os import listdir, path, getcwd
from PIL import Image
from PyQt5 import uic, QtGui  # Импортируем uic
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize, QTimer, QRect
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem, QWidget, QFileDialog, \
    QGraphicsOpacityEffect, QLabel, QTextEdit, QLineEdit, QPushButton, QFrame
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from bs4 import BeautifulSoup
import requests
from time import gmtime, strftime
import ftplib


class Server:
    USER = "cw64765"
    PASS = "x7ORTZ8MSrNO"
    PORT = 21
    SERVER = 'vh312.timeweb.ru'  # use FTP server name here

    def __init__(self):
        self.ftp_server = None
        self.connect()

    def connect(self):
        self.ftp_server = ftplib.FTP()
        self.ftp_server.connect(self.SERVER, self.PORT)
        self.ftp_server.login(self.USER, self.PASS)

    def ftp_load(self, filename):
        with open(filename, "wb") as file:
            self.ftp_server.retrbinary(f"RETR {filename}", file.write)

    def ftp_send(self, filename):
        with open(filename, "rb") as file:
            self.ftp_server.storbinary(f"STOR {filename}", file)


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


class User:
    def __init__(self, name, password, date):
        self.name = name
        self.password = password
        self.date = date
        self.characteristic = {
            "text": {
                "Имя": "none",
                "Фамилия": "none",
                "Отчество": "none",
                "Опыт работы": "none",
                "Описание": "none",
            },
            "img": {
                "Изображение": "none",
            }

        }

    def update_characteristic(self):
        try:
            self.conn = sqlite3.connect(r'data_ad.db')
            self.cur = self.conn.cursor()
            tab = f"SELECT * FROM {self.name}{self.password};"
            self.cur.execute(tab)
            results = self.cur.fetchall()
            self.conn.commit()
            path = f'user_{self.name}.png'
            write_to_file(results[0][6], path)

            self.characteristic['text']["Имя"] = results[0][1]
            self.characteristic['text']["Фамилия"] = results[0][2]
            self.characteristic['text']["Отчество"] = results[0][3]
            self.characteristic['text']["Опыт работы"] = results[0][4]
            self.characteristic['text']["Описание"] = results[0][5]
            self.characteristic['img']["Изображение"] = path
            self.cur.close()
        except Exception as ex:
            pass


st = """
        font-size: 50px; margin: 20px 20px;
        """

base_style = """
    QPushButton{border: 3px solid green; border-radius: 20px; margin: 10px 10px; background-color: rgb(0,0,0,0)}
    QPushButton:hover{border: none; color: rgb(0,0,0); background-color: rgb(83,184,35, 190);}
    QHeaderView::section { background-color: rgb(83,184,35); color: rgb(0,0,0); border: 2px solid rgb(0,0,0) }
    QTreeView {border: 2px solid rgb(0,0,0)}
    QLineEdit {border:3px solid rgb(83,184,35); color: rgb(83,184,35); border-radius: 20px;}

    QListWidget::item:pressed,QListWidget::item:selected{background-color:rgb(83,184,35); color: rgb(0,0,0)}
    QTableWidget::item:pressed,QTableWidget::item:selected{border:3px solid rgb(83,184,35); border-radius: 10px;color: rgb(83,184,35)}

    QTreeView::item:pressed,QTreeView::item:selected{background-color:rgb(83,184,35); color: rgb(0,0,0)}
    QTableWidget{alternate-background-color: rgba(15,15,15);}
    QWidget {
        background-color: rgb(0,0,0);
        color: #fff;
    }
    QWidget{color: rgb(83,184,35);font-size: 30px;font-family: 'CatV 6x12 9'}
"""

# rgb(83,184,35)
style_but = '''
        QPushButton{border: 2px solid rgb(83,184,35); background-color: rgb(0,0,0,0)}
        QPushButton:hover{border: none; color: rgb(0,0,0); background-color: rgb(83,184,35, 190);}
        '''
style_but2 = '''
        QPushButton{border: none; background-color: rgb(83,184,35,0)}
        QPushButton:hover{border: none; color: rgb(83,184,35); background-color: rgb(0,0,0);}
        '''

errorFormat = '<font style="color:red">{}</font>'
warningFormat = '<font color="orange">{}</font>'
validFormat = '<font color="green">{}</font>'
darkgreenFormat = '<font color="#80CF0C";">{}</font>'
whiteFormat = '<font style="color:#A1A1A1">{}</font>'
titleFormat = '<font style="color:#010101; background-color: #1F4D3C">{}</font>'
style_close = """QPushButton{border: none; background-color: rgb(83,184,35,0)}
        QPushButton:hover{background-color: rgb(184,0,0); color: rgb(250,250,250); border: 0px;}"""
style_close2 = """QPushButton{color: red; border: 3px solid rgb(184,0,0); background-color: rgb(83,184,35,0); border-radius: 20px}
        QPushButton:hover{background-color: rgb(184,0,0); color: rgb(250,250,250); border: 0px;}"""
style_add = """QPushButton{color: rgb(124,99,253); border: 3px solid rgb(104,79,243); background-color: rgb(83,184,35,0); border-radius: 20px}
        QPushButton:hover{background-color: rgb(104,79,243); color: rgb(250,250,250); border: 0px;}"""

commands = {
    'cd': ['cd',
           'Переходит по указанной директории'],
    'systeminfo': ['systeminfo',
                   'Системная информация'],
    'clear': ['clear',
              'Очищает консоль'],
    'help': ['help',
             'Выводит все команды'],
    'ls': ['ls',
           'Выводит все файлы и папки в текущей директории'],
    'nano': ['nano',
             'текстовый редактор'],
    'ls.dirs': ['ls.dirs',
                'Выводит только папки в текущей директории'],
    'ls.files': ['ls.files',
                 'Выводит только файлы в текущей директории'],
    'system': ['system',
               'Выполняет системную команду'],
}


class TitleBar(QWidget):

    # Сигнал минимизации окна
    windowMinimumed = pyqtSignal()
    # увеличить максимальный сигнал окна
    windowMaximumed = pyqtSignal()
    # сигнал восстановления окна
    windowNormaled = pyqtSignal()
    # сигнал закрытия окна
    windowClosed = pyqtSignal()
    # Окно мобильных
    windowMoved = pyqtSignal(QPoint)
    # Сигнал Своя Кнопка +++
    signalButtonMy = pyqtSignal()


    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        # Поддержка настройки фона qss
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos     = None
        self.iconSize = 20                       # Размер значка по умолчанию
        self.setStyleSheet("""background-color: rgb(83,184,35); color: rgb(0,0,0)""")
        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(40, 40, 240))
        self.setPalette(palette)

        # макет
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        # значок окна
        self.iconLabel = QLabel(self)
#         self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)

        # название окна
        self.titleLabel = QLabel(self)
        self.titleLabel.setStyleSheet("""background-color: rgb(83,184,35,0); font-size: 30px;font-family: 'CatV 6x12 9'""")
        layout.addWidget(self.titleLabel)

        # Средний телескопический бар
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Использовать шрифты Webdings для отображения значков
        font = self.font() or QFont()
        font.setFamily('Webdings')


        # Своя Кнопка ++++++++++++++++++++++++++
        # self.buttonMy = QPushButton('@', self, clicked=self.showButtonMy, font=font, objectName='buttonMy')
        # layout.addWidget(self.buttonMy)


        # Свернуть кнопку
        self.buttonMinimum = QPushButton('0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        self.buttonMinimum.setStyleSheet(style_but2)
        layout.addWidget(self.buttonMinimum)

        # Кнопка Max / restore
        self.buttonMaximum = QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        self.buttonMaximum.setStyleSheet(style_but2)
        layout.addWidget(self.buttonMaximum)

        # Кнопка закрытия
        self.buttonClose = QPushButton(
            'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        self.buttonClose.setStyleSheet(style_close)
        layout.addWidget(self.buttonClose)

        # начальная высота
        self.setHeight()

    # +++ Вызывается по нажатию кнопки buttonMy
    def showButtonMy(self):
        self.signalButtonMy.emit()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # Максимизировать
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # Восстановить
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=38):
        """ Установка высоты строки заголовка """
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # Задайте размер правой кнопки  ?
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

        # self.buttonMy.setMinimumSize(height, height)
        # self.buttonMy.setMaximumSize(height, height)

    def setTitle(self, title):
        """ Установить заголовок """
        self.titleLabel.setText(title)
        self.titleLabel.setFont(QFont('OCR A Extended', 10))

    def setIcon(self, icon):
        """ настройки значокa """
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """ Установить размер значка """
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        ''' Событие отказов мыши '''
        self.mPos = None
        event.accept()
        self.setStyleSheet("""background-color: rgb(83,184,35); color: rgb(0,0,0)""")

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
            self.setStyleSheet("""background-color: rgb(83,184,135); color: rgb(0,0,0)""")
        event.accept()


# Перечислить верхнюю левую, нижнюю правую и четыре неподвижные точки
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class FramelessWindow(QWidget):

    # Четыре периметра
    Margins = 5

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        self._pressed  = False
        self.Direction = None

        # Фон прозрачный
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Нет границы
        self.setWindowFlag(Qt.FramelessWindowHint)
        # Отслеживание мыши
        self.setMouseTracking(True)

        # макет
        layout = QVBoxLayout(self, spacing=0)
        # Зарезервировать границы для изменения размера окна без полей
        layout.setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)
        # Панель заголовка
        self.titleBar = TitleBar(self)

        layout.addWidget(self.titleBar)

        # слот сигнала
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)

    def setTitleBarHeight(self, height=38):
        """ Установка высоты строки заголовка """
        self.titleBar.setHeight(height)

    def setIconSize(self, size):
        """ Установка размера значка """
        self.titleBar.setIconSize(size)

    def setWidget(self, widget):
        """ Настройте свои собственные элементы управления """
        if hasattr(self, '_widget'):
            return
        self._widget = widget
        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # Максимизировать или полноэкранный режим не допускается
            return
        super(FramelessWindow, self).move(pos)

    def showMaximized(self):
        """ Чтобы максимизировать, удалите верхнюю, нижнюю, левую и правую границы.
            Если вы не удалите его, в пограничной области будут пробелы. """
        super(FramelessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """ Восстановить, сохранить верхнюю и нижнюю левую и правую границы,
            иначе нет границы, которую нельзя отрегулировать """
        super(FramelessWindow, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

    def eventFilter(self, obj, event):
        """ Фильтр событий, используемый для решения мыши в других элементах
            управления и восстановления стандартного стиля мыши """
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(FramelessWindow, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """ Поскольку это полностью прозрачное фоновое окно, жесткая для поиска
            граница с прозрачностью 1 рисуется в событии перерисовывания, чтобы отрегулировать размер окна. """
        super(FramelessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        super(FramelessWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        ''' Событие отказов мыши '''
        super(FramelessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        """ Событие перемещения мыши """
        super(FramelessWindow, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # Верхний левый угол
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # Нижний правый угол
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # верхний правый угол
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # Нижний левый угол
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # Влево
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # Право
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # выше
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # ниже
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def _resizeWidget(self, pos):
        """ Отрегулируйте размер окна """
        if self.Direction == None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:          # Верхний левый угол
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:    # Нижний правый угол
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == RightTop:       # верхний правый угол
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == LeftBottom:     # Нижний левый угол
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == Left:            # Влево
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:           # Право
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == Top:             # выше
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:          # ниже
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return
        self.setGeometry(x, y, w, h)


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.clicked.emit()