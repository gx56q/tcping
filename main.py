import argparse
import ipaddress
import socket
import sys

import ping


def parse_args():
    parser = argparse.ArgumentParser(description="Utility for tcp ping")
    parser.add_argument("hosts", help="Comma-separated target hosts to ping")
    parser.add_argument("-p", "--ports", default="80",
                        help="Comma-separated TCP port numbers")
    parser.add_argument("-c", "--count", type=int,
                        help="Number of pings to send")
    parser.add_argument("-t", "--timeout", type=float, default=1,
                        help="Time to wait for a response, in seconds")
    parser.add_argument("-i", "--interval", type=float, default=1,
                        help="Interval between pings, in seconds")
    return parser.parse_args()


def validate_host(host):
    if not host:
        sys.exit(f"Error: Host is empty.")
    try:
        ip_version = ipaddress.ip_address(host).version
        if ip_version == 6:
            return host, 'ipv6'
        else:
            return host, 'ipv4'
    except ValueError:
        try:
            resolved_ip = socket.gethostbyname(host)
            ip_version = ipaddress.ip_address(resolved_ip).version
            if ip_version == 6:
                return host, 'ipv6'
            else:
                return host, 'ipv4'
        except socket.gaierror:
            sys.exit(
                f"Error: Unable to resolve {host}."
                f" It's not a valid domain name or IP address.")


def validate_port(port_str):
    try:
        port = int(port_str)
        if not (1 <= port <= 65535):
            raise ValueError
        return port
    except ValueError:
        sys.exit(f"Error: {port_str} is not a valid TCP port")


def main():
    args = parse_args()
    if args.count is not None and args.count <= 0:
        sys.exit("Error: count should be greater than 0")
    if args.timeout <= 0:
        sys.exit("Error: timeout should be greater than 0")
    if args.interval <= 0:
        sys.exit("Error: interval should be greater than 0")

    hosts_data = [validate_host(h) for h in args.hosts.split(',') if h]
    ports = [validate_port(p) for p in args.ports.split(',') if p]

    for host, host_type in hosts_data:
        for port in ports:
            if host_type == "ipv6":
                display_host = f"[{host}]"
            else:
                display_host = host
            print(f"-- Pinging {display_host}:{port} --")
            sent, received, times = ping.tcp_ping(host, port, args.count,
                                                  args.timeout, args.interval,
                                                  host_type)
            if sent:
                ping.print_statistics(sent, received, times)
            print()


if __name__ == '__main__':
    print("\033c")
    main()
