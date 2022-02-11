#!/usr/bin/python

import select
import socket
import string

'''
This is a template for lab3 exercise 2. It creates a server that listens for TCP and UDP connections and when it receives one it will execute either handle_tcp() or handle_udp() function. 
'''

# Hard coded values. You are allowed to hard code the target servers address if you like.
'''
If the port is not available use another one. You can't use the same ports as other groups so find a unique value from around 21XX port range 
'''
TCP_PORT = 21562
UDP_PORT = 21562

def handle_tcp(sock):
    '''
    This function does the following:
    * When receiving a message from the client print the message content and somehow implicate where it came from. For example "Client sent X"
    * Create a TCP socket.
    * Forward the message to the server using the socket.
    * Print what you received from the server
    * Forward it to the client.
    * Close socket
    '''
    #accepts the connection
    (c, address) = sock.accept()
    #receives the message from client
    message = c.recv(1024)
    #prints the message
    print("Client sent: ", message)
    #creates a tcp socket
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connects the socket to lab3 server
    s_tcp.connect(("195.148.20.105", 20000))
    #sends the message received from client to the lab3 server
    s_tcp.sendall(message)
    #receives data from server
    data_tcp = s_tcp.recv(1024)
    #prints the data received from server
    print("Server sent: ", data_tcp)
    #sends the data received from server to client
    c.sendall(data_tcp)
    #closes the tcp socket
    s_tcp.close()
    #sanity check that the code got this far
    print("TCP happended")

    return


def handle_udp(sock):
    '''
    This function should do the following
    * When receiving a message from the client print the message content and somehow implicate where it came from. For example "Client sent X"
    * Create a UDP socket
    * Forward the message to the server using the socket.
    * A loop that does the following:
        * Print what you received from the server
        * Forward it to the client.
        * Break. DO NOT use message content as your break logic (if "QUIT" in message). Use socket timeout or some other mean.  
    * Close socket
    '''
    #receives data from client
    message, address = sock.recvfrom(1024)
    #prints the data received from client
    print("Client sent: ", message)
    #Creates a UDP socket
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sends the message received from client to the lab3 server
    s_udp.sendto(message, ("195.148.20.105", 20000))
    
    while True:
        try:
            #receives data from server
            data, server = s_udp.recvfrom(1024)
            #prints the data received from server
            print("Server sent: ", data)
            #sends the data received from server to client
            sock.sendto(data, address)
            #sets the timeout for udp socket
            s_udp.settimeout(1)
        #socket timeout to break out from the loop
        except socket.timeout:
            break
        
    #closes the udp socket
    s_udp.close()
    #sanity check that the code got this far
    print("UDP happened")
    
    return




def main():
    try:
        print("Creating sockets")
        '''
        Create and bind TCP and UDP sockets here. Use hard coded values TCP_PORT and UDP_PORT to choose your port. 
        Note that while loop below  uses these sockets, so name them tcp_socket and udp_socket or modify the loop below.
        '''
        #creates a tcp socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #binds the tcp socket to the chosen port
        tcp_socket.bind(('', TCP_PORT))
        #starts listening
        tcp_socket.listen(0)
        #print to make sure that the tcp socket creating was successful
        print("TCP server up and listening")
        #creates a udp socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #binds the udp socket to the chosen port
        udp_socket.bind(('', UDP_PORT))
        #print to make sure that the udp socket creating was successful
        print("UDP server up and listening")
        
    except OSError:
        '''
    This will be raised if you are trying to create a socket but it is still active. Likely your code crashed or otherwise closed before you closed the socket. Wait a second and the socket should become available. Alternatively you can create a logic here that binds the socket to X_PORT+1. Doing this is not mandatory
        '''
        print("OSError was rised. Port is in use. Wait a second.")

    try:
        while True:
            i, o, e = select.select([tcp_socket, udp_socket], [], [], 5)
            if tcp_socket in i:
                handle_tcp(tcp_socket)
            if udp_socket in i:
                handle_udp(udp_socket)
    except NameError:
        print("Please create the sockets. NameError was raised doe to them missing.")
    finally:
        '''
        !!Close sockets here!!
        '''
        #closing the sockets here
        tcp_socket.close()
        udp_socket.close()
    


if __name__ == '__main__':
    main()
