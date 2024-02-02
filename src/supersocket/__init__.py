import threading
import socket
import json
import time, datetime
from typing import Any

from outvar import OutputVar
from infoinject import infoinject



"""

TODO: make sure we're checkout the output of functions that could fail.

TODO: add support for dns names instead of just ip addresses.

TODO: implement the following feature.

- Saves on bandwidth by only sending the header when it changes. This module does not however save on bandwidth on the
	message itself.
	This is because the message should be quick to access and modify, and since the message is usually larger than 
	the header, it would take too much time to compress it.\n

TODO: add support for a range of ports instead of just one port.

This means having a connection id. the same id must be on the client and the server.
During the handshake, they will both agree on the id and if the id does not match, the connection will be refused.

TODO: add reconnecting feature.

if the connection is lost unexpectedly, the client will try to reconnect to the server.

TODO: make it easy to incorporate state persistance for reconnecting.

Say the client is playing a game and the connection is lost.
Once reconnected, the client will need to know what state the game was in before the connection was lost.

Not having this feature in a game is really easy to mess up so we need to make an api that encapsulates and encourages
this feature.

TODO: add detailed logging system.

TODO: add support for multiple clients.

TODO: add support for a server pool. kind of like a load balancer.

A server pool will have a central server that will redirect clients to other servers in the pool.
This will allow for a lot of clients to connect to the server pool without overloading one specific server.

- The goal is to make it seem like a single server is handling all the clients.
- We will abstract away the server pool so that, when using the api, it will seem like a single server is handling all
	the clients.

TODO: after all this bs, rewrite the entire thing in rust and make a python wrapper for it.

"""




def STOP_SOCK(s:socket.socket, out_done:"OutputVar[bool]"):
	s.close()
	out_done.set(True)




class PacketHeader:
	def __init__(self, **kwargs):
		if "__from_string" in kwargs:
			self._json:"str" = kwargs["__from_string"]
			return
		self._json = json.dumps(kwargs)

	def __call__(self, *args, **kwargs) -> str:
		if len(args) != 0 or len(kwargs) != 0:
			raise Exception("`PacketHeader.__call__` does not support *args or **kwargs")
		return self._json

	@staticmethod
	def Empty() -> 'PacketHeader':
		return PacketHeader()



class Packet:
	def __init__(self, msg:str, header:'PacketHeader'=PacketHeader.Empty(), splitter:str='\U000f0000'):
		self.header:Any = json.loads(header())
		self.msg:str = msg
		self._splitter = splitter

	def decode_to_string(self, do_repr_splitter=False) -> str:
		return f"{self.header}{repr(self._splitter) if do_repr_splitter else self._splitter}{self.msg}"

	@staticmethod
	def Empty() -> 'Packet':
		ret = Packet("", header=PacketHeader(), splitter='\U000f0000')
		assert type(ret) is Packet
		return ret

	@classmethod
	def encode_to_packet(cls, pkt_string:str, split_char:str='\U000f0000') -> 'Packet':
		x = pkt_string.split(split_char)
		if len(x) == 1:
			return Packet(x[0], header=PacketHeader(), splitter=split_char)
		h = PacketHeader(__from_string=x[0])
		
		return Packet(x[1], header=h, splitter=split_char)



EmptyPacket = Packet("", header=PacketHeader(), splitter='\U000f0000')



