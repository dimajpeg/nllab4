import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fuzzy_system_model import get_fan_speed_simulation


def plot_3d_surface():
    # Создание сетки для температуры и влажности
    temp_range = np.arange(0, 101, 1)
    humidity_range = np.arange(0, 101, 1)
    Temp, Humidity = np.meshgrid(temp_range, humidity_range)


    fan_speed_sim = get_fan_speed_simulation()


    FanSpeed = np.zeros_like(Temp)


    for i in range(Temp.shape[0]):
        for j in range(Humidity.shape[1]):
            fan_speed_sim.input['temperature'] = Temp[i, j]
            fan_speed_sim.input['humidity'] = Humidity[i, j]
            fan_speed_sim.compute()
            FanSpeed[i, j] = fan_speed_sim.output['fan_speed']


    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Temp, Humidity, FanSpeed, cmap='viridis')


    ax.set_xlabel('Temperature')
    ax.set_ylabel('Humidity')
    ax.set_zlabel('Fan Speed')
    ax.set_title('3D Surface Plot of Fan Speed')

    plt.show()

if __name__ == '__main__':
    plot_3d_surface()
