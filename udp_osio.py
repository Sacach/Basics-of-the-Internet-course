
def send_and_receive_udp(address, port, CID):

    # Creates UDP socket
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Creates a message
    message = "Hello from {}\n".format(CID)
    lenght = len(message)

    encoded_udp = message.encode()
    encoded_CID = CID.encode()
    Data = struct.pack('!8s??HH128s', encoded_CID, True, False, 0, int(lenght), encoded_udp)

    # send given message to given address and port using the socket.
    s_udp.sendto(Data, (address, int(port)))

    # Loop the following
    while True:
        viesti = ""
        list = []
        while True:
            # receive data from socket
            data_udp = s_udp.recvfrom(1024)
            # Data you receive is in bytes format. Turn it to string with .decode() command
        
            decoded_udp = data_udp[0].decode()
        
            print("data_udp: ",data_udp)
            CID, ACK, EOM, Rem, lenght, data = struct.unpack('!8s??HH128s', data_udp[0])
            #remain = Rem
            
            data1 = data.decode()
            data1 = data1.rstrip("\x00")
            
            print("Rem: ", Rem)

            # print received data

            list += data1.split(" ")
            print("lista: ",list)

            if Rem == 0:
                break

        if EOM:
            break
        
        while list:
            viesti = viesti + "{} ".format(list.pop(-1))
        
        viesti = viesti.rstrip(" ")
        print("viesti: ",viesti)
        lenght = len(viesti)
        encoded_viesti = viesti.encode()
        Data = struct.pack('!8s??HH128s', encoded_CID, True, False, 0, int(lenght), encoded_viesti)
        
        s_udp.sendto(Data, (address, int(port)))

        # if received data contains the word 'Bye' break the loop
        
        
       
    # close the socket
    s_udp.close()
    
    return