class ANetworkManipulator:
	def _default_recv_callback(self, packet:Packet) -> Packet:
		return packet

	def _default_send_callback(self, packet:Packet) -> Packet:
		return packet
	
	def _decode_msg(self, msg:bytes) -> str:
		return msg.decode(self._encoding)
	
	def _encode_msg(self, msg:str) -> bytes:
		return msg.encode(self._encoding)
	
	def _recv(self) -> str:
		return self._decode_msg(self._sock.recv(self._buffer_size))
	
	def _send(self, packet:Packet) -> None:
		self._sock.sendall(self._encode_msg(f"{packet.decode_to_string()}{self._suffix}"))

	def define_recv_callback(self, callback) -> None:
		self._recv_callback = callback

	def define_send_callback(self, callback) -> None:
		self._send_callback = callback

	def __init__(self,
			bindable_address:"str", bindable_port:"int", encoding: "str"="utf-8", 
			buffer_size:"int"=512, suffix: "str|None"=None, split_char:"str|None"=None
	) -> None:
		if suffix is None:
			suffix = '\x00'
		if split_char is None:
			split_char = '\U000f0000'

		self._bindable_address = bindable_address
		self._bindable_port = bindable_port
		self._encoding = encoding
		self._buffer_size = buffer_size
		self._suffix = suffix
		self._split_char = split_char

		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self._recv_callback = self._default_recv_callback
		self._send_callback = self._default_send_callback

		self.DEBUGGING = False

		self._is_connected = False

		if self._handle_handshake is None: # type:ignore
			err_msg = ""
			err_msg += "Any child class of `ANetworkManipulator` must implement the `_handle_handshake` "
			err_msg += "method"
			raise Exception(err_msg)
		if self._handle_post_handshake is None: # type:ignore
			err_msg = ""
			err_msg += "Any child class of `ANetworkManipulator` must implement the "
			err_msg += "`_handle_post_handshake` method"
			raise Exception(err_msg)

	def SET_DEBUGGING(self) -> None:
		self.DEBUGGING = True

	def log(self, *args, **kwargs) -> None:
		end = "\n"
		if "end" in kwargs:
			end = kwargs["end"]
		t = datetime.datetime.now()
		msg = ""
		msg += f"[{t.date()} - {t.hour}:{t.minute}:{t.second}] ::: "
		msg += " ".join([str(x) for x in args])
		msg += end
		print(msg, end="")

	@infoinject.inject_debug_info([
		{
		"line": 1, "prefix": "\t",
		"x": "print(f\"`ANetworkManipulator.specify_socket_args` called with args={args} and kwargs={kwargs}.\")",
		}
	])
	def specify_socket_args(self, *args, **kwargs) -> None:
		if self.DEBUGGING:
			self.log(f"`ANetworkManipulator.specify_socket_args` called with args={args} and kwargs={kwargs}.")
		self._sock = socket.socket(*args, **kwargs)
		if self.DEBUGGING: self.log(f"`ANetworkManipulator.specify_socket_args` done.")

	def end(self, out_done:"OutputVar[bool]", non_blocking:bool=False) -> "threading.Thread|None":
		global STOP_SOCK
		if self.DEBUGGING: self.log(f"`ANetworkManipulator.end` called with out_done={out_done} and non_blocking={non_blocking}.")
		proc = None
		if non_blocking:
			proc = threading.Thread(target=STOP_SOCK, args=(self._sock, out_done))
			proc.start()
		else:
			self._sock.close()
			out_done.set(True)
		if self.DEBUGGING: self.log(f"`ANetworkManipulator.end` done.")
		return proc

	def recv(self, out_packet:OutputVar[Packet]) -> None:
		if self.DEBUGGING: self.log(f"`ANetworkManipulator.recv` called with out_packet={out_packet}.")
		if type(out_packet) is not OutputVar:
			raise TypeError(f"Expected type `OutputVar`, got type `{type(out_packet)}`")
		if type(out_packet()) is not Packet:
			raise TypeError(f"Expected type `Packet`, got type `{type(out_packet())}`")

		msgs = [self._recv()]
		while not msgs[len(msgs)-1].endswith(self._suffix):
			msgs.append(self._recv())
		msg = ""
		for m in msgs:
			msg += m
		if self.DEBUGGING: self.log(f"MSG: \t [{repr(msg)}]")
		header, msg = msg.split(self._split_char)
		if repr(header) == "{}":
			pkt = Packet(msg.strip(self._suffix), header=PacketHeader(), splitter=self._split_char)
		else:
			pkt = Packet(msg.strip(self._suffix), header=PacketHeader(__from_string=header), splitter=self._split_char)
		if self.DEBUGGING: self.log(f"`ANetworkManipulator.recv` done.")
		return out_packet.set(self._recv_callback(pkt))

	def send(self, packet:Packet) -> None:
		if self.DEBUGGING: self.log(f"`ANetworkManipulator.send` called with packet={packet}.")
		if type(packet) is not Packet:
			raise TypeError(f"Expected type `Packet`, got type `{type(packet)}`")
		
		p = self._send_callback(packet)
		self._send(p)
		if self.DEBUGGING: self.log(f"`ANetworkManipulator.send` done.")







