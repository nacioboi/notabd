from ptysocket import Packet, Client, Server, PacketHeader, OutputVar  # Replace 'your_module' with the actual name
import threading
import time



def test_handshake() -> bool:
	try:
		server = Server("127.0.0.1", 3000)
		client = Client("127.0.0.1", 3000)

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
	server.SET_DEBUGGING()
	server.begin()
	server.wait_for_connection()
	server.send(Packet("Hello, client!"))
	out_packet = OutputVar[Packet](Packet.EmptyPacket())
	print(server.recv(out_packet))



def _client_test_send_recv(client):
	client.SET_DEBUGGING()
	time.sleep(5)
	client.begin()
	out_packet = OutputVar[Packet](Packet.EmptyPacket())
	print(client.recv(out_packet))
	client.send(Packet("Hello, server!"))



def test_send_recv() -> bool:
	try:
		server = Server("127.0.0.1", 3101)
		client = Client("127.0.0.1", 3101)

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





if not test_handshake():
	print("Handshake test failed!")
	exit(1)

if not test_send_recv():
	print("Send/Recv test failed!")
	exit(1)

