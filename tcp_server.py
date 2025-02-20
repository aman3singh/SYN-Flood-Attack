import socket

# Define the server IP and port
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 8080        # Change if you want to test on a different port

def start_server():
    """
    Starts a simple TCP server that listens for incoming connections.
    """
    try:
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket options to reuse the port if restarting
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections (max 5 queued connections)
        server_socket.listen(5)
        print(f"[*] Server started on {HOST}:{PORT}, waiting for connections...")

        while True:
            try:
                # Accept incoming client connection
                client_socket, client_address = server_socket.accept()
                print(f"[+] Connection established with {client_address}")

                # Send a welcome message to the client
                client_socket.send(b"Hello, you are connected to the server!\n")

                # Close the client connection
                client_socket.close()

            except Exception as e:
                print(f"[-] Error handling client: {e}")

    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
    except Exception as e:
        print(f"[-] Server error: {e}")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    start_server()