class Client (ANetworkManipulator):
	"""
	A client for the `SocketWrapper` module.

	Features:` \n
		- Set your own encoding.\n
		- Don't worry about buffer sizes anymore as the module, when receiving, will wait until receiving the suffix. Once the suffix is
			received, the module will stop receiving and return the message.\n
		- Set your own suffix.\n
		- Set your own split char. The split char is the character that splits the header and the message.\n
		- Packet class makes life easier by allowing you to send headers and messages in one packet.\n
		- Set *args and **kwargs for the socket object.\n
		- Set callbacks for receiving and sending.\n
			\t- The callback for sending will be called before sending the packet, allowing you to modify the packet before sending it.\n
			\t- The callback for receiving will be called after receiving the packet, allowing you to modify the packet after receiving it.\n
			\t- Each callback will be called every time a packet is sent/received.\n
		- Handshake system to make sure the server and the client are compatible.\n
		- Saves on bandwidth by only sending the header when it changes. This module does not however save on bandwidth on the message
			itself. This is because the message should be quick to access and modify, and since the message is usually larger than the
			header, it would take too much time to compress it.\n
	`
	"""

	def __init__(self,
			bindable_address:"str", bindable_port:"int",
			encoding: "str"="utf-8", buffer_size:"int"=512, suffix: "str|None"=None, split_char:"str|None"=None
	) -> None:
		super().__init__(
			bindable_address, bindable_port,
			encoding, buffer_size, suffix, split_char
		)

	def _handle_handshake(self) -> None:
		if self.DEBUGGING: self.log(f"`Client._handle_handshake` called.")
		s = socket.socket()
		
		# sometimes the client will connect before the server is ready, so we need to wait for the server to be ready.
		retries = 10
		while retries > 0:
			try:
				s.connect((self._bindable_address, self._bindable_port+1))
				break
			except ConnectionRefusedError as e:
				time.sleep(0.5)
				print(f"`Client._handle_handshake`: {e}")
				retries -= 1
		if retries <= 0:
			raise ConnectionRefusedError("The server is not ready to accept connections.")
		
		r_msg = s.recv(1024).decode('utf-8')
		encoding, buffer_size, suffix, split_char = r_msg.split('\u0001')

		s_msg = ""
		s_msg += str(self._encoding)
		s_msg += "\u0001"
		s_msg += str(self._buffer_size)
		s_msg += "\u0001"
		s_msg += str(self._suffix)
		s_msg += "\u0001"
		s_msg += str(self._split_char)

		s.sendall(s_msg.encode('utf-8'))

		s.close()

		if str(encoding) != (self._encoding):
			raise ValueError(f"Encoding mismatch: expected [{repr(self._encoding)}], got [{repr(encoding)}]")
		if str(buffer_size) != str(self._buffer_size):
			raise ValueError(f"Buffer size mismatch: expected [{repr(self._buffer_size)}], got [{repr(buffer_size)}]")
		if str(suffix) != str(self._suffix):
			raise ValueError(f"Suffix mismatch: expected [{repr(self._suffix)}], got [{repr(suffix)}]")
		if str(split_char) != str(self._split_char):
			raise ValueError(f"Split char mismatch: expected [{repr(self._split_char)}], got [{repr(split_char)}]")
		
		if self.DEBUGGING: self.log(f"`Client._handle_handshake` done.")
	
	def _handle_post_handshake(self) -> None:
		if self.DEBUGGING: self.log(f"`Client._handle_post_handshake` called.")
		self._handshake_completed = True
		# Sometimes the server will not be ready to accept connections, so we need to wait for it to be ready.
		retries = 10
		while retries > 0:
			try:
				time.sleep(0.5)
				self._sock.connect((self._bindable_address, self._bindable_port))
				break
			except Exception as e:
				print(f"`Client._handle_post_handshake`: {e}")
				retries -= 1
		if retries <= 0:
			raise ConnectionRefusedError("The server is not ready to accept connections.")
		self._is_connected = True
		if self.DEBUGGING: self.log(f"`Client._handle_post_handshake` done.")

	def begin(self) -> None:
		if self.DEBUGGING: self.log(f"`Client.begin` called.")
		self._handle_handshake()
		self._handle_post_handshake()
		if self.DEBUGGING: self.log(f"`Client.begin` done.")

	def wait_for_connection(self) -> None:
		if self.DEBUGGING: self.log(f"`Client.wait_for_connection` called.")
		while not self._is_connected:
			time.sleep(0.01)
		if self.DEBUGGING: self.log(f"`Client.wait_for_connection` done.")







