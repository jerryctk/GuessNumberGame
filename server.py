import socket
import random
import threading

serverip = 'localhost'
port = 5555


def client_handler(conn,addr):
    print(f"[New connection] {addr} connected.")
    num = random.randint(1, 20)     # Random number
    print("Random Number is ", num)
    turn = 0
    
    while turn <= 5:   # Game logic
        try:
            turn += 1
            data = int(conn.recv(2048).decode()) # กำหนดขนาดข้อมูลที่จะรับใน recv()
            if int(data) == num:
                conn.send(str(num).encode()+" ".encode()+"Win".encode()+str(turn).encode())
                break
            if int(data) > num:
                if turn == 5:
                    conn.send(str(num).encode()+" ".encode()+"Lost".encode() +str(turn).encode()) 
                    break
                else:
                    conn.send(str(num).encode()+" ".encode()+"High".encode()+str(turn).encode())
            if int(data) < num:
                if turn == 5:
                    conn.send(str(num).encode()+" ".encode()+"Lost".encode() + str(turn).encode())
                    break
                else:
                    conn.send(str(num).encode()+" ".encode()+"Low".encode() + str(turn).encode())
            print(f"[{addr}] send {data}")
        
        except ValueError:
            break
        
    print(f"[{addr}] Turns taken {turn}")
        
    conn.close()
   
 
print("[Starting] Server is starting...") 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server.bind((serverip, port))                                    
server.listen(4)                
print(f"[Listening] Server is listening on {serverip}:{port}")


while True:
    (conn, addr) = server.accept() 
    print(f"Connected to {addr}")
    thread = threading.Thread(target=client_handler, args=(conn, addr))
    thread.start()
    print(f"[Active Connection] {threading.activeCount()-1}\n")