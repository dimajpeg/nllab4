import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
fan_speed = ctrl.Consequent(np.arange(0, 11, 1), 'fan_speed')

temperature['low'] = fuzz.trapmf(temperature.universe, [0, 0, 20, 30])
temperature['medium'] = fuzz.trimf(temperature.universe, [25, 35, 45])
temperature['high'] = fuzz.trapmf(temperature.universe, [40, 50, 100, 100])

humidity['low'] = fuzz.trapmf(humidity.universe, [0, 0, 20, 40])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trapmf(humidity.universe, [60, 80, 100, 100])


fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 5])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [4, 5, 6])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [5, 10, 10])


rule1 = ctrl.Rule(temperature['low'] & humidity['low'], fan_speed['low'])
rule2 = ctrl.Rule(temperature['low'] & humidity['medium'], fan_speed['low'])
rule3 = ctrl.Rule(temperature['low'] & humidity['high'], fan_speed['medium'])

rule4 = ctrl.Rule(temperature['medium'] & humidity['low'], fan_speed['medium'])
rule5 = ctrl.Rule(temperature['medium'] & humidity['medium'], fan_speed['medium'])
rule6 = ctrl.Rule(temperature['medium'] & humidity['high'], fan_speed['high'])

rule7 = ctrl.Rule(temperature['high'] & humidity['low'], fan_speed['high'])
rule8 = ctrl.Rule(temperature['high'] & humidity['medium'], fan_speed['high'])
rule9 = ctrl.Rule(temperature['high'] & humidity['high'], fan_speed['high'])


fan_speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
fan_speed_sim = ctrl.ControlSystemSimulation(fan_speed_ctrl)


def get_fan_speed_simulation():
    return fan_speed_sim
