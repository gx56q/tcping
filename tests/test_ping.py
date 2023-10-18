import unittest
from _socket import gaierror
from unittest.mock import patch

from scapy.layers.inet import TCP

import ping


class TestPing(unittest.TestCase):

    @patch('ping.sr1')
    def test_successful_ping(self, mock_sr1):
        mock_sr1.return_value = TCP(flags=0x12)
        sent, received, times = ping.tcp_ping("www.google.com", 80, 1, 1, 1)
        self.assertEqual(sent, 1)
        self.assertEqual(received, 1)
        self.assertTrue(0 <= times[0] <= 1)

    @patch('ping.sr1')
    def test_unsuccessful_ping(self, mock_sr1):
        mock_sr1.return_value = None
        sent, received, times = ping.tcp_ping("www.google.com", 80, 1, 1, 1)
        self.assertEqual(sent, 1)
        self.assertEqual(received, 0)
        self.assertFalse(times)

    @patch('ping.sr1')
    @patch('builtins.print')
    def test_network_error(self, mock_print, mock_sr1):
        mock_sr1.side_effect = gaierror(8, "Name or service not known")
        ping.tcp_ping("g0ogle.xyz", 80, 1, 1, 1)
        mock_print.assert_any_call(
            "Error: g0ogle.xyz is unreachable")

    @patch('ping.sr1')
    def test_keyboard_interrupt(self, mock_sr1):
        mock_sr1.side_effect = KeyboardInterrupt
        sent, received, times = ping.tcp_ping("www.google.com", 80, 1, 1, 1)
        self.assertEqual(sent, 0)
        self.assertEqual(received, 0)
        self.assertFalse(times)

    @patch('builtins.print')
    @patch('ping.sr1')
    def test_no_response(self, mock_sr1, mock_print):
        mock_sr1.return_value = TCP(flags=0x10)
        ping.tcp_ping("www.google.com", 80, 1, 1, 1)
        mock_print.assert_any_call("No response from www.google.com:80")

    @patch('ping.sr1')
    def test_response_timeout(self, mock_sr1):
        mock_sr1.return_value = None
        sent, received, times = ping.tcp_ping("www.google.com", 80, 1, 1, 1)
        self.assertEqual(sent, 1)
        self.assertEqual(received, 0)
        self.assertFalse(times)

    @patch('builtins.print')
    def test_print_statistics(self, mock_print):
        ping.print_statistics(4, 3, [20, 25, 22, 23])

        mock_print.assert_any_call("\n--- tcping stats ---")
        mock_print.assert_any_call(
            "Packets: Sent = 4, Received = 3, Lost = 1 (25.00% loss)")
        mock_print.assert_any_call("Answer times (ms):")
        mock_print.assert_any_call(
            "Minimum = 20.00ms, Maximum = 25.00ms, Average = 22.50ms")


if __name__ == '__main__':
    unittest.main()
