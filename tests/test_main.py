import sys
import unittest
import main
from unittest.mock import patch


class TestTcping(unittest.TestCase):

    @patch('ping.tcp_ping', return_value=(4, 4, [10, 12, 11, 9]))
    @patch('ping.print_statistics')
    def test_ipv6_display_format(self, mock_tcp_ping,
                                 mock_print_statistics):
        import argparse
        args = argparse.Namespace()
        args.hosts = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        args.ports = '80'
        args.count = 4
        args.timeout = 1
        args.interval = 1

        with patch('builtins.print') as mock_print:
            with patch('main.parse_args', return_value=args):
                main.main()
                mock_print.assert_any_call(
                    '-- Pinging [2001:0db8:85a3:0000:0000:8a2e:0370:7334]:80 '
                    '--')

    def test_validate_host_ipv6(self):
        host, host_type = main.validate_host(
            '2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertEqual(host_type, 'ipv6')

    def test_validate_host_ipv4(self):
        host, host_type = main.validate_host('192.168.1.1')
        self.assertEqual(host_type, 'ipv4')

    @patch('sys.exit')
    def test_validate_empty_host(self, mock_exit):
        main.validate_host('')
        mock_exit.assert_called_once()

    @patch('sys.exit')
    def test_validate_empty_port(self, mock_exit):
        main.validate_port('')
        mock_exit.assert_called_once()

    @patch('ping.tcp_ping')
    def test_valid_ping(self, mock_tcp_ping):
        mock_tcp_ping.return_value = (4, 4, [20, 25, 22, 23])
        sys_argv_backup = sys.argv
        sys.argv = ['tcping.py', 'www.google.com', '-p', '80', '-c', '4']
        main.main()
        sys.argv = sys_argv_backup

    def test_invalid_count(self):
        sys_argv_backup = sys.argv
        sys.argv = ['tcping.py', 'www.google.com', '-c', '0']
        with self.assertRaises(SystemExit) as context:
            main.main()
        self.assertTrue(
            "Error: count should be greater than 0" in str(context.exception))
        sys.argv = sys_argv_backup

    def test_invalid_timeout(self):
        sys_argv_backup = sys.argv
        sys.argv = ['tcping.py', 'www.google.com', '-t', '0']
        with self.assertRaises(SystemExit) as context:
            main.main()
        self.assertTrue("Error: timeout should be greater than 0" in
                        str(context.exception))
        sys.argv = sys_argv_backup

    def test_invalid_interval(self):
        sys_argv_backup = sys.argv
        sys.argv = ['tcping.py', 'www.google.com', '-i', '0']
        with self.assertRaises(SystemExit) as context:
            main.main()
        self.assertTrue("Error: interval should be greater than 0" in
                        str(context.exception))
        sys.argv = sys_argv_backup

    @patch('ping.tcp_ping')
    def test_default_values(self, mock_tcp_ping):
        mock_tcp_ping.return_value = (4, 4, [20, 25, 22, 23])
        sys_argv_backup = sys.argv
        sys.argv = ['tcping.py', 'www.google.com']
        main.main()
        mock_tcp_ping.assert_called_once_with('www.google.com', 80, None, 1, 1,
                                              'ipv4')
        sys.argv = sys_argv_backup

    @patch('ping.tcp_ping')
    @patch('builtins.print')
    def test_statistics_printout(self, mock_print, mock_tcp_ping):
        mock_tcp_ping.return_value = (4, 4, [20, 25, 22, 23])
        sys_argv_backup = sys.argv
        sys.argv = ['tcping.py', 'www.google.com', '-c', '4']
        main.main()
        mock_print.assert_any_call(
            "\n--- tcping stats ---")
        mock_print.assert_any_call(
            "Packets: Sent = 4, Received = 4, Lost = 0 (0.00% loss)")
        mock_print.assert_any_call(
            "Answer times (ms):")
        mock_print.assert_any_call(
            "Minimum = 20.00ms, Maximum = 25.00ms, Average = 22.50ms")
        sys.argv = sys_argv_backup

    def test_parse_args_defaults(self):
        sys.argv = ['main.py', 'www.google.com']
        args = main.parse_args()
        self.assertEqual(args.hosts, 'www.google.com')
        self.assertEqual(args.ports, '80')
        self.assertEqual(args.count, None)
        self.assertEqual(args.timeout, 1)
        self.assertEqual(args.interval, 1)

    def test_parse_args_non_defaults(self):
        sys.argv = ['main.py', 'www.example.com', '-p',
                    '8080', '-c', '5', '-t', '2', '-i', '0.5']
        args = main.parse_args()
        self.assertEqual(args.hosts, 'www.example.com')
        self.assertEqual(args.ports, '8080')
        self.assertEqual(args.count, 5)
        self.assertEqual(args.timeout, 2)
        self.assertEqual(args.interval, 0.5)


if __name__ == '__main__':
    unittest.main()
