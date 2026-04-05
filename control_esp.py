import serial
import sys
import time

PORT = "/dev/ttyUSB0"   # cámbialo si hace falta
BAUDRATE = 115200

def main():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        time.sleep(2)
        ser.reset_input_buffer()
        print(f"Conectado a {PORT}")
    except Exception as e:
        print(f"Error abriendo puerto: {e}")
        sys.exit(1)

    print("Controles:")
    print("  w = adelante")
    print("  s = atras")
    print("  x = stop")
    print("  a = direccion izquierda")
    print("  d = direccion derecha")
    print("  c = centrar direccion")
    print("  1,2,3 = velocidad")
    print("  q = salir")

    try:
        while True:
            cmd = input("Comando: ").strip().lower()

            if cmd == "q":
                ser.write(b"x\n")
                break

            validos = ["w", "s", "x", "a", "d", "c", "1", "2", "3"]
            if cmd in validos:
                ser.write((cmd + "\n").encode("utf-8"))
                time.sleep(0.1)

                while ser.in_waiting:
                    resp = ser.readline().decode("utf-8", errors="ignore").strip()
                    if resp:
                        print("ESP32:", resp)
            else:
                print("Comando no válido")

    except KeyboardInterrupt:
        try:
            ser.write(b"x\n")
        except Exception:
            pass

    finally:
        ser.close()
        print("Puerto cerrado")

if __name__ == "__main__":
    main()