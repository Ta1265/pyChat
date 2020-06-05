import socket
import select #provides OS-Level monitoring of things, such as sockets
import threading

class pyChat_server:

	def __init__(self, HEADERSIZE = 10, IP = "127.0.0.1", PORT = 1217):
		self.HEADERSIZE = HEADERSIZE
		self.IP = IP
		self.PORT = PORT
		ip_port_tuple = (IP, PORT) #just to make myself remember .bind input type
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ##allows us to re-use the address somehow need to look more into it
		self.server_socket.bind(ip_port_tuple)
		self.server_socket.listen()

		self.socket_list = [self.server_socket]
		self.clientsDict = {} # {key = socket : data = user}
		print(f'pyChat server_socket initialized, Listening for connections on {IP} : {PORT}')


	def receive_message(self, client_socket):
		# Handle message receiving
		try:
			message_header = client_socket.recv(self.HEADERSIZE) # HEADERSIZE should be constant/same between server and clients
			if len(message_header) == 0: #if no header received, then client has exited
				print('message_header came back as 0 returning False')
				return False
			message_header = message_header.decode('UTF-8')
			message_header = message_header.strip() # remove spaces
			message_len = int(message_header)

			client_message = client_socket.recv(message_len) #receive the rest of the data

			client_data_dict = {'header': message_header, 'data': client_message}
			return client_data_dict

		except:
			# empty messege OR client exited
			print("Message was empty returning False")
			return False



	def accept_Connections(self):

		while True:
			print("?")
			client_socket, client_address = self.server_socket.accept()
			print("??")
			# a new user wants to make a connection
			if client_socket not in self.socket_list:
				print("???")
				client_socket.send(self.prepMsgToSend("Welcome to pyChat, what is you username? "))
				user = self.receive_message(client_socket)
				if user != False:
					self.socket_list.append(client_socket)
					self.clientsDict[client_socket] = user
					print('Accepted new Connection from {}:{}, User name: {}'.format(*client_address, user['data'].decode('UTF-8')))
				else:
					print("Failed to accept user")
			

				threadaccept_traffic

			# Exisiting user sent a message
			else:
				print("?????")
				message = self.receive_message(client_socket)

				if message != False:
					user = self.clientsDict[client_socket]
					userName = user['data'].decode('utf-8')
					said = message['data'].decode('utf-8')
					print("Received message from - ", userName,": ", said)

				# client has disconnected
				else:
					user = self.clientsDict[client_socket]
					userName = user['data'].decode('utf-8')
					print("Closed connection from: ",userName)
					self.sockets_list.remove(client_socket)
					del self.clientsDict[client_socket]





	def add_New_User(self, client_socket):

		user = self.receive_message(client_socket)
		if user != False:
			self.sockets_list.append(client_socket)
			self.clientsDict[client_socket] = user
			print('Accepted new Connection from {}:{}, user: {}'.format(*client_address, user['data'].decode('UTF-8')))

	def prepMsgToSend(self, msg):
		newMsg = f'{len(msg):<{self.HEADERSIZE}}' + msg
		newMsg = newMsg.encode('UTF-8')
		return newMsg



def main():

	myServer = pyChat_server()

	myServer.accept_Connections()


if __name__ == '__main__':
	main()

