# A simple chat terminal app.



from supersocket import Client, ServerRepresentative, Packet
from outvar import OutputVar

import re



def get_connectable_addr() -> "str":
	
	valid_ip = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

	addr = input("Enter the address to connect to: ")
	if valid_ip.match(addr):
		return addr
	else:
		return get_connectable_addr()
	
	# End of `get_connectable_addr`.



def get_connectable_port() -> "int":

	valid_port = re.compile(r"^[0-9]{1,5}$")

	port = input("Enter the port to connect to: ")
	if valid_port.match(port):
		return int(port)
	else:
		return get_connectable_port()
	
	# End of `get_connectable_port`.



def make_client() -> "Client":
	
	addr = get_connectable_addr()
	port = get_connectable_port()

	return Client(addr, port)

	# End of `make_client`.



def chat_loop(server:"ServerRepresentative"):

	while True:

		# RECEIVING...
		
		pkt = OutputVar[Packet](Packet.Empty())
		server.recv_from(pkt)

		if pkt().msg == "/exit":
			print("The other user has left the chat.")
			break

		print(f"Them: {pkt().msg}")

		# SENDING...

		message = input("You: ")

		if message == "/exit":
			pkt = Packet("/exit")
			server.send_to(pkt)
			break

		server.send_to(Packet(message))

	# End of `chat_loop`.
		


def main():
	
	client = make_client()

	client.begin()
	server_representative = client.wait_for_connection()

	print("To exit the chat, type '/exit' and press enter.")
	chat_loop(server_representative)

	print("Exiting...")

	# End of `main`.



if __name__ == "__main__": main()