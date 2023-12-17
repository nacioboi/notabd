"""
from supersocket import Packet, Client, Server, PacketHeader, OutputVar  # Replace 'your_module' with the actual name
import threading
import time


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

"""

import infoinject

InfoInjector = infoinject.initialize(
	compilation_result_path="./compilation_result.json",
	dont_save_compilation=True,
)

def test_info_inject():
	@InfoInjector.inject_debug_info_using_AI("print the result of a and b")
	@InfoInjector.provide_test_args(1, 2)
	def add(a, b):
		return a + b

	add(1,2)

#RUN_TEST(test_handshake)
#RUN_TEST(test_send_recv)
RUN_TEST(test_info_inject)

