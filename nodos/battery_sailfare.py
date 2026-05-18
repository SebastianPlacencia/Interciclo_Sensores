#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String

class BatteryFailsafe(Node):
    def __init__(self):
        super().__init__('battery_failsafe')
        
        # Se suscribe para leer la batería
        self.battery_sub = self.create_subscription(
            Int32, 
            '/battery_status', 
            self.battery_callback, 
            10)
            
        # Publica comandos de control hacia el dron
        self.cmd_pub = self.create_publisher(String, '/tello_cmd', 10)
        
        # Umbral definido por el proyecto
        self.battery_threshold = 30
        self.land_triggered = False
        
        self.get_logger().info('Nodo battery_failsafe iniciado. Vigilando energía...')

    def battery_callback(self, msg):
        battery_level = msg.data
        
        # Lógica de seguridad: si baja del 30% y no ha aterrizado ya
        if battery_level < self.battery_threshold and not self.land_triggered:
            self.get_logger().warn(f'¡ALERTA! Batería crítica ({battery_level}%). Forzando aterrizaje...')
            
            # Crear y enviar el comando de aterrizaje
            land_msg = String()
            land_msg.data = 'land'
            self.cmd_pub.publish(land_msg)
            
            # Bloqueamos para que no envíe el comando mil veces por segundo
            self.land_triggered = True
            
        elif battery_level >= self.battery_threshold:
            # Reseteamos el bloqueo por si cambias la batería del dron
            self.land_triggered = False

def main(args=None):
    rclpy.init(args=args)
    node = BatteryFailsafe()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
