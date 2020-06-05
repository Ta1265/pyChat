import socket
import threading
import sys

HEADERSIZE = 10 #constant


######### Instructions ##########
#### To start a server procces pass 'server' as a command line argument 
#### example -> python3 pyChat.py server
#### If no argument passed, a client process will be created by default.
################################

class pyChat:

	def client_start(self, IP = '127.0.0.1', PORT = 1303):

		self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try: self.server_sock.connect((IP,PORT))
		except:
			print(f'Failed to connect to server on IP-{IP} : PORT-{PORT}, Exiting')
			return False

		userName = input("First enter your user name -> ")
		while(userName == ''):
			userName = input("No really give me a user name -> ")
		self.send_msg(sock = self.server_sock, msg = userName)
		
		myThread = threading.Thread(target= self.client_listen) #start new thread to listen for traffic
		myThread.daemon = True
		myThread.start()

		running = True #continuously take user input to send off 
		while running:
			userInput = input()
			print ("\033[A                             \033[A") # Makes chat look neater
			self.send_msg(sock = self.server_sock, msg = userInput)
			if userInput == 'EXIT': running = False

	def client_listen(self): # used by client to listen for traffic from the server
		while True:
			msg = self.get_msg(self.server_sock)
			if msg == -1:
				print("--- Server seems to be offline, disconnecting. ---")
				exit()
			else:
				print(msg)
				
	def server_start(self, IP = '127.0.0.1',  PORT = 1303, PASSKEY = '' ):
		self.PASSKEY = PASSKEY
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ##allows us to re-use the address somehow need to look more into it
		self.connections = []
		try: self.sock.bind((IP,PORT))
		except:
			print(f'Failed to bind to PORT-{PORT} : IP-{IP}, Exiting')
			return False
		self.sock.listen(5)
		print(f'--- pyChat Server started on IP-{IP} : PORT-{PORT} ---')
		self.server_acpt_con()

	def server_acpt_con(self):
		while True:
			client, address = self.sock.accept()
			myThread = threading.Thread(target=self.server_listen, args = (client, address ))
			myThread.daemon = True #main thread is not daemon, all others are
			myThread.start()
			self.connections.append(client)

	def server_listen(self, this_client_socket, address):
		userName = self.get_msg(this_client_socket)
		self.send_msg(sock = this_client_socket, msg = f'--- You have connected. Welcome to PyChat {userName}! Type EXIT to disconnect ---')
		self.server_blast_msg(sender_c  = this_client_socket, msg = f'--- {userName} has connection was made from: {address} ---')
		
		while True:
			msg = self.get_msg(this_client_socket)
			if msg == -1 or msg == 'EXIT':
				self.server_blast_msg(sender_c = this_client_socket, msg = f'--- {userName} has disconnected from pyChat. ---')
				self.connections.remove(this_client_socket)
				exit()
			else: self.server_blast_msg(sender_c = this_client_socket, msg = userName + " says-> " + msg)

	def server_blast_msg(self, sender_c, msg ):
		print("server: ", msg)
		for client in self.connections:
			self.send_msg(sock = client, msg = msg)

	def send_msg(self, sock, msg): # helper works with both client/server methods
		msg = (f'{len(msg):<{HEADERSIZE}}' + msg ).encode('UTF-8')
		try: sock.send(msg)
		except: print("--- Failed to send message ---")

	def get_msg(self,sock): # helper works with both client/server methods
		try:
			len_msg = (int(sock.recv(HEADERSIZE).decode('UTF-8').strip()))
			return sock.recv(len_msg).decode('UTF-8')
		except: return -1 # sock disconnected

def main():

	IP,PORT = '', ''
	IP = input("Enter IP (leave empty for default)")
	PORT = input("Enter PORT (leave empty for default)")
	
	#command line arguments
	if len(sys.argv) > 1 and sys.argv[1] == 'server':
		if IP != '' and PORT != '': pyChat().server_start(IP = IP, PORT = PORT)
		else: pyChat().server_start()
			
	#default to creating a client
	else:
		if IP != '' and PORT != '': pyChat().client_start(IP = IP, PORT = PORT)
		else: pyChat().client_start()

if __name__ == '__main__':
	main()