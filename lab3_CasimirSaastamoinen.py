#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# The modules required
import sys
import socket

'''
Use this template to create exercise 1 of lab3. Follow the hints found in the comments to complete the task.
'''
 
 
def send_and_receive_tcp(address, port, message):
    # create TCP socket
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect socket to given address and port
    s_tcp.connect((address, port))
    # python3 sendall() requires bytes like object. Encode the message with .encode() command
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

    # Uncomment for second part of the exercise:
    send_and_receive_udp(address, port, decoded)
    return
 
 
def send_and_receive_udp(address, port, message):
    # create UDP socket
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # You turned the message in to str in previous function. Turn it back to bytes
    encoded_udp = message.encode()
    # send given message to given address and port using the socket.
    s_udp.sendto(encoded_udp, (address, port))

    # Loop the following
    while True:
        # receive data from socket
        data_udp = s_udp.recvfrom(1024)
        # Data you receive is in bytes format. Turn it to string with .decode() command
        decoded_udp = data_udp[0].decode()
        # print received data
        print(decoded_udp)
        # if received data contains the word 'QUIT' break the loop
        if "QUIT" in decoded_udp:
            break
        
       
    # close the socket
    s_udp.close()

    return
 
 
def main():
    USAGE = 'usage: %s <server address> <server port> <message>' % sys.argv[0]
 
    try:
        # Get the server address, port and message from command line arguments
        server_address = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
        message = str(sys.argv[3])
    except IndexError:
        print("Index Error")
    except ValueError:
        print("Value Error")
    # Print usage instructions and exit if we didn't get proper arguments
        sys.exit(USAGE)
 
    send_and_receive_tcp(server_address, server_tcpport, message)
 
 
if __name__ == '__main__':
    # Call the main function when this script is executed
    main()
