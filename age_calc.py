import sys

from PyQt6.QtWidgets import QApplication, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton

from datetime import datetime


class AgeCalculator(QWidget):
    """QWidget helps create windows for functions"""
    def __init__(self):
        """The init method of parent class needed to be called before the init we
        overwrote was run so super.__init__() is called"""
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        # Create widgets
        name_label = QLabel("Name: ")
        self.name_line_edit = QLineEdit()

        dob_label = QLabel("Date of Birth (mm/dd/yyyy): ")
        self.dob_line_edit = QLineEdit()

        calculate_button = QPushButton("Submit")
        calculate_button.clicked.connect(self.calculate_age)
        # Label to display output
        self.output_label = QLabel("")

        # Add widgets to grid
        """grid.addWidget(label, row, column)"""
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(dob_label, 1, 0)
        grid.addWidget(self.dob_line_edit, 1, 1)
        """grid.addWidget(label, row, column, width of row to extend to, width of column to extend to)"""
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.dob_line_edit.text()
        year_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y").date().year
        age = current_year - year_of_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old")


# sys helps gives the file in the form of list[str] to QApplication
app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
