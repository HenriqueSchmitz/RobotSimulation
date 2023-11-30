class PIDController:
    def __init__(self, motor, kp, ki, kd):
        self.motor = motor
        self.setpoint = 0  # Default setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error = 0
        self.integral = 0
        self.last_elapsed_time = 0

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def control(self, elapsed_time):
        time_difference = elapsed_time - self.last_elapsed_time
        current_position = self.motor.position
        error = self.setpoint - current_position

        # Proportional term
        p_term = self.kp * error

        # Integral term
        self.integral += error * time_difference
        i_term = self.ki * self.integral

        # Derivative term
        if time_difference > 0:
          d_term = self.kd * (error - self.prev_error) / time_difference
        else:
          d_term = 0

        # Calculate the control signal
        control_signal = p_term + i_term + d_term

        # Set the power input to the motor based on the control signal
        self.motor.set_power_input(control_signal)

        # Update previous error for the next iteration
        self.prev_error = error
        self.last_elapsed_time = elapsed_time

        return control_signal