from supersocket import Packet, Client, Server, ClientRepresentative, ServerRepresentative, PacketHeader, OutputVar
import unittest
from unittest.mock import MagicMock, Mock, patch
import datetime
import warnings
import json







warnings.filterwarnings(action="ignore", category=ResourceWarning)

OLD_PRINT = print

def print(*args, **kwargs):
	msg = " ".join([str(arg) for arg in args])
	time = datetime.datetime.now().strftime("[[ %d/%m/%Y %H:%M:%S ]]")
	OLD_PRINT(f"\n{time} ::: {msg}")







class Test_supersocket_ANetworkManipulator(unittest.TestCase):



	@patch("supersocket.socket.socket")
	def test_direct_recv_from_using_client(self, mock_socket_class):
		# Making `supersocket.socket.socket` be a mocked object.
		mock_socket = MagicMock()
		mock_socket_class.return_value = mock_socket

		client = Client("127.0.0.1", 12345, buffer_size=10)

		# Mocking the handshake methods to not actually perform any network operations.
		client._handle_handshake = MagicMock()
		client._handle_post_handshake = MagicMock()
		
		# Since we're testing `direct_recv_from`, no need to mock `client.begin` or invoke it.
		# Prepare the mocked `_recv` method to simulate receiving message parts.
		parts = [
			f"{{\"a\":\"b\"}}{client._split_char}",
			"Hello     ",
			"     World",
			f"     !!!!{client._suffix}"
		]
		for part in parts:
			assert len(part) == 10
		client._recv = MagicMock(side_effect=parts)  # Directly mock `_recv` on the instance

		# Invoke `direct_recv_from` to test its behavior.
		packet = client.direct_recv_from()

		# Verify `_recv` was called the correct number of times.
		self.assertEqual(client._recv.call_count, len(parts))

		# Construct the expected message by joining the parts and removing sum stuff.
		expected_message = "".join(parts)
		expected_message = expected_message[expected_message.find(client._split_char)+1:]
		expected_message = expected_message[:expected_message.find(client._suffix)]

		# Construct the expected header.
		expected_header = json.loads(PacketHeader(a="b")())

		# Assert that the packet contains the expected message.
		self.assertEqual(packet.msg, expected_message)
		self.assertEqual(packet.header, expected_header)

		# Assert that the packet's splitter are as expected.
		self.assertEqual(packet._splitter, client._split_char)

		# End of `test_direct_recv_from`



	@patch("supersocket.socket.socket")
	def test_compatible_handshake_on_server(self, mock_socket_class):
		# Making `supersocket.socket.socket` be a mocked object.
		mock_socket = MagicMock()
		mock_socket.accept = MagicMock(return_value=(mock_socket, "accept"))
		mock_socket_class.return_value = mock_socket

		server = Server("127.0.0.1", 12345, buffer_size=10)

		# Mocking the `socket.recv` to simulate receiving a handshake message.
		handshake_message = ""
		handshake_message += f"{str(server._encoding)}\u0001"
		handshake_message += f"{str(server._buffer_size)}\u0001"
		handshake_message += f"{str(server._suffix)}\u0001"
		handshake_message += f"{str(server._split_char)}"
		mock_socket.recv = MagicMock(return_value=handshake_message.encode(server._encoding))

		server.begin()

		# Verify that the server's handshake was handled correctly.
		self.assertTrue(server._handshake_completed)
		self.assertTrue(server._is_connected)

		# End of `test_compatible_handshake_on_server`



	@patch("supersocket.socket.socket")
	def test_incompatible_handshake_on_server(self, mock_socket_class):
		# Making `supersocket.socket.socket` be a mocked object.
		mock_socket = MagicMock()
		mock_socket_class.return_value = mock_socket

		server = Server("127.0.0.1", 12345, buffer_size=10)

		# Mocking the `socket.recv` to simulate receiving a handshake message.
		handshake_message = ""
		handshake_message += f"{str(server._encoding)}\u0001"
		handshake_message += f"8\u0001" # incompatible buffer size
		handshake_message += f"{str(server._suffix)}\u0001"
		handshake_message += f"{str(server._split_char)}"
		mock_socket.recv = MagicMock(return_value=handshake_message.encode(server._encoding))

		try:
			server.begin()
		except:
			pass

		# Verify that the server's handshake was handled correctly.
		try:
			_ = server._handshake_completed
			raise Exception("Server handshake should have failed.")
		except AttributeError:
			pass

		self.assertFalse(server._is_connected)

		# End of `test_incompatible_handshake_on_server`







if __name__ == "__main__":
    unittest.main()
