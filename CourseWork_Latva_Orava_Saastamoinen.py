#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# The modules required
import sys
import socket
import struct
import random
import textwrap
'''
This is a template that can be used in order to get started. 
It takes 3 commandline arguments and calls function send_and_receive_tcp.
in haapa7 you can execute this file with the command: 
python3 CourseWorkTemplate.py <ip> <port> <message> 

Functions send_and_receive_tcp contains some comments.
If you implement what the comments ask for you should be able to create 
a functioning TCP part of the course work with little hassle.  

''' 
def get_parity(n):
    """
    Luo parity bitin muuttujalle n
    Kopioitu harjoitustyön ohjeesta
    """
    while n > 1:
        n = (n >> 1) ^ (n & 1) 
    return n

def xor_strings(string_1, string_2):
    """
    Tekee xor-operaation kahdelle str-tyypin muuttujalle
    """
    # alustetaan xor tulos
    xor_result = ""
    # for looppi, jossa xorrataan merkki kerrallaan kaksi merkkijonoa
    for x,y in zip(string_1, string_2):
        # xor-operaatio samassa kohdassa oleville merkkeille
        xorred_char = chr(ord(x) ^ ord(y))
        # lisätään saatu merkki xor tulokseen
        xor_result += xorred_char
    # palautetaan kahden merkkijonon xor-operaation tulos
    return xor_result

def get_keys():
    """
    Luo 20 kpl 64:n tavun pituista avainta
    """
    # alustetaan laskuri i, avainten muuttuja keys ja avainten lista
    i = 0
    keys = ""
    keylist = []
    # merkit joista avaimet muodostetaan
    merkit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"]
    # while looppi jossa luodaan 20 avainta
    while i < 20:
        # alustetaan key muuttuja uuden avaimen luontia varten
        key = ""
        # alustetaan laskuri j
        j = 0
        # while looppi jossa luodaan yksi 64 merkin pituinen avain
        while j < 64:
            # valitaan satunnainen merkki
            valinta = random.choice(merkit)
            # lisätään merkki avaimeen
            key += valinta
            # kasvatetaan laskuria (1 merkki lisätty)
            j += 1
        keylist.append(key)
        # lisätään avain kaikkien avainten joukkoon
        keys += key + "\r\n"
        # kasvatetaan laskuria (1 avain luotu)
        i += 1
    # lisätään ".\r\n" avainten perään
    keys += ".\r\n"
    # palautetaan keys ja keylist
    return keys, keylist

def send_and_receive_tcp(address, port, message):
    """
    tcp kommunikointi funktio
    """
    # Kertoo annetut argumentit
    print("You gave arguments: {} {} {}".format(address, port, message))
    # luodaan TCP socket
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # yhdistetään tcp socket osoiteeseen ja portiin
    s_tcp.connect((address, port))
    # luodaan avaimet get_keys-funktiolla
    keys, keylist = get_keys()
    # luodaan lähetettävä viesti 
    message = message + "\r\n" + keys
    # encodataan viesti
    encoded = message.encode()
    # lähetetään viesti
    s_tcp.sendall(encoded)
    # vastaanotetaan dataa
    data = s_tcp.recv(2048)
    # dekoodaus datalle
    decoded = data.decode()
    # suljetaan socket
    s_tcp.close()
    # jaetaan saatu viesti välilyöntien kohdalta
    hello, CID, portNkeys = decoded.split(" ")
    # udp-portti ja avaimet joutuivat samaan muuttujaan, joten erotetaan ne toisistaan
    port, server_keys = portNkeys.strip("\r\n.\r\n").split("\r\n", 1)
    # luodaan lista serverin avaimista
    server_keylist = server_keys.split("\r\n")
    # Jatketaan udp vaiheeseen
    send_and_receive_udp(address, port, CID, keylist, server_keylist)
    return

def parity(str):
    """
    Lisää pariteettibitin str-merkkijonon jokaiseen merkkiin
    """
    # alustetaan p, johon tehdään paritettu merkkijono
    p = ""
    # for looppi jolla käydään merkit läpi
    for x in str:
        # x:n unicode arvo
        x = ord(x)
        # left shift yhdellä
        x <<= 1
        # lisätään pariteettibitti x:n arvoon
        x += get_parity(x)
        # muutetaan x merkiksi
        x = chr(x)
        # lisätään saatu merkki paritettuun merkkijonoon
        p += x
    # palautetaan valmis merkkijono
    return p

def inv_parity(str):
    # alustetaan p, johon tehdään epäparitettu merkkijono
    p = ""
    # for looppi jolla käydään merkit läpi
    for x in str:
        # x:n unicode arvo
        x = ord(x)
        # poimitaan x:n binäärimuodosta pariteettibitti
        binary = bin(x)
        p_bit = binary[-1]
        # right shift yhdellä
        x >>= 1
        # jos pariteettibitti on virheellinen, palautetaan tähän asti saatu p ja false
        if int(p_bit) != int(get_parity(x)):
            return p, False
        # muutetaan x merkiksi
        x = chr(x)
        # lisätään saatu merkki epäparitettuun merkkijonoon
        p += x
    # palautetaan valmis merkkijono ja true
    return p, True

