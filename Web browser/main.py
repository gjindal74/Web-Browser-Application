import sys
import os
import json

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QTabBar, QFrame, QStackedLayout, QTabWidget, QShortcut, QKeySequenceEdit)

from PyQt5.QtGui import QIcon, QImage, QKeySequence
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()

class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        self.CreateApp()
        self.setWindowIcon(QIcon("logo.png"))
        self.resize(1366, 768)

    def CreateApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create Tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)
        self.tabbar.setCurrentIndex(0)
        self.shortcutNewTab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcutNewTab.activated.connect(self.AddTab)
        self.shortcutReload = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcutReload.activated.connect(self.Reload)

        # Keep tab track
        self.tabcount = 0
        self.tabs = []

        # Create AddressBar
        self.ToolBar = QWidget()
        self.ToolBar.setObjectName("ToolBar");
        self.ToolBarlayout = QHBoxLayout()
        self.addressbar = AddressBar()

        self.ToolBar.setLayout(self.ToolBarlayout)
        self.ToolBarlayout.addWidget(self.addressbar)

        # New tab button
        self.AddTabButton = QPushButton("+")
        self.addressbar.returnPressed.connect(self.BrowseTo)
        self.AddTabButton.clicked.connect(self.AddTab)


        self.BackButton = QPushButton("<")
        self.BackButton.clicked.connect(self.GoBack)
        self.ForwardButton = QPushButton(">")
        self.ForwardButton.clicked.connect(self.GoForward)

        self.ReloadButton = QPushButton("RELOAD")
        self.ReloadButton.clicked.connect(self.Reload)

        self.ToolBarlayout.addWidget(self.BackButton)
        self.ToolBarlayout.addWidget(self.ForwardButton)
        self.ToolBarlayout.addWidget(self.ReloadButton)

        self.ToolBarlayout.addWidget(self.AddTabButton)

        # Set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.ToolBar)
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)
        self.AddTab()
        self.show()

    def CloseTab(self, i):
        self.tabbar.removeTab(i)
    def AddTab(self):
        i = self.tabcount

        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()

        self.tabs[i].setObjectName("tab" + str(i))

        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("https://www.google.com/"))
        self.tabs[i].content.titleChanged.connect(lambda title, i=i: self.SetTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda icon, i=i: self.SetTabContent(i, "icon"))

        # Add webview
        self.tabs[i].layout.addWidget(self.tabs[i].content)
        self.tabs[i].setLayout(self.tabs[i].layout)

        # Add tab to top level stackedwidget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        # Set the tab to the top of screen
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {"object": "tab" + str(i), "initial": i})
        self.tabbar.setCurrentIndex(i)

        self.tabcount += 1

    def SwitchTab(self, i):
        tab_data = self.tabbar.tabData(i)
        tab_object_name = tab_data["object"]
        tab_content = self.findChild(QWidget, tab_object_name)
        self.container.layout.setCurrentWidget(tab_content)

    def BrowseTo(self):
        text = self.addressbar.text()

        i = self.tabbar.currentIndex()
        tab_data = self.tabbar.tabData(i)
        tab_object_name = tab_data["object"]
        wv = self.findChild(QWidget, tab_object_name).content

        if "http" not in text:
            if "." not in text:
                url = "https://www.google.co.in/search?q=" + text
            else:
                url = "http://" + text
        else:
            url = text
        wv.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, type):
        tab_data = self.tabbar.tabData(i)
        tab_object_name = tab_data["object"]
        if type == "title":
            new_title = self.findChild(QWidget, tab_object_name).content.title()
            self.tabbar.setTabText(i, new_title)
        elif type == "icon":
            new_icon = self.findChild(QWidget, tab_object_name).content.icon()
            self.tabbar.setTabIcon(i, new_icon)

    def GoBack(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.back()

    def Reload(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.reload()


    def GoForward(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.forward()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "667"
    window = App()
    with open("style.css", "r") as style:
        app.setStyleSheet(style.read())


    sys.exit(app.exec_())
