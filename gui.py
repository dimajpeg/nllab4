from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class FuzzySystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Fuzzy System Control')

        layout = QVBoxLayout()

        self.temp_input = QLineEdit(self)
        self.humidity_input = QLineEdit(self)
        self.result_label = QLabel('Fan Speed: ', self)

        self.run_button = QPushButton('Run Simulation', self)
        self.run_button.clicked.connect(self.run_simulation)

        layout.addWidget(self.temp_input)
        layout.addWidget(self.humidity_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.show()

    def run_simulation(self):
        # Створення змінних та функцій належності
        temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
        humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
        fan_speed = ctrl.Consequent(np.arange(0, 11, 1), 'fan_speed')

        temperature['low'] = fuzz.trapmf(temperature.universe, [0, 0, 15, 25])
        temperature['medium'] = fuzz.trimf(temperature.universe, [20, 25, 30])
        temperature['high'] = fuzz.trapmf(temperature.universe, [25, 35, 40, 40])

        humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 50])
        humidity['medium'] = fuzz.trimf(humidity.universe, [40, 50, 60])
        humidity['high'] = fuzz.trimf(humidity.universe, [50, 100, 100])

        fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 5])
        fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [4, 5, 6])
        fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [6, 10, 10])


        rule1 = ctrl.Rule(temperature['low'] & humidity['low'], fan_speed['slow'])
        rule2 = ctrl.Rule(temperature['low'] & humidity['medium'], fan_speed['medium'])
        rule3 = ctrl.Rule(temperature['low'] & humidity['high'], fan_speed['fast'])
        rule4 = ctrl.Rule(temperature['medium'] & humidity['low'], fan_speed['medium'])
        rule5 = ctrl.Rule(temperature['medium'] & humidity['medium'], fan_speed['medium'])
        rule6 = ctrl.Rule(temperature['medium'] & humidity['high'], fan_speed['fast'])
        rule7 = ctrl.Rule(temperature['high'] & humidity['low'], fan_speed['fast'])
        rule8 = ctrl.Rule(temperature['high'] & humidity['medium'], fan_speed['fast'])
        rule9 = ctrl.Rule(temperature['high'] & humidity['high'], fan_speed['fast'])


        fan_speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        fan_speed_sim = ctrl.ControlSystemSimulation(fan_speed_ctrl)

        temperature_value = float(self.temp_input.text())
        humidity_value = float(self.humidity_input.text())

        fan_speed_sim.input['temperature'] = temperature_value
        fan_speed_sim.input['humidity'] = humidity_value
        fan_speed_sim.compute()

        # Виведення результату
        self.result_label.setText(f"Fan Speed: {fan_speed_sim.output['fan_speed']}")


if __name__ == '__main__':
    app = QApplication([])
    ex = FuzzySystemGUI()
    app.exec_()
