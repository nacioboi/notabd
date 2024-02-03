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
		print(f"\x1b[31m Test {func.__name__} failed!! \x1b[1;31m \nErrors\x1b0m\x1b[31m: {e} \x1b[0m")
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
			return fib(n-1) + fib(n-2)
	
	fib(5)

#RUN_TEST(test_handshake)
#RUN_TEST(test_send_recv)
RUN_TEST(test_info_inject_1)