class Server (ANetworkManipulator):
	"""
	A server for the `SocketWrapper` module.

	Features:` \n
		- Set your own encoding.\n
		- Don't worry about buffer sizes anymore as the module, when receiving, will wait until receiving the suffix. Once the suffix is
			received, the module will stop receiving and return the message.\n
		- Set your own suffix.\n
		- Set your own split char. The split char is the character that splits the header and the message.\n
		- Packet class makes life easier by allowing you to send headers and messages in one packet.\n
		- Set *args and **kwargs for the socket object.\n
		- Set callbacks for receiving and sending.\n
			\t- The callback for sending will be called before sending the packet, allowing you to modify the packet before sending it.\n
			\t- The callback for receiving will be called after receiving the packet, allowing you to modify the packet after receiving it.\n
			\t- Each callback will be called every time a packet is sent/received.\n
		- Handshake system to make sure the server and the client are compatible.\n
		- Saves on bandwidth by only sending the header when it changes. This module does not however save on bandwidth on the message
			itself. This is because the message should be quick to access and modify, and since the message is usually larger than the
			header, it would take too much time to compress it.\n
	`
	"""

	def __init__(self,
			bindable_address:"str", bindable_port:"int", backlog:"int"=1,
			encoding: "str"="utf-8", buffer_size:"int"=512, suffix: "str|None"=None, split_char:"str|None"=None
	) -> None:
		super().__init__(
			bindable_address, bindable_port,
			encoding, buffer_size, suffix, split_char
		)
		self._backlog = backlog
		self._accepted_addr:"tuple|None" = None

	def _handle_handshake(self) -> None:
		if self.DEBUGGING: self.log(f"`Server._handle_handshake` called.")
		s = socket.socket()
		s.bind((self._bindable_address, self._bindable_port+1))
		s.listen()
		sock, _ = s.accept()

		s_msg = ""
		s_msg += str(self._encoding)
		s_msg += "\u0001"
		s_msg += str(self._buffer_size)
		s_msg += "\u0001"
		s_msg += str(self._suffix)
		s_msg += "\u0001"
		s_msg += str(self._split_char)

		sock.sendall(s_msg.encode('utf-8'))

		r_msg = sock.recv(1024).decode('utf-8')
		encoding, buffer_size, suffix, split_char = r_msg.split('\u0001')

		s.close()
		sock.close()

		if str(encoding) != str(self._encoding):
			raise ValueError(f"Encoding mismatch: expected [{repr(self._encoding)}], got [{repr(encoding)}]")
		if str(buffer_size) != str(self._buffer_size):
			raise ValueError(f"Buffer size mismatch: expected [{repr(self._buffer_size)}], got [{repr(buffer_size)}]")
		if str(suffix) != str(self._suffix):
			raise ValueError(f"Suffix mismatch: expected [{repr(self._suffix)}], got [{repr(suffix)}]")
		if str(split_char) != str(self._split_char):
			raise ValueError(f"Split char mismatch: expected [{repr(self._split_char)}], got [{repr(split_char)}]")
	
		if self.DEBUGGING: self.log(f"`Server._handle_handshake` done.")
		
	def _handle_post_handshake(self) -> None:
		if self.DEBUGGING: self.log(f"`Server._handle_post_handshake` called.")
		self._handshake_completed = True
		self._sock.bind((self._bindable_address, self._bindable_port))
		if self.DEBUGGING: self.log(f"`Server._handle_post_handshake` attempting to listen.")
		self._sock.listen(self._backlog)
		self._sock, self._accepted_addr = self._sock.accept()
		self._is_connected = True
		if self.DEBUGGING: self.log(f"`Server._handle_post_handshake` done.")

	def begin(self) -> None:
		if self.DEBUGGING: self.log(f"`Server.begin` called.")
		self._handle_handshake()
		self._handle_post_handshake()
		if self.DEBUGGING: self.log(f"`Server.begin` done.")

	def wait_for_connection(self) -> None:
		if self.DEBUGGING: self.log(f"`Server.wait_for_connection` called.")

		while not self._is_connected:
			time.sleep(0.01)

		if self.DEBUGGING: self.log(f"`Server.wait_for_connection` done.")