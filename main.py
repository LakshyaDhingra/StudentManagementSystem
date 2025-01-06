import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, \
    QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QGridLayout, QLabel, \
    QLineEdit, QPushButton, QVBoxLayout, QComboBox

import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        search_action.setMenuRole(QAction.MenuRole.NoRole)

    # Creating table using QTableWidget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile No."))
        # Remove duplicate index column
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create combo box widget
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Physics", "Chemistry"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile_no = QLineEdit()
        self.mobile_no.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile_no)

        # Add register button
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.add_student)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_no.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        student_database.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add submit button
        submit_button = QPushButton("Search")
        submit_button.clicked.connect(self.search_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))
        rows = list(result)
        items = student_database.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            student_database.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
student_database = MainWindow()
student_database.show()
student_database.load_data()
sys.exit(app.exec())
