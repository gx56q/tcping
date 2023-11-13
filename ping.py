import time
from _socket import gaierror
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1
from scapy.layers.inet6 import IPv6


def tcp_ping(target, port, count, timeout, interval, host_type='ipv4'):
    sent = 0
    received = 0
    times = []

    try:
        if host_type == 'ipv6':
            ip_layer = IPv6(dst=target)
            display_target = f"[{target}]"
        else:
            ip_layer = IP(dst=target)
            display_target = target
    except (OSError, gaierror) as e:
        if e.errno == 8:
            print(f"Error: {target} is unreachable")
            return sent, received, times

    try:
        while True:
            if count is not None and sent >= count:
                return sent, received, times
            packet = ip_layer / TCP(dport=port, flags="S")
            start_time = time.time()
            reply = sr1(packet, timeout=timeout, verbose=0)
            if reply:
                if reply.haslayer(TCP):
                    tcp_flags = reply[TCP].flags

                    if tcp_flags == 0x12:
                        # SYN-ACK
                        received += 1
                        elapsed = (time.time() - start_time) * 1000
                        times.append(elapsed)
                        print(
                            f"Reply from {display_target}:{port} "
                            f"time={elapsed:.2f}ms")
                    elif tcp_flags == 0x14:
                        # RST-ACK
                        print(f"Port {port} on {display_target} is closed")
                    elif tcp_flags == 0x11:
                        # FIN-ACK
                        print(
                            f"Port {port} on {display_target} is open, "
                            f"no response")
                    elif tcp_flags == 0x10 or tcp_flags == 0x02:
                        # ACK or SYN
                        print(
                            f"Port {port} on {display_target} is open "
                            f"and reset")
                    elif tcp_flags == 0x04:
                        # RST
                        print(f"Port {port} on {display_target} is closed")
                    elif tcp_flags & 0x01:
                        # FIN
                        print(f"Received FIN from {display_target}:{port}")
                    elif tcp_flags & 0x11:
                        # FIN-ACK
                        print(
                            f"Received FIN-ACK from {display_target}:{port}")
                    elif tcp_flags & 0x08:
                        # PSH
                        print(f"Received PSH from {display_target}:{port}")
                    elif tcp_flags & 0x18:
                        # PSH-ACK
                        print(
                            f"Received PSH-ACK from {display_target}:{port}")
                    else:
                        print(
                            f"Received a response from"
                            f"{display_target}:{port}, "
                            f"but with unexpected TCP flags: {hex(tcp_flags)}")
                else:
                    print(
                        f"Unexpected response without TCP layer from "
                        f"{display_target}:{port}")

            else:
                print(f"No response from {display_target}:{port}")

            sent += 1
            if interval:
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\n--- Interruption detected. Stopping pinging. ---")
    except (OSError, gaierror) as e:
        if e.errno == 8:
            print(f"Error: {target} is unreachable")
        else:
            print(str(e))
    finally:
        return sent, received, times


def print_statistics(sent, received, times):
    print("\n--- tcping stats ---")
    print(
        f"Packets: Sent = {sent}, Received = {received}, Lost = "
        f"{sent - received} ({(sent - received) / sent * 100:.2f}% loss)")
    if times:
        print(f"Answer times (ms):")
        print(
            f"Minimum = {min(times):.2f}ms, Maximum = {max(times):.2f}ms, "
            f"Average = {sum(times) / len(times):.2f}ms")
