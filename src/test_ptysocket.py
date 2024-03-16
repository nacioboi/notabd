from ptysocket import PtySocketServer, PtySocketClient, PtySocketClientMode
from supersocket import Packet

from pynput.keyboard import Key, KeyCode, Listener
import threading
import datetime
import termios
import time
import sys
import tty



SCRIPT_STARTED_TIME = datetime.datetime.now().strftime("%d-%m-%Y_%H.%M.%S")



SERVER = None
CLIENT = None

PORT = 3110



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

	# End of `disable_echo`.



def restore_settings(old_settings):

    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # End of `restore_settings`.



def server_handle():

	global SERVER, PORT

	server = PtySocketServer("127.0.0.1", PORT)


	SERVER = server

	server.begin()
	print("ok")
	server.wait_for_exit()

	# End of `server_handle`.



def client_handle():
	global CLIENT, SCRIPT_STARTED_TIME, PORT
	time.sleep(3)
	old_settings = disable_echo()
	try:
		
		client = PtySocketClient("127.0.0.1", PORT, PtySocketClientMode.API)

		CLIENT = client

		def p(pkt:"Packet"):
			with open(f"log/{SCRIPT_STARTED_TIME}.log", "a") as f:
				f.write(f"|{pkt.msg}") # NOTE: FOR DEBUGGING
			msg = pkt.msg
			if msg in ["\x1b[?2004l", "\x1b[?2004h"]:
				# This has been causing problems...
				# This escape sequence is to do with bracketed paste mode in xterm.
				# We dont need to print it to screen, so just ignore it...
				return
			# TODO: fix "too many values to unpack"
			assert isinstance(msg, str) # tried to see if it was not a string, but it is.
			print(msg, end="", flush=True)

		client.on_receive_callback = p

		client.begin()
		print("ok")
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
			print(f"Key [{key.name}] not supported yet. Please just dont press it.")
			return
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



def main(mode):

	t = None

	if mode == "server":
		t = threading.Thread(target=server_handle)
	else:
		t = threading.Thread(target=client_handle)

	assert t is not None
	t.start()

	# Start listening for keypress
	if mode == "client":
		listener = Listener(on_press=on_press, on_release=on_release)
		listener.start()

	time.sleep(600)
	t.join()
	if mode == "client":
		listener.stop()

	# End of `main`.



if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 test_ptysocket.py <mode>")
		print("  where <mode> is either 'server' or 'client'")
		sys.exit(1)

	mode = sys.argv[1]

	if mode not in ["server", "client"]:
		print(f"Invalid mode: {mode}")
		sys.exit(1)

	main(mode)