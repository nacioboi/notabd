"""
# NOTE: DONT REMOVE THESE BLOCK COMMENTS.
from supersocket import Packet, Client, Server, PacketHeader, OutputVar
import time

# NOTE: THEY ARE BECAUSE WE'RE TESTING THE INFOINJECT MODULE, AND WE NEED TO MAKE SURE THE INFOINJECT MODULE IS WORKING PROPERLY.
# NOTE: AFTER WE TEST THE INFOINJECT MODULE, WE CAN RESUME USING THESE COMMENTED OUT CODE.
"""
def RUN_TEST(func):
	print(f"\n\n\n--\x1b[1;33m Running test: {func.__name__} \x1b[0m--")
	try:
		func()
	except Exception as e:
		print(f"\x1b[31m Test {func.__name__} failed!! \x1b[1;31m \nErrors\x1b[31m: {e} \x1b[0m")
		exit(1)
	print(f"--\x1b[1;32m Test {func.__name__} passed!! \x1b[0m--")
"""
# NOTE: DONT REMOVE THESE BLOCK COMMENTS.



# instead of creating server and clients on separate threads...
# we should use pythons built-in unittest module (it's actually pretty good for testing).
# the problem i've come across when trying to use it though is having the server and client communicate is impossible.
# i think the best way to do this is to have the server and client communicate through a file.
# if we run the server isolated, then save the appropriate state to a file, then pass this file to the client
#   (again, isolated), it should solve the problem.
def test_handshake() -> bool:
	try:
		server = Server("127.0.0.1", 3000)
		client = Client("127.0.0.1", 3000)

		#server.SET_DEBUGGING()
		#client.SET_DEBUGGING()

		t1 = threading.Thread(target=server.begin)
		t2 = threading.Thread(target=client.begin)

		t1.start()
		time.sleep(2)
		t2.start()

		t1.join()
		t2.join()

		server_done = OutputVar[bool](False)
		client_done = OutputVar[bool](False)
		server.end(server_done)
		client.end(client_done)
	except Exception as e:
		print(e)
		return False
	
	return True




def _server_test_send_recv(server):
	#server.SET_DEBUGGING()
	server.begin()
	server.wait_for_connection()
	server.send(Packet("Hello, client!"))
	out_packet = OutputVar[Packet](Packet.Empty())
	server.recv(out_packet)
	print(out_packet().msg)



def _client_test_send_recv(client):
	#client.SET_DEBUGGING()
	time.sleep(1)
	client.begin()
	out_packet = OutputVar[Packet](Packet.Empty())
	client.recv(out_packet)
	print(out_packet().msg)
	client.send(Packet("Hello, server!"))



def test_send_recv() -> bool:
	try:
		server = Server("127.0.0.1", 60000)
		client = Client("127.0.0.1", 60000)

		t1 = threading.Thread(target=_server_test_send_recv, args=(server,))
		t2 = threading.Thread(target=_client_test_send_recv, args=(client,))

		t1.start()
		time.sleep(1)
		t2.start()

		t1.join()
		t2.join()

		server_done = OutputVar[bool](False)
		client_done = OutputVar[bool](False)
		server.end(server_done)
		client.end(client_done)
	except Exception as e:
		print(e)
		return False

	return True



\"""
TODO: 	MORE TESTS:

1. Test sending more than the buffer size.
2. Test sending a packet with a header larger than the buffer size.
3. Test sending a packet with the split char in the message or head.
5. Test sending a packet with the suffix char in the message or head.
6. Test sending unicode characters.
7. Test changing the buffer size to 4 bytes.
8. Test changing the callbacks.
7. Test a different type of socket.

# NOTE: THEY ARE BECAUSE WE'RE TESTING THE INFOINJECT MODULE, AND WE NEED TO MAKE SURE THE INFOINJECT MODULE IS WORKING PROPERLY.
# NOTE: AFTER WE TEST THE INFOINJECT MODULE, WE CAN RESUME USING THESE COMMENTED OUT CODE.
"""

import os

# Firstly, disable the infoinject openai integration.
# It's a bit of a hack, but it works, I just wanted the errors to go away.
with open(".DISABLE_OPENAI", "w") as f: pass
from infoinject import InfoInjector
os.remove(".DISABLE_OPENAI")

def test_info_inject_1():
	@InfoInjector.inject_debug_info([
		{
			"line": 1,
			"x":
			[
			"print(f'a = {a}')",
			"print(f'b = {b}')"
			]
		}
	])
	def add(a, b):
		return a + b

	print(add(1,2))

def test_info_inject_2():
	@InfoInjector.inject_debug_info([
		{
			"line": 1,
			"x":
			[
			"print(f'n = {n}')",
			]
		},
		{
			"line": 2,
			"x":
			[
			"\tprint(f'n <= 1 = {n <= 1}')",
			]
		},
		{
			"line": 4,
			"x":
			[
			"\tprint(f'fib(n-2) = {fib(n-2)}')",
			]
		}
	])
	def fib(n):
		if n <= 1:
			return n
		else:
			new = fib(n-1) + fib(n-2)
			return new
	
	fib(5)

