# Arquitectura del Auto Autónomo / Teleoperado

## 1. Visión general

El sistema se divide en dos niveles:

- **Nivel de bajo nivel:** ESP32
- **Nivel de alto nivel:** Jetson Nano

Además, durante la fase de desarrollo se usará una **MacBook** para teleoperación remota.

---

## 2. Objetivo de la arquitectura

La arquitectura busca:

- separar la inteligencia del control de actuadores
- hacer el sistema más robusto
- permitir teleoperación y autonomía
- facilitar pruebas por etapas
- evitar cargar a la Jetson con tareas de tiempo real

---

## 3. Componentes y responsabilidades

### 3.1 ESP32
Responsable de:

- recibir comandos remotos
- controlar los motores traseros
- controlar el servo de dirección
- leer encoders
- ejecutar paros de seguridad
- actuar como controlador de tiempo real

### 3.2 Jetson Nano
Responsable de:

- procesar cámara
- procesar LiDAR
- ejecutar algoritmos de percepción
- detectar carriles, obstáculos y señales
- decidir velocidad y ángulo de dirección
- enviar comandos de control al ESP32

### 3.3 MacBook
Responsable de:

- teleoperación remota en etapa de pruebas
- validación de actuadores
- depuración inicial del sistema

### 3.4 Puente H
Responsable de:

- accionar los motores traseros
- convertir señales de control en potencia para motores

### 3.5 PCA9685
Responsable de:

- generar PWM estable para el servo
- descargar esa tarea del ESP32

### 3.6 Servo de dirección
Responsable de:

- mover el mecanismo frontal de dirección

### 3.7 Motores DC con encoder
Responsables de:

- tracción del vehículo
- retroalimentación de velocidad y desplazamiento

### 3.8 Cámara
Responsable de:

- capturar información visual para percepción

### 3.9 LiDAR
Responsable de:

- detectar distancias y obstáculos en el entorno

---

## 4. Modos de operación

### 4.1 Modo manual
Flujo:

- MacBook envía comandos por WiFi al ESP32
- ESP32 controla motores y dirección

Uso:

- pruebas
- calibración
- teleoperación
- validación de hardware

### 4.2 Modo autónomo
Flujo:

- cámara y LiDAR envían datos a Jetson
- Jetson procesa entorno
- Jetson calcula acción de control
- Jetson envía comando al ESP32
- ESP32 ejecuta movimiento

Uso:

- navegación autónoma
- seguimiento de carril
- evasión de obstáculos
- pruebas de competencia

### 4.3 Modo seguro
Flujo:

- si falla comunicación o hay evento crítico
- ESP32 ejecuta stop de motores
- opcionalmente centra la dirección

Uso:

- seguridad del sistema
- recuperación ante fallos

---

## 5. Flujo de información

### 5.1 Flujo manual
1. Usuario presiona tecla en MacBook
2. MacBook manda comando por WiFi
3. ESP32 recibe el comando
4. ESP32 ajusta motor y dirección
5. Puente H y PCA9685 ejecutan la orden

### 5.2 Flujo autónomo
1. Sensores capturan datos
2. Jetson procesa percepción
3. Jetson calcula trayectoria o acción
4. Jetson manda comando al ESP32
5. ESP32 aplica actuadores

### 5.3 Flujo de retroalimentación futura
1. Encoders generan pulsos
2. ESP32 calcula velocidad real
3. ESP32 ajusta PWM si es necesario
4. Jetson recibe estado resumido del vehículo

---

## 6. Arquitectura física resumida

```text
MacBook ----WiFi----> ESP32 ----> Puente H ----> Motores traseros
                          |
                          +----I2C----> PCA9685 ----> Servo dirección
                          |
                          +----GPIO----> Encoders

Jetson Nano <---- Cámara
Jetson Nano <---- LiDAR

Jetson Nano ----(futuro enlace de control)----> ESP32