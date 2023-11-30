from MotorSimulation import MotorSimulation
from PIDController import PIDController
import keyboard

class RobotControl:
    def __init__(self, motor1: MotorSimulation, motor2: MotorSimulation):
        self.motor1 = motor1
        self.motor2 = motor2

        # PID controllers for motor1
        self.pid_controller_1 = PIDController(motor1, kp=0.005, ki=0.0003, kd=0.0)

        # PID controllers for motor2
        self.pid_controller_2 = PIDController(motor2, kp=0.0005, ki=0.00003, kd=0.0)

        # State machine variables
        self.state = 'startPosition'

    def set_state(self, new_state):
        self.state = new_state

    def refresh(self, elapsed_time):
        # Update PID controllers based on the current state
        print(self.state)
        if self.state == 'startPosition':
            self._state_startPosition()
        elif self.state == 'intaking':
            self._state_intaking()
        elif self.state == 'extendingUpperArm':
            self._state_extendingUpperArm()
        elif self.state == 'stowingLowerArm':
            self._state_stowingLowerArm()
        elif self.state == 'safePosition':
            self._state_safePosition()
        elif self.state == 'scoreMid':
            self._state_scoreMid()
        elif self.state == 'scoreHigh':
            self._state_scoreHigh()
        elif self.state == 'unstowMid':
            self._state_unstowMid()
        elif self.state == 'unstowHigh':
            self._state_unstowHigh()
        elif self.state == 'returnUpperArm':
            self._state_returnUpperArm()

        # Control motors
        self.pid_controller_1.control(elapsed_time)
        self.pid_controller_2.control(elapsed_time)

    def _state_startPosition(self):
        self.pid_controller_1.set_setpoint(0)
        self.pid_controller_2.set_setpoint(90)
        if keyboard.is_pressed("i"):
          self.set_state('intaking')

    def _state_intaking(self):
        self.pid_controller_1.set_setpoint(0)
        self.pid_controller_2.set_setpoint(0)
        if keyboard.is_pressed("a"):
          self.set_state('extendingUpperArm')

    def _state_extendingUpperArm(self):
        self.pid_controller_1.set_setpoint(80)
        self.pid_controller_2.set_setpoint(0)
        if self.motor1.position > 30:
          self.set_state('stowingLowerArm')

    def _state_stowingLowerArm(self):
        self.pid_controller_1.set_setpoint(80)
        self.pid_controller_2.set_setpoint(160)
        if self.motor2.position > 90:
          self.set_state('safePosition')

    def _state_safePosition(self):
        self.pid_controller_1.set_setpoint(10)
        self.pid_controller_2.set_setpoint(160)
        if keyboard.is_pressed("m"):
          self.set_state('scoreMid')
        elif keyboard.is_pressed("h"):
          self.set_state('scoreHigh')

    def _state_scoreMid(self):
        self.pid_controller_1.set_setpoint(70)
        self.pid_controller_2.set_setpoint(160)
        if keyboard.is_pressed("h"):
          self.set_state('scoreHigh')
        elif keyboard.is_pressed("d"):
          self.set_state('unstowMid')

    def _state_scoreHigh(self):
        self.pid_controller_1.set_setpoint(110)
        self.pid_controller_2.set_setpoint(160)
        if keyboard.is_pressed("m"):
          self.set_state('scoreMid')
        elif keyboard.is_pressed("d"):
          self.set_state('unstowHigh')

    def _state_unstowMid(self):
        self.pid_controller_1.set_setpoint(70)
        self.pid_controller_2.set_setpoint(0)
        if self.motor2.position < 70:
          self.set_state('returnUpperArm')

    def _state_unstowHigh(self):
        self.pid_controller_1.set_setpoint(110)
        self.pid_controller_2.set_setpoint(0)
        if self.motor2.position < 120:
          self.set_state('returnUpperArm')

    def _state_returnUpperArm(self):
        self.pid_controller_1.set_setpoint(0)
        self.pid_controller_2.set_setpoint(0)
        if self.motor2.position < 60:
          self.set_state('startPosition')