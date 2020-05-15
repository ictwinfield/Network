import socket
import threading

# Constants
PORT = 1234
# HOST  = socket.gethostbyname(socket.gethostname())
HOST = '192.168.1.22'
HEADER = 10
DISCONNECT_MSG = "!DISCONNECT"

connections = {}

# Create client handler
def client_handler(my_key, conn, addr):
    # Create a loop to continuously look for messages
    while True:
        header = conn.recv(HEADER).decode("utf-8")
        # Make sure there is something to look at
        if header:
            msg_len = int(header)
            msg = conn.recv(msg_len).decode("utf-8")
            if msg == DISCONNECT_MSG:
                break
            print(f'[{addr}] {msg}')
            for myKey in connections:
                if my_key != myKey:
                    print(f"Sending to: {my_key}")
                    connections[myKey][0].send(msg.encode('utf-8'))
    
    conn.close()

def start():
    num_connections = 0
    # Create listening socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(3)
    # Loop to keep listening for connect
    while True:
        conn, addr = s.accept()
        # Place the client information in a dictionary
        connections[num_connections] = [conn, addr]
        # Create the thread
        thread = threading.Thread(target=client_handler, args=(num_connections,conn,addr))
        num_connections += 1
        thread.start()


# Create listening socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(3)

start()