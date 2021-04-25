import socket
import time
import threading

class SocketServer:
	def __init__(self, port = 9999):
		self.host = socket.gethostname()
		self.port = port
		self.clientSocket = None
		self.lines = []
		self.temperature = 0
		self.humidity = 0
		self.thread = threading.Thread(target=self.listen)
		self.thread.start()

	def sendMessage(self,msg):
		if(not self.clientSocket):
			return False
		self.clientSocket.sendall(bytes(msg,'utf-8'))
		return True
	def receiveInfo(self):
		while True:
			msg = self.receiveMessage()
			self.lines = []
			for line in msg.split("\r\n"):
				self.lines.append(line)
				if "Temperature" in line and "Sensor" not in line:
					self.temperature = line.split(" ")[-1]
				if "Humidity" in line and "Sensor" not in line:
					self.humidity = line.split(" ")[-1]

	def receiveMessage(self):
		if(not self.clientSocket):
			return False
		return self.clientSocket.recv(1024).decode("utf-8")
	def listen(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		    s.bind((self.host, self.port))
		    s.listen()
		    while True:
			    # accept connections from outside
			    (self.clientSocket, self.clientAddress) = s.accept()
			    self.receiveThread = threading.Thread(target=self.receiveInfo)
			    self.receiveThread.start()


if __name__ == "__main__":
	serverSocket = SocketServer()
	while True:
		print(serverSocket.temperature)
		print(serverSocket.humidity)
		time.sleep(1)

