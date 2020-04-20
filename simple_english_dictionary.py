from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QCompleter, QTextEdit, QVBoxLayout, QHBoxLayout, QApplication, QMessageBox, QComboBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect
from difflib import get_close_matches
import json
import sys

data = json.load(open("data.json"))

class Window(QDialog):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Simple English Dictionary")
        self.setWindowIcon(QIcon("dict.png"))
        self.setGeometry(350,150,550,350)
        self.setStyleSheet("background-color:#f2f2f2")

        self.ui_window()

        self.show()

    def ui_window(self):

        # completer
        keys = data.keys()
        comp = QCompleter(keys)

        # label
        word_count = QLabel(f"There is {len(keys)} word!")
        label = QLabel("Enter The Word:")
        label.setFont(QFont("Arial",15))
        self.label2 = QLabel()
        self.label2.setFont(QFont("Arial",13))
        self.label2.setStyleSheet("color:#E84682")

        # line erea
        self.line_edit = QLineEdit()
        self.line_edit.setFont(QFont("Arial",13))
        self.line_edit.returnPressed.connect(self.translate_word)
        self.line_edit.setCompleter(comp)

        # text erea
        self.text_erea = QTextEdit()
        self.text_erea.setFont(QFont("Arial",13))

        # buttons
        translate = QPushButton("Translate")
        translate.setFont(QFont("Arial",13))
        translate.setStyleSheet("background-color:#27FF4F")
        translate.clicked.connect(self.translate_word)

        exit = QPushButton("Exit")
        exit.setFont(QFont("Arial",13))
        exit.setStyleSheet("background-color:#FF0000")
        exit.clicked.connect(sys.exit)

        hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addWidget(label)
        hbox.addWidget(self.line_edit)
        hbox.addWidget(translate)
        vbox.addWidget(word_count)
        vbox.addLayout(hbox)
        vbox.addLayout(self.hbox2)
        vbox.addWidget(self.text_erea)
        vbox.addWidget(exit)

        self.setLayout(vbox)

    def translate_word(self):
        if self.line_edit.text():
            try:
                self.cbox.deleteLater()
            except:
                pass
            try:
                self.set.deleteLater()
            except:
                pass
            self.label2.clear()
            self.text_erea.clear()
            word = self.line_edit.text()
            match = str()
            try:
                for d in data[word]:
                    match += f"{d}\n"+"-"*80+"\n"
                self.label2.setText(word)
                self.text_erea.setText(match)
            except KeyError:
                matches = get_close_matches(word, data.keys())
                self.cbox = QComboBox()
                self.cbox.setGeometry(QRect(40, 40, 491, 31))
                self.cbox.setFont(QFont("Arial",12))
                self.cbox.setObjectName("ComboBox")
                self.set = QPushButton("Apply")
                self.set.setFont(QFont("Arial",11))
                self.set.setStyleSheet("background-color:#00FFFF")
                self.set.clicked.connect(self.set_word)
                if matches:
                    self.label2.setText(f"Did you mean this")
                    for m in matches:
                        self.cbox.addItem(m)
                    self.hbox2.addWidget(self.label2)
                    self.hbox2.addWidget(self.cbox)
                    self.hbox2.addWidget(self.set)
                else:
                    QMessageBox.about(self, "Translate", "Sorry, This word doesn't exist!")

            self.line_edit.clear()

    def set_word(self):

        word = self.cbox.currentText()
        match = str()
        for d in data[word]:
            match += f"{d}\n"+"-"*80+"\n"
        self.label2.setText(word)
        self.text_erea.setText(match)

        self.line_edit.clear()
        self.cbox.deleteLater()
        self.set.deleteLater()

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec())
