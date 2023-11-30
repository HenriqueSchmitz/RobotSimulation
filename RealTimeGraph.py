import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimeGraph:
    def __init__(self, max_value, interval=10, duration=10, xlabel='Time', ylabel='Value'):
        self.max_value = max_value
        self.interval = interval  # Interval between updates in milliseconds
        self.duration = duration  # Total duration of the simulation in seconds

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_ylim(-max_value, max_value)
        self.ax.set_xlim(0, self.duration)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        self.simulation_function = None

        self.animation = FuncAnimation(self.fig, self.update, init_func=self.init_plot, blit=False)

        self.last_elapsed_time = 0  # Keep track of the last elapsed time
        self.current_time_limit = self.duration  # Initial limit for current time
        self.current_value_limit = max_value  # Initial limit for current value

    def init_plot(self):
        self.line.set_data([], [])
        return self.line,

    def update(self, frame):
        current_time = self.simulation()
        value = self.get_current_value()

        x_data = list(self.line.get_xdata()) + [current_time]
        y_data = list(self.line.get_ydata()) + [value]

        # Adjust x-axis limits to auto-scroll with the graph
        if current_time > self.current_time_limit:
            self.ax.set_xlim(current_time - self.duration, current_time)
            self.current_time_limit = current_time

        # Adjust y-axis limits to auto-scale
        if value > self.current_value_limit or value < -self.current_value_limit:
            self.ax.set_ylim(-max(value, self.max_value), max(value, self.max_value))
            self.current_value_limit = max(value, self.max_value)

        self.line.set_data(x_data, y_data)

        # Autoscale y-axis
        self.ax.relim()
        self.ax.autoscale_view(scalex=False, scaley=True)

        return self.line,

    def simulation(self):
        if self.simulation_function:
            return self.simulation_function(self.last_elapsed_time)

    def set_simulation_function(self, simulation_function):
        self.simulation_function = simulation_function

    def get_current_value(self):
        # Override this method in a subclass to get the current value at a given time
        raise NotImplementedError("Subclasses must implement get_current_value method")

    def show(self):
        plt.show()