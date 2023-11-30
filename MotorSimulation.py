class MotorSimulation:
    def __init__(self, max_torque, max_speed):
        self.max_torque = max_torque
        self.max_speed = max_speed
        self.load = 0  # Initial load
        self.speed = 0
        self.position = 0
        self.power_input = 0
        self.last_elapsed_time = 0  # Keep track of the last elapsed time
        self.torque = 0

    def set_load(self, load):
        self.load = load

    def set_power_input(self, power):
        self.power_input = max(-1, min(1, power))

    def refresh(self, elapsed_time):
        time_difference = elapsed_time - self.last_elapsed_time
    
        torque_multiplier = self.power_input - (self.speed / self.max_speed)
        if torque_multiplier > 1:
            torque = self.max_torque
        elif torque_multiplier < -1:
            torque = -1 * self.max_torque
        else:
            torque = self.max_torque * torque_multiplier
        resulting_torque = torque - self.load

        # Update position and speed based on torque
        acceleration = resulting_torque  # Assuming mass = 1 for simplicity
        self.speed += acceleration * time_difference
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < (-1 * self.max_speed):
            self.speed = -1 * self.max_speed
        self.position += self.speed * time_difference

        self.last_elapsed_time = elapsed_time  # Update the last elapsed time
        self.torque = resulting_torque

        return self.torque, self.speed, self.position