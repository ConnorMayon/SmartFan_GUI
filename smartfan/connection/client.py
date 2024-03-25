import socket

if __name__ == "__main__":
    HOST = '192.168.1.161'    # The remote host
    PORT = 50007              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        output = bytes(input(), 'utf-8');
        s.sendall(output)
        data = s.recv(1024)
    print('Received', repr(data))