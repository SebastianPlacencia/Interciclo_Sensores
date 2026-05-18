#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32

class TelemetryMonitor(Node):
    def __init__(self):
        super().__init__('telemetry_monitor')
        # Suscriptores a los tópicos relevantes
        self.battery_sub = self.create_subscription(Int32, '/battery_status', self.battery_callback, 10)
        self.telemetry_sub = self.create_subscription(String, '/telemetry', self.telemetry_callback, 10)
        self.get_logger().info('Monitor de Telemetría Iniciado')

    def battery_callback(self, msg):
        self.get_logger().info(f'[BATERÍA]: {msg.data}%')

    def telemetry_callback(self, msg):
        self.get_logger().info(f'[DATOS DE VUELO]: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
