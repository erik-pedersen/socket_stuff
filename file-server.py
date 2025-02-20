import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                method, file, *_ = data.split(b" ")
                print(f"DEBUG: method = {method}, file = {file}")
            except ValueError:
                conn.sendall(b"Usage: <METHOD> <FILENAME>")
                continue

            if method == b"GET":
                try:
                    f = open(file)
                    send = f.read().encode(encoding="utf-8")
                    conn.send(file + b": \n")
                    conn.sendall(send)
                except FileNotFoundError:
                    print(f"File {f} not found.")

            elif method == b"POST":
                try:
                    f = open(file, "w")
                    conn.sendall(b"Send data to transmit\n")
                    while True:
                        postData = conn.recv(1024)
                        if not postData:
                            f.close()
                            break
                        f.write(postData)
                except:
                    conn.sendall(b"Error receiving data")
            else:
                send = b"Invalid method.\n"
                conn.sendall(send)

            print(f"Received: {data}")
            conn.sendall(data)
