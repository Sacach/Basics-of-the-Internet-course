def send_and_receive_tcp(address, port, message):
    print("You gave arguments: {} {} {}".format(address, port, message))
    # create TCP socket
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect socket to given address and port
    s_tcp.connect((address, port))
    # python3 sendall() requires bytes like object. encode the message with str.encode() command
    encoded = message.encode()
    # send given message to socket
    s_tcp.sendall(encoded)
    # receive data from socket
    data = s_tcp.recv(1024)
    # data you received is in bytes format. turn it to string with .decode() command
    decoded = data.decode()
    # print received data
    print(decoded)
    # close the socket
    s_tcp.close()
    # Get your CID and UDP port from the message
    hello, CID, port = decoded.strip("\r\n").split(" ")
    # Continue to UDP messaging. You might want to give the function some other parameters like the above mentioned cid and port.
    send_and_receive_udp(address, port, CID)
    return
