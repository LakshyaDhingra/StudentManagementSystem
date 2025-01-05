import sys

from PyQt6.QtWidgets import QApplication, \
    QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QComboBox


class SpeedCalculator(QWidget):
    """QWidget helps create windows for functions"""
    def __init__(self):
        """The init method of parent class needed to be called before the init we
        overwrote was run so super.__init__() is called"""
        super().__init__()
        self.setWindowTitle("Speed Calculator")
        grid = QGridLayout()

        # Create widgets
        distance_label = QLabel("Distance: ")
        self.distance_line_edit = QLineEdit()

        time_label = QLabel("Time (hours): ")
        self.time_line_edit = QLineEdit()

        self.combo = QComboBox()
        self.combo.addItems(['Metric (km)', 'Imperial (miles)'])

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_speed)
        # Label to display output
        self.output_label = QLabel("")

        # Add widgets to grid
        """grid.addWidget(label, row, column)"""
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.combo, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        """grid.addWidget(label, row, column, width of row to extend to, width of column to extend to)"""
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_speed(self):
        speed = 0
        unit = ""
        distance = float(self.distance_line_edit.text())
        hours = float(self.time_line_edit.text())

        if self.combo.currentText() == 'Metric (km)':
            unit = "km/"
            speed = distance/hours

        if self.combo.currentText() == 'Imperial (miles)':
            unit = "mp"
            speed = (distance / hours) * 0.621371
            # rounding up number
            speed = speed.__round__(2)

        self.output_label.setText(f"Average speed: {speed} {unit}h")


# sys helps gives the file in the form of list[str] to QApplication
app = QApplication(sys.argv)
speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())
