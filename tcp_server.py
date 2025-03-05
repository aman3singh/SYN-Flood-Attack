import socket
import threading
import time

# Define the server IP and port
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 8080       # Change if you want to test on a different port
BACKLOG = 50      # Increased backlog to better observe SYN flood effects

# Add stats for monitoring
connection_count = 0
start_time = time.time()

def monitor_server():
    """Periodically prints server statistics."""
    global connection_count, start_time
    
    while True:
        elapsed_time = time.time() - start_time
        print(f"[*] Server running for {elapsed_time:.1f}s | Connections accepted: {connection_count}")
        time.sleep(5)

def handle_client(client_socket, client_address):
    """Handles an individual client connection."""
    global connection_count
    
    try:
        print(f"[+] Connection established with {client_address}")
        connection_count += 1
        
        # Send a welcome message to the client
        client_socket.send(b"Hello, you are connected to the server!\n")
        
        # Keep the connection open for a short time to simulate processing
        time.sleep(2)
        
    except Exception as e:
        print(f"[-] Error handling client: {e}")
    finally:
        # Close the client connection
        client_socket.close()

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

        # Listen for incoming connections with increased backlog
        server_socket.listen(BACKLOG)
        print(f"[*] Server started on {HOST}:{PORT}, waiting for connections...")
        
        # Start the monitoring thread
        monitor_thread = threading.Thread(target=monitor_server, daemon=True)
        monitor_thread.start()

        while True:
            try:
                # Accept incoming client connection
                client_socket, client_address = server_socket.accept()
                
                # Handle client in a separate thread
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

            except Exception as e:
                print(f"[-] Error accepting connection: {e}")

    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
    except Exception as e:
        print(f"[-] Server error: {e}")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    start_server()