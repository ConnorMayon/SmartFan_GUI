import RPi.GPIO as GPIO
import socket

def main():
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    pin = 4
    fan_state = False

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.OUT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                if data == b'power':
                    if fan_state:
                        fan_state = False
                        GPIO.output(pin, GPIO.LOW)
                    else:
                        fan_state = True
                        GPIO.output(pin, GPIO.HIGH)
                else:
                    GPIO.output(pin, GPIO.LOW)
                conn.sendall(data)



if __name__ == "__main__":
    main()