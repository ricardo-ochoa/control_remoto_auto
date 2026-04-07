# Control Remoto de Auto - oli

## Descripción

Este proyecto implementa un sistema de control remoto para un vehículo autónomo/teleoperado. Utiliza un ESP32 como controlador de bajo nivel para motores y dirección, mientras que scripts en Python permiten la teleoperación desde una computadora. El sistema está diseñado para ser robusto, separando la inteligencia del control en tiempo real.

## Arquitectura

El sistema se divide en dos niveles principales:

- **Nivel de bajo nivel (ESP32):** Maneja el control directo de motores traseros, servo de dirección, lectura de encoders y paros de seguridad.
- **Nivel de alto nivel (Jetson Nano):** Procesa datos de cámara y LiDAR, ejecuta algoritmos de percepción y envía comandos al ESP32.
- **Desarrollo (MacBook):** Utilizada para teleoperación remota durante la fase de desarrollo.

## Componentes

### Hardware
- ESP32 (con módulo WiFi)
- Motores DC para tracción
- Servo para dirección
- Posiblemente encoders y sensores adicionales

### Software
- `testesp32.ino`: Código para ESP32 (Arduino IDE)
- `control_auto.py`: Script de Python para control remoto vía WiFi usando Pygame
- `control_esp.py`: Script de Python para control directo vía puerto serial
- `documentacion_auto.html` y `documentacion_auto.md`: Documentación del proyecto

## Instalación

### Dependencias de Python
Asegúrate de tener Python 3.x instalado. Instala las dependencias necesarias:

```bash
pip install pygame pyserial
```

### Configuración del ESP32
1. Carga el código `testesp32.ino` al ESP32 usando Arduino IDE.
2. Configura el SSID y contraseña del punto de acceso WiFi en el código.
3. Conecta los pines de motores y servo según las definiciones en el código.

## Uso

### Control Remoto vía WiFi
Ejecuta el script `control_auto.py` para controlar el auto usando el teclado:

```bash
python control_auto.py
```

- **W**: Adelante
- **S**: Atrás
- **A**: Girar izquierda
- **D**: Girar derecha
- **X**: Detener motores
- **C**: Centrar dirección

### Control Directo vía Serial
Ejecuta `control_esp.py` para enviar comandos directamente al ESP32 conectado por USB:

```bash
python control_esp.py
```

Sigue las instrucciones en pantalla para enviar comandos.

## Desarrollo y Pruebas

- Utiliza la MacBook para teleoperación durante el desarrollo.
- La Jetson Nano se integrará para autonomía completa en futuras fases.
- Revisa la documentación en `documentacion_auto.md` para detalles técnicos.

## Contribución

Si deseas contribuir:
1. Haz un fork del repositorio.
2. Crea una rama para tu feature.
3. Envía un pull request.

## Licencia

Este proyecto es de código abierto. Consulta el archivo de licencia para más detalles.

## Contacto

Para preguntas o soporte, contacta al desarrollador.