def send_and_receive_udp(address, port, CID, keylist, server_keylist):
    """
    udp kommunikointi funktio
    """
    # alustetaan käytettyjen avainten laskurit (a = omat, b = serverin)
    a = 0
    b = 0
    # Luo UDP socketin
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udp aloitusviesti
    message = "Hello from {}\n".format(CID)
    # otetaan udp viestin pituus
    lenght = len(message)
    # viestin kryptaus
    encrypted = xor_strings(message, keylist[a])
    # yksi omista avaimista käytetty
    a += 1
    # viestin paritus
    parited = parity(encrypted)
    # enkoodataan kryptattu viesti
    encoded_udp = parited.encode()
    # enkoodataan CID
    encoded_CID = CID.encode()
    # luodaan lähetettävä datapaketti pakkaamalla kaikki vaaditut tiedot
    Data = struct.pack('!8s??HH128s', encoded_CID, True, False, 0, lenght, encoded_udp)
    # lähetetään datapaketti serverille
    s_udp.sendto(Data, (address, int(port)))
    # Looppi lopuille udp viesteille
    while True:
        # alustetaan viesti, lista, multipart viestityksen puskuri ja ACK_flag
        viesti = ""
        multipart = ""
        lista = []
        ACK_flag = 0
        # looppi vastaanottamiselle
        while True:
            # vastaanotetaan dataa serveriltä
            data_udp = s_udp.recvfrom(1024)
            # avataan vastaanotettu paketti muuttujiin CID, ACK, EOM, Rem, lenght ja msg
            CID, ACK, EOM, Rem, lenght, msg = struct.unpack('!8s??HH128s', data_udp[0])
            # dekoodataan viesti
            msg = msg.decode()
            # jos viesti on viimeinen serverin lähettämä poistutaan vastaanottoloopista
            if EOM:
                # tulostetaan serverin viimeinen viesti
                print("Server: ", msg)
                break
            # epäparitetaan msg
            deparited, ACK = inv_parity(msg)
            # jos pariteettibitti on virheellinen nostetaan ACK_flag
            if ACK == False:
                ACK_flag = 1
            # jos serverin avaimia on vielä jäljellä kryptataan
            if b < 20:
                # kryptaus xor-operaatiolla
                decrypted = xor_strings(deparited, server_keylist[b])
                # yksi serverin avaimista käytetty
                b += 1
            # muutoin ei kryptata
            else:
                decrypted = deparited
            # lisätään multipart puskuriin dekryptattu viesti 
            multipart += decrypted[:lenght]
            # jos jäljellä olevan viestin osuus on 0 poistutaan loopista
            if Rem == 0:
                break
        # jos viesti on viimeinen serverin lähettämä poistutaan udploopista
        if EOM:
            break
        # luodaan lista puskurissa olevista sanoista
        lista = multipart.split(" ")
        # jos ACK_flag on ylhäällä pyydetään serveriä lähettämään uudestaan
        if ACK_flag == 1:
            # uudelleen lähetyspyyntö
            send_again = "Send again"
            # jos omia avaimia on vielä jäljellä kryptataan
            if a < 20:
                # kryptaus xor-operaatiolla
                encrypted = xor_strings(send_again, keylist[a])
                # yksi omista avaimista käytetty
                a += 1
            # muutoin ei kryptata
            else:
                encrypted = send_again
            # merkkijonon pituus
            lenght = len(encrypted)
            # paritetaan viesti
            parited = parity(encrypted)
            # encodataan lähetettävä viesti
            encoded_viesti = parited.encode()
            # luodaan lähetettävä datapaketti pakkaamalla kaikki vaaditut tiedot
            Data = struct.pack('!8s??HH128s', encoded_CID, False, False, 0, lenght, encoded_viesti)
            # lähetetään datapaketti
            s_udp.sendto(Data, (address, int(port)))
            # ACK_flag alas
            ACK_flag = 0
        else:
            # looppi viestin luomiselle
            while lista:
                # järjestetään saadut sanat päinvastaiseen järjestykseen
                viesti += "{} ".format(lista.pop(-1))
            # poistetaan ylimääräinen välilyönti
            viesti = viesti.rstrip(" ")
            # jäljellä olevan viestin pituus
            Rem_lenght = len(viesti)
            # luodaan rajat, joilla valitaan tietty osa viestistä lähetettäväksi
            raja1 = 0
            raja2 = 64
            # looppi joka jatkuu niin kauan kuin viestiä on vielä lähetettävänä
            while Rem_lenght:
                # lähetettävää on 64 tavua vähemmän
                Rem_lenght -= 64
                # jos lähetettävää ei ole jäljellä asetetaan Rem_lenght nollaan
                if Rem_lenght <= 0:
                    Rem_lenght = 0
                # jos omia avaimia on vielä jäljellä kryptataan
                if a < 20:
                    # kryptaus xor-operaatiolla
                    encrypted = xor_strings(viesti[raja1:raja2], keylist[a])
                    # yksi omista avaimista käytetty
                    a += 1
                # muutoin ei kryptata
                else:
                    encrypted = viesti[raja1:raja2]
                # nostetaan molempia rajoja
                raja1 += 64
                raja2 += 64
                # hankitaan viestin pituus
                lenght = len(encrypted)
                # paritetaan viesti
                parited = parity(encrypted)
                # enkoodataan lähetettävä viesti
                encoded_viesti = parited.encode()
                # luodaan lähetettävä datapaketti pakkaamalla kaikki vaaditut tiedot
                Data = struct.pack('!8s??HH128s', encoded_CID, True, False, Rem_lenght, lenght, encoded_viesti)
                # lähetetään datapaketti
                s_udp.sendto(Data, (address, int(port)))
    # suljetaan socket
    s_udp.close()
    
    return
 
 
def main():
    """
    main funktio, ei muokkauksia
    """
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
