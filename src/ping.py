import time
from _socket import gaierror
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1


def tcp_ping(target, port, count, timeout, interval):
    sent = 0
    received = 0
    times = []

    try:
        while True:
            if count is not None and sent >= count:
                return sent, received, times
            packet = IP(dst=target) / TCP(dport=port, flags="S")
            start_time = time.time()

            reply = sr1(packet, timeout=timeout, verbose=0)
            if reply and reply[TCP].flags == 0x12:
                received += 1
                elapsed = (time.time() - start_time) * 1000
                times.append(elapsed)
                print(f"Reply from {target}:{port} time={elapsed:.2f}ms")
            else:
                print(f"No response from {target}:{port}")

            sent += 1

            if interval:
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\n--- Interruption detected. Stopping pinging. ---")
    except (OSError, gaierror) as e:
        if e.errno == 8:
            print(f"Error: {target} is unreachable")
        else:
            print(e)
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
