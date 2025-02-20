Just messing around with sockets in python :)

The file-server.py has a critical security flaw that allows arbitrary read/write of data on the server side. See if you can find it!

After running file-server.py, you can connect to it by running netcat:
    `$ nc 127.0.0.1 65432`
