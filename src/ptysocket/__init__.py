"""
ptysocket is a library that provides a simple way to control a terminal from machine a where the terminal is running 
on machine b.
"""

from supersocket import Packet, Client, Server, OutputVar, ClientRepresentative, ServerRepresentative
from outvar import OutputVar

from typing import Callable
from enum import Enum
from queue import Queue
import threading
import select
import time
import os




# NOTE: FOR DEBUGGING
import datetime
SCRIPT_STARTED_TIME = datetime.datetime.now().strftime("%d-%m-%Y_%H.%M.%S")



class PtySocketServer:



	def __init__(self, acceptable_ip: "str", port: int) -> None:

		self._server = Server(acceptable_ip, port)
		self._server.DEBUGGING = False
		self._pty_master, self._pty_slave = None, None

		self.is_running = False

		# End of `__init__`



	def _setup_pty(self):

		master_fd, slave_fd = os.openpty()

		pid = os.fork()

		if pid == 0:  # Child process
			# Set the slave FD as the process's controlling terminal
			os.setsid()
			os.dup2(slave_fd, 0)  # STDIN
			os.dup2(slave_fd, 1)  # STDOUT
			os.dup2(slave_fd, 2)  # STDERR

			# Close file descriptors
			os.close(slave_fd)
			os.close(master_fd)

			# Execute zsh
			os.execv('/bin/zsh', ['zsh'])
		else:  # Parent process
			self._pty_master = master_fd
			self._pty_slave = slave_fd

		self.is_running = True

		# End of `_setup_pty`



	def begin(self) -> None:

		self.is_running = True
		self._setup_pty()

		self._server.begin()
		client_rep:"ClientRepresentative" = self._server.wait_for_connection()
		self._server_rep = None

		self.read_thread = threading.Thread(target=self._read_from_pty_and_send, args=(client_rep,), daemon=True)
		self.write_thread = threading.Thread(target=self._receive_and_write_to_pty, args=(client_rep,), daemon=True)

		self.read_thread.start()
		self.write_thread.start()

		# End of `begin`

	

	def wait_for_exit(self) -> None:
		while self.is_running:
			time.sleep(0.1)
		self.read_thread.join()
		self.write_thread.join()

		# End of `wait_for_exit`


	def _read_from_pty_and_send(self, client_rep:"Client"):
		assert self._pty_master is not None
		while self.is_running:
			r, w, e = select.select([self._pty_master], [], [], 0.1)
			if self._pty_master in r:
				output = os.read(self._pty_master, 1024)
				pkt = Packet(output.decode())
				client_rep.send_to(pkt)

		print("Exiting _read_from_pty_and_send")


	def _receive_and_write_to_pty(self, client_rep: "Client"):
		assert self._pty_master is not None
		while self.is_running:
			pkt = OutputVar[Packet](Packet.Empty())
			client_rep.recv_from(pkt)
			data = pkt().msg
			print(f"Received data: {repr(data)}")
			if data:
				os.write(self._pty_master, data.encode())
		
		print("Exiting _receive_and_write_to_pty")






class PtySocketClientMode(Enum):

	TAKEOVER = 0
	API = 1



class PtySocketClient:



	def __init__(self, ip: str, port: int, mode:"PtySocketClientMode"=PtySocketClientMode.TAKEOVER) -> None:

		self._client = Client(ip, port)
		self._client.DEBUGGING = False
		self._mode = mode
		self.is_running = False

		self.on_connect_callback = None
		self.on_disconnect_callback = None
		self.on_receive_callback = None

		self.command_queue = Queue()

		# End of `__init__`



	def set_on_receive_callback(self, callback: "Callable[[Packet], None]") -> None:
		self.on_receive_callback = callback

		# End of `set_on_receive_callback`

	
	def begin(self) -> None:
		try:

			self.is_running = True

			assert self._client is not None
			self._client.begin()
			self._server_rep = self._client.wait_for_connection()
			self._client = None
			if self.on_connect_callback is not None:
				self.on_connect_callback()
			
			if self._mode == PtySocketClientMode.TAKEOVER:
				pass
				#self.start_takeover_mode()
			elif self._mode == PtySocketClientMode.API:
				self._start_api_mode()

		except Exception as e:
			if self.on_disconnect_callback:
				self.on_disconnect_callback(e)
		# End of `begin`
				
	

	def _start_api_mode(self) -> None:

		self.output_thread = threading.Thread(target=self._receive_output_loop, daemon=True)
		self.command_sender_thread = threading.Thread(target=self._send_commands_from_queue, daemon=True)
		
		self.output_thread.start()
		self.command_sender_thread.start()

		# End of `start_takeover_mode`



	def wait_for_exit(self) -> None:

		while self.is_running:
			time.sleep(0.1)

		self.output_thread.join()
		self.command_sender_thread.join()

		# End of `wait_for_exit`



	###########
	# helpers #
	###########



	def enqueue_command(self, command: str):
		       
		self.command_queue.put(command)

		# End of `enqueue_command`



	def send_command(self, command: str) -> None:

		packet = Packet(command)
		self._server_rep.send_to(packet)

		# End of `send_command`



	def _send_commands_from_queue(self) -> None:

		while self.is_running:
			if not self.command_queue.empty():
				command = self.command_queue.get()
				self.send_command(command)
				self.command_queue.task_done()
			else:
				time.sleep(0.1)


		# End of `_send_commands_from_queue`


	def _receive_output_loop(self) -> None:
		global OLD_PRINT
		while self.is_running:
			#self._client.DEBUGGING = True
			def new_print(*args, **kwargs):
				with open(f"log/{SCRIPT_STARTED_TIME}.log", "a") as f:
					f.write(f"[[[ {args} ]]]\n")
			print = new_print
			try:

				# Assuming self.client.recv() is blocking and waits for data to arrive
				# NOTE: FOR DEBUGGING
				#with open(f"log/{SCRIPT_STARTED_TIME}.log", "a") as f:
				#	f.write(f"[[[ waiting for data ]]]\n")
				# TODO: VERY IMPORTANT, FOUND ERROR HERE.
				# NOTE: the cause of the "too many values to unpack (expected 2)" error is the fault of
				# 	  the supersocket module.
				pkt = OutputVar[Packet](Packet.Empty())
				self._server_rep.recv_from(pkt)  # Adjust based on your Client class implementation
				with open(f"log/{SCRIPT_STARTED_TIME}.log", "a") as f:
					f.write(f"[[[ received data - msg,hdr:({pkt().msg}),({pkt().header}) ]]]\n")
				if self.on_receive_callback:
					self.on_receive_callback(pkt())

			except Exception as e:
				print(f"Error receiving data: {e}")
				# Optionally, you can call the on_disconnect callback here if the error indicates a disconnect.
				if self.on_disconnect_callback:
					self.on_disconnect_callback(e)
				break  # Exit the loop if an error occurs
		# End of `_receive_output`