#RUN_TEST(test_handshake)
#RUN_TEST(test_send_recv)
#RUN_TEST(test_info_inject_2)
	


# testing the ptysocket module.
	
from ptysocket import PtySocketServer, PtySocketClient, PtySocketClientMode
from supersocket import Packet

from pynput.keyboard import Key, KeyCode, Listener
import threading
import termios
import time
import sys
import tty



SCRIPT_STARTED_TIME = time.time()



SERVER = None
CLIENT = None



def disable_echo():
	# Get the current terminal settings
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	
	# Copy the current settings to make modifications
	new_settings = termios.tcgetattr(fd)
	
	# Turn off echo
	new_settings[3] = new_settings[3] & ~termios.ECHO
	
	# Apply the new settings
	termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
	
	return old_settings



def restore_settings(old_settings):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



def server_handle():

	global SERVER

	server = PtySocketServer("127.0.0.1", 3100)

	SERVER = server

	server.begin()
	server.wait_for_exit()

	# End of `server_handle`.



def client_handle():
	global CLIENT, SCRIPT_STARTED_TIME
	time.sleep(3)
	old_settings = disable_echo()
	try:
		
		client = PtySocketClient("127.0.0.1", 3100, PtySocketClientMode.API)

		CLIENT = client

		def p(pkt:"Packet"):
			with open(f"log/{SCRIPT_STARTED_TIME}.log", "a") as f:
				f.write(f"|{pkt.msg}") # NOTE: FOR DEBUGGING
			msg = pkt.msg
			if msg == "\x1b[?2004l":
				# This has been causing problems...
				# This escape sequence is to do with bracketed paste mode in xterm.
				# We dont need to print it to screen, so just ignore it...
				return
			# TODO: fix "too many values to unpack"
			assert isinstance(msg, str) # tried to see if it was not a string, but it is.
			print(msg, end="", flush=True)

		client.on_receive_callback = p

		client.begin()
		client.wait_for_exit()
	
	finally:
		restore_settings(old_settings)
	# End of `client_handle`.



SHIFT_IS_DOWN = False



def on_press(key:"Key|KeyCode|None"):
	global CLIENT, SHIFT_IS_DOWN
	
	char = None
	if isinstance(key, Key):
		# we need to handle all of these:
		# - alt', 'alt_l', 'alt_r', 'alt_gr', 'backspace', 'caps_lock', 'cmd', 'cmd_l', 'cmd_r',
		# - 'ctrl', 'ctrl_l', 'ctrl_r', 'delete', 'down', 'end', 'enter', 'esc',
		# - 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
		# - 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20',
		# - 'home', 'left', 'page_down', 'page_up', 'right', 'shift', 'shift_l', 'shift_r', 'space', 'tab', 'up',
		# - 'media_play_pause', 'media_volume_mute', 'media_volume_down', 'media_volume_up',
		# -'media_previous', 'media_next', 'insert', 'menu', 'num_lock', 'pause', 'print_screen', 'scroll_lock'
		if key.name in 	[
					"alt", "alt_l", "alt_r", "alt_gr", "caps_lock", "cmd", "cmd_l", "cmd_r",
					"ctrl", "ctrl_l", "ctrl_r", "end",
					"f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
					"f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20",
					"home", "page_down", "page_up",
					"media_play_pause", "media_volume_mute", "media_volume_down",
					"media_volume_up", "media_previous", "media_next",
					"insert", "menu", "num_lock", "pause", "print_screen", "scroll_lock"
				]:
			raise NotImplementedError(f"Key [{key.name}] not supported yet. Please just dont press it.")
		elif key.name == "backspace":
			char = "\b"
		elif key.name == "delete":
			char = "\x7f"
		elif key.name == "down":
			char = "\x1b[B"
		elif key.name == "enter":
			char = "\n"
		elif key.name == "esc":
			char = "\x1b"
		elif key.name == "left":
			char = "\x1b[D"
		elif key.name == "right":
			char = "\x1b[C"
		elif key.name in ["shift", "shift_l", "shift_r"]:
			SHIFT_IS_DOWN = True
			return
		elif key.name == "space":
			char = " "
		elif key.name == "tab":
			char = "\t"
		elif key.name == "up":
			char = "\x1b[A"
		else:
			raise Exception(f"Unknown key: {key.name}")
	elif isinstance(key, KeyCode):
		char = key.char
	else:
		return
		
	assert CLIENT is not None
	assert char is not None

	CLIENT.enqueue_command(char)

	# End of `on_press`.



def on_release(key):
	global SHIFT_IS_DOWN

	if key in [Key.shift, Key.shift_l, Key.shift_r]:
		SHIFT_IS_DOWN = False

	# End of `on_release`.



st = threading.Thread(target=server_handle)
ct = threading.Thread(target=client_handle)

st.start()
ct.start()



# Start listening for keypress
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()



def foo():
	global CLIENT

	assert CLIENT is not None




st.join()
ct.join()
