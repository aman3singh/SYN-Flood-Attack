# SYN Flood Attack Simulation

This project provides a simple implementation of a SYN flood attack simulation and a custom TCP server for educational purposes. It demonstrates how TCP/IP networking works and how denial-of-service attacks can affect server resources.

## Overview

The project consists of two main components:

1. **TCP Server**: A lightweight Python server that listens for incoming TCP connections
2. **SYN Flood Tool**: A tool that simulates a SYN flood attack by sending multiple connection requests

This project is designed for educational purposes to help understand network security concepts and how DoS attacks work.

## Disclaimer

This tool is provided for educational purposes only. Using this tool against systems without explicit permission is illegal and unethical. Always practice responsible security testing.

## Prerequisites

- Python 3.6 or higher
- Administrative/root privileges (for sending raw packets)
- macOS, Linux, or Windows (with administrator privileges)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/syn-flood-simulation.git
   cd syn-flood-simulation
   ```

2. Install the required dependencies:
   ```bash
   pip install scapy
   ```

## Usage

### Starting the TCP Server

The TCP server listens for incoming connections on the specified port (default: 8080) and accepts them.

```bash
python3 tcp_server.py
```

You can modify the server port in the `tcp_server.py` file if needed.

### Running the SYN Flood Attack

The SYN flood tool sends multiple TCP SYN packets to the target server to simulate a flood attack.

```bash
# Basic usage (requires root/admin privileges)
sudo python3 syn_flood.py

# Custom parameters
sudo python3 syn_flood.py -t 127.0.0.1 -p 8080 -c 1000 -d 0.01 -n 2
```

Parameters:
- `-t, --target`: Target IP address (default: 127.0.0.1)
- `-p, --port`: Target port (default: 8080)
- `-c, --count`: Number of packets to send (default: 1000)
- `-d, --delay`: Delay between packets in seconds (default: 0.01)
- `-n, --threads`: Number of threads to use (default: 1)

## How It Works

### TCP Server

The TCP server:
1. Creates a socket and binds it to the specified host and port
2. Listens for incoming connections
3. Accepts connections and sends a welcome message
4. Closes the connection and waits for new ones

### SYN Flood Attack

The SYN flood attack:
1. Creates TCP sockets with random source ports
2. Sends TCP SYN packets to the target
3. Immediately closes the socket without completing the TCP handshake
4. Repeats this process multiple times to consume server resources

In a real-world scenario, this would cause the target server to maintain half-open connections, potentially exhausting its connection pool and resources.

## Code Structure

- `tcp_server.py`: Simple TCP server implementation
- `syn_flood.py`: SYN flood attack simulation tool

## Example Output

### TCP Server
```
[*] Server started on 0.0.0.0:8080, waiting for connections...
[+] Connection established with ('127.0.0.1', 55931)
[+] Connection established with ('127.0.0.1', 55932)
[*] Server running for 1916.8s | Connections accepted: 1000
```

### SYN Flood Tool
```
[*] Starting SYN flood attack on 127.0.0.1:8080
[*] Using 1 threads to send 1000 connection attempts with 0.01s delay
[*] Thread 1: Sent 100 connection attempts
[*] Thread 1: Sent 200 connection attempts
...
[*] Thread 1: Sent 1000 connection attempts
[+] Attack completed in 12.34 seconds
[+] Attempted to send approximately 1000 SYN packets
[+] Average rate: 81.04 attempts/second
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- This project was created for educational purposes to demonstrate network security concepts
- Inspiration and knowledge derived from various network security resources and courses