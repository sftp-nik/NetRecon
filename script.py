import socket
import os
import subprocess

def scan_ports(target_ip, ports):
    results = {}
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            results[port] = "Open"
        else:
            results[port] = "Closed"
        sock.close()
    return results

def get_service_version(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  
        sock.connect((target_ip, port))
        sock.send(b'GET / HTTP/1.1\r\n\r\n')
        response = sock.recv(1024)
        sock.close()
        return response.decode('utf-8')
    except Exception as e:
        return str(e)

def detect_os(target_ip):
    try:
        cmd = f"nmap -O {target_ip}"
        output = subprocess.check_output(cmd, shell=True)
        return output.decode('utf-8')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    port_range = input("Enter port range to scan (e.g., 1-100): ")
    start_port, end_port = map(int, port_range.split('-'))
    ports_to_scan = range(start_port, end_port + 1)

    port_results = scan_ports(target_ip, ports_to_scan)
    print("Port Scanning Results:")
    for port, status in port_results.items():
        print(f"Port {port}: {status}")

    for port in port_results:  
        if port_results[port] == "Open":
            service_version = get_service_version(target_ip, port)
            print(f"Service version on port {port}: {service_version}")

    os_detection = detect_os(target_ip)
    print("Operating System Detection:")
    print(os_detection)
