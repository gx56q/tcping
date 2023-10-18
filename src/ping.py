import time
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1


def tcp_ping(target, port, count, timeout, interval):
    sent = 0
    received = 0
    times = []

    while True:
        if count is not None and sent >= count:
            break

        packet = IP(dst=target) / TCP(dport=port, flags="S")
        start_time = time.time()
        reply = sr1(packet, timeout=timeout, verbose=0)
        if reply and reply[TCP].flags == "SA":
            received += 1
            elapsed = (time.time() - start_time) * 1000
            times.append(elapsed)
            print(f"Reply from {target}:{port} time={elapsed:.2f}ms")
        else:
            print(f"No response from {target}:{port}")

        sent += 1

        if count is not None and sent < count:
            time.sleep(interval)

    print_statistics(sent, received, times)


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
