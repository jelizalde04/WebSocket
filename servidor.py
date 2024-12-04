import socket
import threading
import base64
import hashlib

# Configuración del servidor
HOST = '0.0.0.0'  # Escucha en todas las interfaces disponibles
PORT = 9001       # Cambié el puerto para evitar conflictos

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    print("Solicitud del cliente:")
    print(request)

    # Manejo del handshake WebSocket
    key_line = [line for line in request.split('\r\n') if "Sec-WebSocket-Key" in line][0]
    key = key_line.split(": ")[1]

    magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    accept_key = base64.b64encode(hashlib.sha1((key + magic_string).encode()).digest()).decode()

    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
    )
    client_socket.send(response.encode())

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print("Mensaje recibido (crudo):", message)
            decoded_message = message[2:].decode()
            print("Mensaje recibido (decodificado):", decoded_message)

            # Responder con un eco del mensaje recibido
            response_message = f"Eco: {decoded_message}"
            client_socket.send(b'\x81' + bytes([len(response_message)]) + response_message.encode())
        except Exception as e:
            print(f"Error manejando el cliente: {e}")
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor WebSocket escuchando en {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        print(f"Conexión aceptada de {address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
