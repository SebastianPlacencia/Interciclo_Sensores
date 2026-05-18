#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MissionPlanner(Node):
    def __init__(self):
        super().__init__('mission_planner')

        # Publicador de comandos
        self.cmd_pub = self.create_publisher(String, '/tello_cmd', 10)

        # Secuencia exacta de la misión (el circuito predefinido)
        self.mission_sequence = [
            'takeoff',
            'up 50',        # Sube 50 cm
            'forward 50',   # Avanza 50 cm
            'back 50',      # Retrocede 50 cm al punto de inicio
            'land'          # Aterriza
        ]
        self.current_step = 0

        # Ejecuta un paso de la misión cada 6 segundos
        self.timer = self.create_timer(6.0, self.execute_mission)
        self.get_logger().info('Planificador de misión iniciado. ¡Despegue en 6 segundos!')

    def execute_mission(self):
        if self.current_step < len(self.mission_sequence):
            # Obtener el comando actual
            cmd = self.mission_sequence[self.current_step]

            # Publicarlo en ROS2
            msg = String()
            msg.data = cmd
            self.cmd_pub.publish(msg)
            self.get_logger().info(f'-> Ejecutando: {cmd}')

            # Avanzar al siguiente paso
            self.current_step += 1
        else:
            self.get_logger().info('¡Misión completada con éxito!')
            self.timer.cancel() # Detenemos el temporizador

def main(args=None):
    rclpy.init(args=args)
    node = MissionPlanner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
