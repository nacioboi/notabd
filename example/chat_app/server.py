# A simple chat terminal app.



from supersocket import Server, ClientRepresentative, Packet
from outvar import OutputVar

import re



def get_bindable_addr() -> "str":

	valid_ip = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

	addr = input("Enter the address to bind to: ")
	if valid_ip.match(addr):
		return addr
	else:
		return get_bindable_addr()
	
	# End of `get_bindable_addr`.



def get_bindable_port() -> "int":

	valid_port = re.compile(r"^[0-9]{1,5}$")

	port = input("Enter the port to bind to: ")
	if valid_port.match(port):
		return int(port)
	else:
		return get_bindable_port()
	
	# End of `get_bindable_port`.



def make_server() -> "Server":

	addr = get_bindable_addr()
	port = get_bindable_port()

	return Server(addr, port)

	# End of `make_server`.



def chat_loop(client: "ClientRepresentative"):
	while True:
		
		# SENDING...

		message = input("You: ")

		if message == "/exit":
			pkt = Packet("/exit")
			client.send_to(pkt)
			break

		client.send_to(Packet(message))

		# RECEIVING...

		pkt = OutputVar[Packet](Packet.Empty())
		client.recv_from(pkt)

		if pkt().msg == "/exit":
			print("The other user has left the chat.")
			break

		print(f"Them: {pkt().msg}")

	# End of `chat_loop`.




def main():

	server = make_server()
	
	server.begin()
	client_representative = server.wait_for_connection()

	print("To exit, type, '/exit' and press enter.")
	chat_loop(client_representative)

	print("Exiting...")

	# End of `main`.



if __name__ == "__main__": main()