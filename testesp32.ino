#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

const char* ssid = "CARRO_ESP32";
const char* password = "12345678";

WiFiServer server(80);

// ===== SERVO =====
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVO_CHANNEL 0
#define SERVO_MIN 150
#define SERVO_MAX 600

int ANGULO_IZQ = 40;
int ANGULO_CENTRO = 90;
int ANGULO_DER = 140;

// ===== MOTORES =====
#define IN1 25
#define IN2 26
#define IN3 27
#define IN4 14
#define ENA 33
#define ENB 32

int velocidadMotor = 180;

// ===== FUNCIONES =====
void setServo(int angle) {
  int pulse = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(SERVO_CHANNEL, 0, pulse);
}

void adelante() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  ledcWrite(ENA, velocidadMotor);
  ledcWrite(ENB, velocidadMotor);
}

void atras() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  ledcWrite(ENA, velocidadMotor);
  ledcWrite(ENB, velocidadMotor);
}

void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  ledcWrite(ENA, 0);
  ledcWrite(ENB, 0);
}

// ===== HTML =====
String html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { text-align: center; font-family: Arial; }
button {
  width: 80px; height: 80px;
  font-size: 20px;
  margin: 10px;
}
</style>
</head>
<body>
<h2>Control Remoto KYROS TMR</h2>

<button ontouchstart="send('w')" ontouchend="send('x')">⬆</button><br>
<button ontouchstart="send('a')" ontouchend="send('c')">⬅︎</button>
<button ontouchstart="send('d')" ontouchend="send('c')">➡︎</button><br>
<button ontouchstart="send('s')" ontouchend="send('x')">⬇</button>

<script>
function send(cmd) {
  fetch("/" + cmd);
}
</script>

</body>
</html>
)rawliteral";

// ===== SETUP =====
void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  ledcAttach(ENA, 1000, 8);
  ledcAttach(ENB, 1000, 8);

  Wire.begin(21, 22);
  pwm.begin();
  pwm.setPWMFreq(50);

  setServo(ANGULO_CENTRO);
  stopMotor();

  WiFi.softAP(ssid, password);
  server.begin();

  Serial.println("Listo");
  Serial.println(WiFi.softAPIP());
}

// ===== LOOP =====
void loop() {
  WiFiClient client = server.available();

  if (client) {
    String req = client.readStringUntil('\r');
    client.flush();

    if (req.indexOf("GET /w") >= 0) adelante();
    if (req.indexOf("GET /s") >= 0) atras();
    if (req.indexOf("GET /x") >= 0) stopMotor();
    if (req.indexOf("GET /a") >= 0) setServo(ANGULO_IZQ);
    if (req.indexOf("GET /d") >= 0) setServo(ANGULO_DER);
    if (req.indexOf("GET /c") >= 0) setServo(ANGULO_CENTRO);

    client.println("HTTP/1.1 200 OK");
    client.println("Content-type:text/html");
    client.println();
    client.println(html);
    client.stop();
  }
}