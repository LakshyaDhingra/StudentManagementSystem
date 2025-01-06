import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, \
    QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QLineEdit, QPushButton, QVBoxLayout, \
    QComboBox, QToolBar, QStatusBar

import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # Minimum size of window changed
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
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

    # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

    # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.table.cellClicked.connect(self.cell_clicked)


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

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
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


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        index = student_database.table.currentRow()
        student_name = student_database.table.item(index, 1).text()

        self.student_id = student_database.table.item(index, 0).text()
        # Create widgets
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create combo box widget
        course_name = student_database.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Physics", "Chemistry"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile_no = student_database.table.item(index, 3).text()
        self.mobile_no = QLineEdit(mobile_no)
        self.mobile_no.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile_no)

        # Add register button
        register_button = QPushButton("Edit")
        register_button.clicked.connect(self.edit_student)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def edit_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_no.text()
        s_id = self.student_id
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, "
                       "mobile = ? WHERE ID = ?", (name, course, mobile, s_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh data
        student_database.load_data()


class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
student_database = MainWindow()
student_database.show()
student_database.load_data()
sys.exit(app.exec())
