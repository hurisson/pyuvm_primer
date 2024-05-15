import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 15259))

while True:
    data  = client.recv(1024)
    print(data.decode("utf-8"))
    break

while True:
    msg = input().encode("utf-8")
    client.send(msg)
    if msg == b'FINISH':
        break