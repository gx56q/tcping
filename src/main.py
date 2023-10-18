import argparse
import sys
import ping

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Utility for tcp ping")
    parser.add_argument("host", help="Target host to ping")
    parser.add_argument("-p", "--port", type=int, default=80,
                        help="TCP port number")
    parser.add_argument("-c", "--count", type=int,
                        help="Number of pings to send")
    parser.add_argument("-t", "--timeout", type=float, default=1,
                        help="Time to wait for a response, in seconds")
    parser.add_argument("-i", "--interval", type=float, default=1,
                        help="Interval between pings, in seconds")

    args = parser.parse_args()

    if args.count is not None and args.count <= 0:
        print("Error: count should be greater than 0")
        sys.exit(1)
    if args.timeout <= 0:
        print("Error: timeout should be greater than 0")
        sys.exit(1)
    if args.interval <= 0:
        print("Error: interval should be greater than 0")
        sys.exit(1)

    sent, received, times = ping.tcp_ping(args.host, args.port, args.count,
                                          args.timeout, args.interval)
    if sent:
        ping.print_statistics(
            sent, received, times)
