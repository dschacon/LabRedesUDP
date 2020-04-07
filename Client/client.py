import socket
import time
import os
import sys
import hashlib


def checkArg():
    if len(sys.argv) != 3:
        print(
            "ERROR. Wrong number of arguments passed. System will exit. Next time please supply 2 arguments!")
        sys.exit()
    else:
        print("2 Arguments exist. We can proceed further")


def checkPort():
    if int(sys.argv[2]) <= 5000:
        print(
            "Port number invalid. Port number should be greater than 5000 else it will not match with Server port. Next time enter valid port.")
        sys.exit()
    else:
        print("Port number accepted!")

checkArg()
try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Invalid host name. Exiting. Next time enter in proper format.")
    sys.exit()

host = sys.argv[1]
try:
    port = int(sys.argv[2])
except ValueError:
    print("Error. Exiting. Please enter a valid port number.")
    sys.exit()
except IndexError:
    print("Error. Exiting. Please enter a valid port number next time.")
    sys.exit()

checkPort()

#host = "127.0.0.1"
#port = 6000
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Client socket initialized")
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("Failed to create socket")
    sys.exit()
# time.sleep(1)  # gives times for server to reach at same stage


while True:
    command = input(
        "Porfavor seleccione un comando: \n1. get [file_name]\n2. list\n3. exit\n ")

    """o get [file_name]
    o put [file_name]
    o exit"""
    CommClient = command.encode('utf-8')
    try:
        s.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print(
            "Error. Port numbers are not matching. Exiting. Next time please enter same port numbers.")
        sys.exit()
    #text1 = CommClient.decode('utf-8')
    #t3 = text1.split()
    CL = command.split()
    print(
        "We shall proceed, but you may want to check Server command prompt for messages, if any.")
    # starting operations
    if CL[0] == "get":
        print("Revizando el comando")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(str("Conexion establecida, ")+text)
        print("En el cliente Get")

        try:
            ClientData2, clientAddr2 = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 30:
            if CL[0] == "get":
                BigC = open("Recibido-" + CL[1], "wb")
                d = 0
                try:
                    # number of paclets
                    CountC, countaddress = s.recvfrom(4096)
                except ConnectionResetError:
                    print(
                        "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                    sys.exit()
                except:
                    print("Timeout or some other error")
                    sys.exit()

                tillC = CountC.decode('utf8')
                tillCC = int(tillC)
                # objeto hash
                h = hashlib.sha1()
                print("Receiving packets will start now if file exists.")
                # print(
                #   "Timeout is 15 seconds so please wait for timeout at the end.")
                while tillCC != 0:
                    ClientBData, clientbAddr = s.recvfrom(4096)
                    dataS = BigC.write(ClientBData)
                    d += 1
                    print("Received packet number:" + str(d))
                    h.update(ClientBData)
                    tillCC = tillCC - 1
                    
                time.sleep(1)
                BigC.close()

                #espera el hash
                hash_archivo_enviado , clientAddr = s.recvfrom(2014)
                hash_archivo_calculado = h.hexdigest()
                hash_archivo_enviado = (str(hash_archivo_enviado).replace("b'","")).replace("'","")
                #print("Hash servidor: "+str(hash_archivo_enviado))
                #print("Hash cliente : "+str(hash_archivo_calculado))
                if hash_archivo_calculado == hash_archivo_enviado:
                    print('Los hash coinciden')
                else:
                    print('Los hash no coinciden')

                print(
                    "New Received file closed. Check contents in your directory.")
    elif CL[0] == "list":
        print("Checking list")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "Comando valido. Ejecutando":
            ClientDataL, clientAddrL = s.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Error list. Invalid.")

    elif CL[0] == "exit":
        print(
            "Server will exit if you have entered port number correctly, but you will not receive Server's message here.")
        break    

    else:
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

print("Program will end now. ")  # though, this won't get executed.
quit()