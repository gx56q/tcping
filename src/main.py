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
    parser.add_argument("-t", "--timeout", type=int, default=1,
                        help="Time to wait for a response, in seconds")
    parser.add_argument("-i", "--interval", type=float, default=1,
                        help="Interval between pings, in seconds")

    args = parser.parse_args()

    try:
        ping.tcp_ping(args.host, args.port, args.count, args.timeout,
                      args.interval)
    except KeyboardInterrupt:
        ping.print_statistics(
            ping.tcp_ping.sent, ping.tcp_ping.received, ping.tcp_ping.times)
        sys.exit(1)
