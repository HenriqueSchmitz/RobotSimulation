import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class RobotVisualization:
    def __init__(self, interval=10, duration=10):
        self.interval = interval  # Interval between updates in milliseconds
        self.duration = duration  # Total duration of the simulation in seconds

        self.fig, self.ax = plt.subplots()
        self.line1, = self.ax.plot([], [], lw=2)
        self.line2, = self.ax.plot([], [], lw=2)
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)

        self.animation = FuncAnimation(self.fig, self.update, init_func=self.init_plot, blit=False)

        self.last_elapsed_time = 0  # Keep track of the last elapsed time

    def init_plot(self):
        self.line1.set_data([], [])
        self.line2.set_data([], [])
        return self.line1, self.line2

    def update(self, frame):
        angle1 = np.deg2rad(self.get_angle_1())
        angle2 = np.deg2rad(self.get_angle_2())

        length1 = 1.5
        length2 = 0.8
        
        x2_origin = -0.7
        y2_origin = -0.7

        x1 = -1 * length1 * np.sin(angle1)  # x-coordinate for line 1
        y1 = 1 - length1 * np.cos(angle1)  # y-coordinate for line 1

        x2 = x2_origin - length2 * np.cos(angle2)  # x-coordinate for line 2
        y2 = y2_origin + length2 * np.sin(angle2)  # y-coordinate for line 2

        self.line1.set_data([0, x1], [1, y1])
        self.line2.set_data([x2_origin, x2], [y2_origin, y2])

        return self.line1, self.line2
    
    def get_angle_1(self):
        # Override this method in a subclass to get the current value at a given time
        raise NotImplementedError("Subclasses must implement get_angle_1 method")
    
    def get_angle_2(self):
        # Override this method in a subclass to get the current value at a given time
        raise NotImplementedError("Subclasses must implement get_angle_2 method")

    def show(self):
        plt.show()