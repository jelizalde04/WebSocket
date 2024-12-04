import socket
import base64

# Configuración del cliente
HOST = '127.0.0.1'  # Cambia si el servidor está en otra máquina
PORT = 9001         # Mismo puerto que el servidor

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Enviar handshake WebSocket
    key = base64.b64encode(b"cliente-websocket").decode()
    handshake = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    client.send(handshake.encode())
    response = client.recv(1024).decode()
    print("Respuesta del servidor:")
    print(response)

    while True:
        # Ingresar mensaje desde la consola
        user_message = input("Ingresa el mensaje para enviar al servidor (o 'exit' para salir): ")
        if user_message.lower() == 'exit':
            print("Cerrando conexión...")
            break

        # Enviar mensaje al servidor
        client.send(b'\x81' + bytes([len(user_message)]) + user_message.encode())
        response = client.recv(1024)

    client.close()

if __name__ == "__main__":
    connect_to_server()
