#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
test_drb_object.py
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from cosmosc2.connection import Connection 


class TestDrbObject(unittest.TestCase):

    HOST, PORT = "127.0.0.1", 7777

    @patch("cosmosc2.connection.HTTPConnection.connect")
    def test_object(self, connect):
        """
        Test json request
        """
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        connect.assert_not_called()
        self.assertIsNone(cmd_tlm_server._connection)

    @patch("cosmosc2.connection.HTTPConnection.connect")
    def test_object_localhost(self, connect):
        """
        Test json request
        """
        cmd_tlm_server = Connection()
        connect.assert_not_called()
        self.assertIsNone(cmd_tlm_server._connection)
        self.assertEqual(cmd_tlm_server.hostname, self.HOST)
        self.assertEqual(cmd_tlm_server.port, 2900)

    @patch("cosmosc2.connection.HTTPConnection.connect")
    def test_object_tacocat(self, connect):
        """
        Test json request
        """
        hostname = "tacocat"
        cmd_tlm_server = Connection(hostname, self.PORT)
        connect.assert_not_called()
        self.assertIsNone(cmd_tlm_server._connection)
        self.assertEqual(cmd_tlm_server.hostname, hostname)

    @patch("cosmosc2.connection.HTTPConnection.connect")
    def test_object_cosmos(self, connect):
        """
        Test json request
        """
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        connect.assert_not_called()
        self.assertIsNone(cmd_tlm_server._connection)

    @patch("cosmosc2.connection.HTTPConnection")
    def test_connection(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = (
            b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        )
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        cmd_tlm_server.write(self.test_connection.__name__)
        self.assertIsNotNone(cmd_tlm_server._connection)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()

    @patch("cosmosc2.connection.HTTPConnection")
    def test_with_connection(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = (
            b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        )
        connection.return_value = mock
        with Connection(self.HOST, self.PORT) as cmd_tlm_server:
            cmd_tlm_server.write(self.test_with_connection.__name__)
            self.assertIsNotNone(cmd_tlm_server._connection)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()

    @patch("cosmosc2.connection.time.sleep")
    @patch("cosmosc2.connection.HTTPConnection")
    def test_connection_refused_error(self, connection, sleep):
        """
        Test connection
        """
        sleep.return_value = None
        mock = MagicMock()
        mock.connect.side_effect = ConnectionRefusedError("test")
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write(self.test_connection_refused_error.__name__)
        self.assertIsNone(cmd_tlm_server._connection)
        mock.connect.assert_called()
        mock.request.assert_not_called()

    @patch("cosmosc2.connection.HTTPConnection")
    def test_connection_error(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.side_effect = ConnectionError("test")
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write(self.test_connection_error.__name__)
        self.assertIsNone(cmd_tlm_server._connection)
        mock.connect.assert_called_once()
        mock.request.assert_not_called()

    @patch("cosmosc2.connection.HTTPConnection")
    def test_response_timeout_error(self, connection):
        """
        Test connection
        """
        from socket import timeout

        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.read.side_effect = timeout("timed out test")
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write(self.test_response_error.__name__)
        self.assertIsNotNone(cmd_tlm_server._connection)
        mock.connect.assert_called()
        mock.request.assert_called()

    @patch("cosmosc2.connection.HTTPConnection")
    def test_response_none(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = None
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write(self.test_response_none.__name__)
        self.assertIsNotNone(cmd_tlm_server._connection)
        mock.connect.assert_called()
        mock.request.assert_called()

    @patch("cosmosc2.connection.HTTPConnection")
    def test_response_error(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.read.side_effect = ConnectionResetError("test")
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write(self.test_response_error.__name__)
        self.assertIsNotNone(cmd_tlm_server._connection)
        mock.connect.assert_called()
        mock.request.assert_called()

    @patch("cosmosc2.connection.HTTPConnection")
    def test_response_result_error(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = b"""
            {
                "jsonrpc": "2.0",
                "id": 107,
                "error": {
                    "code": "1234",
                    "message": "foobar",
                    "data": {
                        "foo": "bar"
                    }
                }
            }
        """
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        response = cmd_tlm_server.write(self.test_response_result_error.__name__)
        self.assertIsNotNone(response)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()

    @patch("cosmosc2.connection.HTTPConnection")
    def test_response_result_invalid(self, connection):
        """
        Test connection
        """
        mock = MagicMock()
        mock.connect.return_value = MagicMock()
        mock.request.request = MagicMock()
        mock.getresponse.return_value.read.return_value = (
            b'{"jsonrpc": "2.0", "id": 107}'
        )
        connection.return_value = mock
        cmd_tlm_server = Connection(self.HOST, self.PORT)
        with self.assertRaises(RuntimeError):
            cmd_tlm_server.write(self.test_response_result_invalid.__name__)
        self.assertIsNotNone(cmd_tlm_server._connection)
        mock.connect.assert_called_once()
        mock.request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
