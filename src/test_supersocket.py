from supersocket import Packet, Client, Server, PacketHeader, OutputVar
import unittest
from unittest.mock import MagicMock, patch
import datetime

import warnings

# Suppress specific warnings in a specific test or setup/teardown method
warnings.filterwarnings(action="ignore", category=ResourceWarning)

OLD_PRINT = print

def print(*args, **kwargs):
	msg = " ".join([str(arg) for arg in args])
	time = datetime.datetime.now().strftime("[[ %d/%m/%Y %H:%M:%S ]]")
	OLD_PRINT(f"\n{time} ::: {msg}")

class TestSupersocket(unittest.TestCase):

	def test_handshake_on_server(self):
		print("`test_handshake_on_server` ::: Creating server...")
		server = Server("127.0.0.1", 8000)
		print("`test_handshake_on_server` ::: Patching `_handle_handshake` & `_handle_post_handshake`...")
		server._handle_handshake = MagicMock(name="_handle_handshake")
		server._handle_post_handshake = MagicMock(name="_handle_post_handshake")
		print("`test_handshake_on_server` ::: Starting server...")
		server.begin()
		print("`test_handshake_on_server` ::: Asserting `_handle_handshake` was called...")
		server._handle_handshake.assert_called_once()
		print("`test_handshake_on_server` ::: Asserting `_handle_post_handshake` was called...")
		server._handle_post_handshake.assert_called_once()
		print("`test_handshake_on_server` ::: Done.")

	def test_handshake_on_client(self):
		print("`test_handshake_on_client` ::: Creating client...")
		client = Client("127.0.0.1", 8000)
		print("`test_handshake_on_client` ::: Patching `_handle_handshake` & `_handle_post_handshake`...")
		client._handle_handshake = MagicMock(name="_handle_handshake")
		client._handle_post_handshake = MagicMock(name="_handle_post_handshake")
		print("`test_handshake_on_client` ::: Starting client...")
		client.begin()
		print("`test_handshake_on_client` ::: Asserting `_handle_handshake` was called...")
		client._handle_handshake.assert_called_once()
		print("`test_handshake_on_client` ::: Asserting `_handle_post_handshake` was called...")
		client._handle_post_handshake.assert_called_once()
		print("`test_handshake_on_client` ::: Done.")

	def test_recv_on_server(self):
		print("`test_send_recv_on_server` ::: Using a patch for `socket.socket`...")
		with patch("supersocket.socket.socket") as mock_socket:
			print("`test_send_recv_on_server` ::: Creating test message...")
			mock_socket_instance = mock_socket.return_value
			mock_socket_instance.recv.return_value = "test message".encode()
			mock_socket_instance.close = MagicMock(name="close")
			mock_socket_instance.close.assert_called_once()
			print("`test_send_recv_on_server` ::: Creating server...")	
			server = Server("127.0.0.1", 8000)
			server._sock = mock_socket_instance
			print("`test_send_recv_on_server` ::: Creating `OutputVar[Packet]`...")
			out_packet = OutputVar[Packet](Packet.Empty())
			print("`test_send_recv_on_server` ::: Simulating a test receiving...")
			server.recv(out_packet)
			print("`test_send_recv_on_server` ::: Asserting packet message...")
			self.assertEqual(out_packet().msg, "test message")
			print("`test_send_recv_on_server` ::: Asserting packet header...")
			self.assertEqual(out_packet().header, PacketHeader.Empty())
			print("`test_send_recv_on_server` ::: Done.")

	def test_recv_on_client(self):
		print("`test_send_recv_on_client` ::: Using a patch for `socket.socket`...")
		with patch("supersocket.socket.socket") as mock_socket:
			print("`test_send_recv_on_client` ::: Creating test message...")
			mock_socket_instance = mock_socket.return_value
			mock_socket_instance.recv.return_value = "test message".encode()
			mock_socket_instance.close = MagicMock(name="close")
			mock_socket_instance.close.assert_called_once()
			print("`test_send_recv_on_client` ::: Creating client...")
			client = Client("127.0.0.1", 8000)
			client._sock = mock_socket_instance
			print("`test_send_recv_on_client` ::: Creating `OutputVar[Packet]`...")
			out_packet = OutputVar[Packet](Packet.Empty())
			print("`test_send_recv_on_client` ::: Simulating a test receiving...")
			client.recv(out_packet)
			print("`test_send_recv_on_client` ::: Asserting packet message...")
			self.assertEqual(out_packet().msg, "test message")
			print("`test_send_recv_on_client` ::: Asserting packet header...")
			self.assertEqual(out_packet().header, PacketHeader.Empty())
			print("`test_send_recv_on_client` ::: Done.")

	def generate_1_kilobyte_message(self):
		return "a" * 1024

	def test_recv_more_than_buffer_size_on_server(self):
		print("`test_send_recv_more_than_buffer_size_on_server` ::: Using a patch for `socket.socket`...")
		with patch("supersocket.socket.socket") as mock_socket:
			print("`test_send_recv_more_than_buffer_size_on_server` ::: Creating test message...")
			mock_socket_instance = mock_socket.return_value
			mock_socket_instance.recv.return_value = self.generate_1_kilobyte_message().encode()
			mock_socket_instance.close = MagicMock(name="close")
			mock_socket_instance.close.assert_called_once()
			print("`test_send_recv_more_than_buffer_size_on_server` ::: Creating server...")
			server = Server("127.0.0.1", 8000)
			server._sock = mock_socket_instance
			print("`test_send_recv_more_than_buffer_size_on_server` ::: Creating `OutputVar[Packet]`...")
			out_packet = OutputVar[Packet](Packet.Empty())
			print("`test_send_recv_more_than_buffer_size_on_server` ::: Simulating a test receiving...")
			server.recv(out_packet)
			print("`test_send_recv_more_than_buffer_size_on_server` ::: Asserting packet message...")
			self.assertEqual(out_packet().msg, self.generate_1_kilobyte_message())
			print("`test_send_recv_more_than_buffer_size_on_server` ::: Asserting packet header...")
			self.assertEqual(out_packet().header, PacketHeader.Empty())
			print("`test_send_recv_more_than_buffer_size_on_server` ::: Done.")

	def test_recv_more_than_buffer_size_on_client(self):
		print("`test_send_recv_more_than_buffer_size_on_client` ::: Using a patch for `socket.socket`...")
		with patch("supersocket.socket.socket") as mock_socket:
			print("`test_send_recv_more_than_buffer_size_on_client` ::: Creating test message...")
			mock_socket_instance = mock_socket.return_value
			mock_socket_instance.recv.return_value = self.generate_1_kilobyte_message().encode()
			mock_socket_instance.close = MagicMock(name="close")
			mock_socket_instance.close.assert_called_once()
			print("`test_send_recv_more_than_buffer_size_on_client` ::: Creating client...")
			client = Client("127.0.0.1", 8000)
			client._sock = mock_socket_instance
			print("`test_send_recv_more_than_buffer_size_on_client` ::: Creating `OutputVar[Packet]`...")
			out_packet = OutputVar[Packet](Packet.Empty())
			print("`test_send_recv_more_than_buffer_size_on_client` ::: Simulating a test receiving...")
			client.recv(out_packet)
			print("`test_send_recv_more_than_buffer_size_on_client` ::: Asserting packet message...")
			self.assertEqual(out_packet().msg, self.generate_1_kilobyte_message())
			print("`test_send_recv_more_than_buffer_size_on_client` ::: Asserting packet header...")
			self.assertEqual(out_packet().header, PacketHeader.Empty())
			print("`test_send_recv_more_than_buffer_size_on_client` ::: Done.")



if __name__ == "__main__":
    unittest.main()
