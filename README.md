# Ecosistema de Nodos ROS2 - Control y Seguridad de UAV

Este apartado describe la arquitectura modular distribuida de los nodos del sistema y proporciona la secuencia exacta de comandos de terminal requeridos para la preparación, despliegue y auditoría de la red de comunicaciones.

---

## Catálogo de Nodos del Sistema

La lógica de control y análisis se divide de manera asíncrona en los siguientes scripts extraídos directamente del entorno operativo:

### 1. Capa de Enlace y Telemetría
* **`drone_connect.txt` (Drone Connector):** Actúa como el nodo puente central. Utiliza el SDK de `djitellopy` para traducir las instrucciones de ROS2 en comandos UDP nativos para el dron, publicando simultáneamente el flujo de video crudo y las métricas de los sensores físicos.
* **`telemetry_monitor.txt` (Telemetry Monitor):** Proceso secundario en tierra de monitoreo pasivo. Se suscribe a los canales de datos de vuelo para imprimir el estado de la batería, altura y velocidades en la consola, sirviendo como herramienta de diagnóstico sin añadir sobrecarga.

### 2. Capa de Visión Artificial y Percepción
* **`video_viewer.txt` (Video Viewer):** Suscriptor dedicado a la matriz visual. Emplea la librería `CvBridge` para convertir las estructuras de datos nativas de ROS2 en matrices tridimensionales de OpenCV, renderizando el flujo de video en tiempo real.
* **`object_detecter.txt` (Object Detector):** Núcleo analítico de percepción. Segmenta las imágenes transformándolas al espacio de color HSV para aislar y contabilizar objetivos de color rojo y negro. Monitorea el rendimiento del procesador inyectando dinámicamente la latencia (3.8 ms) y los FPS (16 cuadros por segundo).

### 3. Capa de Control Autónomo y Failsafe
* **`mission_planner.txt` (Mission Planner):** Gestiona el guiado automático mediante una máquina de estados temporizada de forma asíncrona (intervalos de 6 segundos). Despacha secuencialmente el itinerario de vuelo programado (despegue, traslaciones y aterrizaje).
* **`battery_sailfare.txt` (Battery Failsafe):** Nodo supervisor de seguridad con prioridad absoluta. Evalúa los niveles de energía constantemente; ante una lectura inferior al umbral del 30%, intercepta el bus de comandos global, anula la misión autónoma y fuerza un aterrizaje de emergencia inmediato.

### 4. Estación de Control Terrestre (GCS)
* **`guide_controller.txt` (GUI Controller):** Panel gráfico interactivo multihilo desarrollado en `Tkinter`. Diseña advertencias visuales dinámicas (alertas en color rojo), restringe despegues bajo condiciones críticas y compila de manera automatizada reportes técnicos del historial de vuelo en archivos `.txt`.

---

## Guía de Comandos de Terminal (En Orden Ejecutable)

Siga rigurosamente este orden secuencial para preparar el sistema operativo anfitrión, iniciar el contenedor y ejecutar cada uno de los nodos de ROS2.

### Fase 1: Preparación del Entorno Anfitrión (Host)

**1. Habilitar el Servidor Gráfico X11:**
Permite que las ventanas visuales de OpenCV y la interfaz de `Tkinter` generadas dentro del contenedor Docker se rendericen en la pantalla de su máquina física.
```bash
xhost +local:docker
```

### Fase 2: Arranque y Ejecución de Nodos

**2. Iniciar el contenedor de ROS2:**
Inicia el contenedor en segundo plano con los servicios base.
```bash
sudo docker start ros_tello
```

**3. Lanzar el nodo de conexión principal (Drone Connector):**
Abre una terminal interactiva en el contenedor, carga las variables de entorno de ROS2 y ejecuta el nodo que enlaza con el dron.
```bash
sudo docker exec -it ros_tello bash
source /ros2_ws/install/setup.bash && ros2 run uav_project_pkg drone_connector
```

**4. Lanzar el nodo de visión (Object Detector):**
Abre una nueva terminal para procesar el flujo de video y la detección por color de manera simultánea.
```bash
sudo docker exec -it ros_tello bash
source /ros2_ws/install/setup.bash && ros2 run uav_project_pkg object_detector
```

**5. Lanzar la Estación de Control Terrestre (GUI Controller):**
Abre una nueva terminal para levantar la interfaz gráfica y gestionar la misión.
```bash
sudo docker exec -it ros_tello bash
source /ros2_ws/install/setup.bash && ros2 run uav_project_pkg gui_controller
```

### Fase 3: Auditoría y Monitoreo del Sistema

**6. Evaluar la Latencia de Tópicos (Dentro de Docker):**
Abre una terminal interactiva en el contenedor y ejecuta el comando de diagnóstico para verificar el retraso de la red en los mensajes de telemetría.
```bash
sudo docker exec -it ros_tello bash
ros2 topic delay /telemetry
```

**7. Monitorear Consumo de Recursos (Fuera de Docker):**
Desde una terminal en tu entorno Linux nativo (Ubuntu), verifica el consumo de CPU y memoria RAM asignados al ecosistema.
```bash
docker stats uav_drone_container
```
