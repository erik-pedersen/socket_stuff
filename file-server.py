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
                file = file.strip(b"\n")
                print(f"DEBUG: method = {method}, file = {file}")
            except ValueError:
                conn.sendall(b"Usage: <GET/POST> <FILENAME>")
                continue

            if method == b"GET":
                try:
                    f = open(file, "r")
                    send = f.read().encode()
                    conn.send(file + b": \n")
                    conn.sendall(send)
                    f.close()
                except FileNotFoundError:
                    print(f"File {f} not found.")

            elif method == b"POST":
                #try:
                f = open(file, "w")
                conn.sendall(b"Send data to transmit\n")
                while True:
                    postData = conn.recv(1024)
                    if postData == b"EOF" or postData == b"EOF\n":
                        conn.sendall(b"Data received, closing file.\n")
                        f.close()
                        break
                    elif not postData:
                        conn.sendall(b"Failed to receive file")
                        f.close()
                        break
                    f.write(postData.decode())
            else:
                send = b"Invalid method.\n"
                conn.sendall(send)

            print(f"Received: {data}")
            conn.sendall(data)
