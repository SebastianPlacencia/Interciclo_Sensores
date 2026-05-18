#!/usr/bin/env python3
import os
# Configuraciones obligatorias para evitar conflictos de renderizado según el documento
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1" # render por CPU
os.environ["XDG_RUNTIME_DIR"] = "/tmp"

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VideoViewer(Node):
    def __init__(self):
        super().__init__('video_viewer')
        # Se suscribe al tópico que transmite las imágenes
        self.subscription = self.create_subscription(
            Image,
            '/tello_image',
            self.image_callback,
            10)
        self.br = CvBridge()
        self.get_logger().info('Nodo video_viewer inicializado.')

    def image_callback(self, msg):
        try:
            # Convierte la imagen de ROS2 a un formato de OpenCV
            cv_image = self.br.imgmsg_to_cv2(msg, "bgr8")
            # Muestra el video en una ventana
            cv2.imshow("Video del Dron Tello", cv_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f'Error al procesar la imagen: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = VideoViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
