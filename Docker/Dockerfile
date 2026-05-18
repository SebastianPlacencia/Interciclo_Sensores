# Usamos ROS2 Humble como base (puedes cambiarlo a foxy o iron según tu versión de Ubuntu)
FROM osrf/ros:humble-desktop

# Deshabilitar interacciones durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar el sistema e instalar dependencias básicas y de red
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    iputils-ping \
    net-tools \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias requeridas por el proyecto (OpenCV y cv_bridge)
RUN apt-get update && apt-get install -y \
    ros-humble-cv-bridge \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Crear y establecer el directorio de trabajo (Workspace)
WORKDIR /ros2_ws

# Configurar el entrypoint de ROS2 por defecto
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

CMD ["bash"]
