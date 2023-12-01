from MotorSimulation import MotorSimulation
from RealTimeGraph import RealTimeGraph
from RobotVisualization import RobotVisualization
from RobotControl import RobotControl
import time


motor1 = MotorSimulation(max_torque=100, max_speed=100)
motor2 = MotorSimulation(max_torque=1000, max_speed=1000)
motor2.position = 90

def get_motor_1_speed():
  return motor1.speed

def get_motor_1_position():
  return motor1.position

def get_motor_2_speed():
  return motor2.speed

def get_motor_2_position():
  return motor2.position

startTime = time.time()

def simulation():
  elapsedTime = time.time() - startTime
  motor1.refresh(elapsedTime)
  if motor1.position <= 90:
    motor1.set_load(motor1.position/9)
  elif motor1.position <= 270:
    motor1.set_load((180 - motor1.position)/9)
  else:
    motor1.set_load((motor1.position - 360)/9)
  if motor1.position > 360:
    motor1.position = motor1.position - 360
  elif motor1.position < 0:
    motor1.position = motor1.position + 360
  motor2.refresh(elapsedTime)
  if elapsedTime < 15:
    motor1.set_power_input(1)
  elif elapsedTime < 25:
    motor1.set_power_input(0)
  else:
    motor1.set_power_input(-1)
  print(f"Time: {elapsedTime}, Torque: {motor1.torque}, Speed: {motor1.speed}, Position: {motor1.position}")
  return elapsedTime

motor_1_speed_graph = RealTimeGraph(max_value=motor1.max_speed, xlabel='Time', ylabel='Speed 1', duration=50)
motor_1_speed_graph.simulation = simulation
motor_1_speed_graph.get_current_value = get_motor_1_speed
motor_1_position_graph = RealTimeGraph(max_value=100, xlabel='Time', ylabel='Position 1', duration=50)
motor_1_position_graph.simulation = simulation
motor_1_position_graph.get_current_value = get_motor_1_position

robot_visualization = RobotVisualization(interval=50, duration=10)
robot_visualization.get_angle_1 = get_motor_1_position
robot_visualization.get_angle_2 = get_motor_2_position


motor_1_position_graph.show()