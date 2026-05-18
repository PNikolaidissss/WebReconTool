import socket
import requests
import argparse
import sys

COMMON_PORTS = [21, 22, 80, 443, 8080]
COMMON_PATHS = ["/admin", "/login", "/dashboard", "/api", "/robots.txt"]


def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        print(f"[+] Resolved IP: {ip}")
        return ip
    except socket.gaierror:
        print("[-] Cannot resolve target")
        return None


def scan_ports(ip):
    print("\n[+] Port scanning...\n")
    open_ports = []

    for port in COMMON_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        if sock.connect_ex((ip, port)) == 0:
            print(f"[OPEN] {port}")
            open_ports.append(port)

        sock.close()

    return open_ports


def check_paths(target):
    print("\n[+] Web path discovery...\n")
    found = []

    for path in COMMON_PATHS:
        url = f"http://{target}{path}"

        try:
            r = requests.get(url, timeout=3)
            if r.status_code in [200, 301, 302]:
                print(f"[FOUND] {url} ({r.status_code})")
                found.append(url)
        except:
            pass

    return found


def banner():
    print("""
=============================
   WEB RECON TOOL v2
   (educational use only)
=============================
""")


def main():
    banner()

    parser = argparse.ArgumentParser(description="Simple Recon Tool")
    parser.add_argument("target", help="Domain or IP")

    args = parser.parse_args()

    target = args.target

    ip = resolve_target(target)
    if not ip:
        sys.exit()

    open_ports = scan_ports(ip)
    found_paths = check_paths(target)

    print("\n===== SUMMARY =====")
    print(f"Target: {target}")
    print(f"Open ports: {open_ports}")
    print(f"Found paths: {found_paths}")
    print("===================")


if __name__ == "__main__":
    main()
