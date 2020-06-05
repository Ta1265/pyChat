import socket

HEADERSIZE = 10
IP = '127.0.0.1'
PORT = 1217

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP,PORT))

msg_len = int(s.recv(HEADERSIZE).strip())
msg = s.recv(msg_len).decode('UTF-8')
print(msg)

while True:
	myMsg = input('-> ')
	myMsg = f'{len(myMsg):<{HEADERSIZE}}' + myMsg
	myMsg = myMsg.encode('UTF-8')

	s.send(myMsg)





# userName = f'{len(userName):<{HEADERSIZE}}' + userName
# print(userName)
# userName = userName.encode('UTF-8')

# s.send(userName)



