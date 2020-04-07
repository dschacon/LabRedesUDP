import socket
import time
import os
import sys
import hashlib


def checkArg():
    #Se pide como argumentoel puerto del socket
    if len(sys.argv) != 2:
        print(
            "ERROR. Wrong number of arguments passed. System will exit. Next time please supply 1 argument!")
        sys.exit()
    else:
        print("1 Argument exists. We can proceed further")


def checkPort():
    if int(sys.argv[1]) <= 5000:
        print(
            "Port number invalid. Port number should be greater than 5000. Next time enter valid port.")
        sys.exit()
    else:
        print("Port number accepted!")


def ServerList():
    print("Enviando confirmacion de comando")
    msg = "Comando valido. Ejecutando"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Mensaje enviado por el server.")

    print("En el Server, Lista de funciones")

    F = os.listdir(
        path="C:/Users/HP DY/Documents/2020-1/Redes/LabRedesUDP/Server")
    
    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)
    print("Lista enviada desde el servidor")


def ServerExit():

    print(
        "System exit! No se envia ningun mensaje. Socket cerrado")
    s.close()  # closing socket
    sys.exit()


def ServerGet(g):
    print("Enviando confirmacion de comando")
    msg = "Comando Valido. Ejecutando "
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Mensaje enviado al ciente")
    print(str(os.path))
    print("En el Server, Get function")

    ruta = "C:/Users/HP DY/Documents/2020-1/Redes/LabRedesUDP/Server/" + str(g)

    if os.path.isfile(ruta):
        msg = "El archivo existe "
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Mensaje de confirmacion de archivo existente.")

        c = 0
        sizeS = os.path.getsize(ruta)
        sizeSS = sizeS
        print("Tamaño del archivo: " + str(sizeSS))
        NumS = int(sizeSS / 4096)
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        s.sendto(tillSSS, clientAddr)

        check = int(NumS)
        GetRunS = open(ruta, "rb")
        #objeto hash
        h = hashlib.sha1()
        tiempo_inicio=time.time()
        while check != 0:
            RunS = GetRunS.read(4096)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            h.update(RunS) #actualiza el hash
            print("Numero de fragmento:" + str(c))
            print("Enviando...")
            
        tiempo_final = round(time.time() - tiempo_inicio,5)
        time.sleep(1)
        GetRunS.close()
        print("Archivo enviado")
        hash_archivo = h.hexdigest()
        #Se envia hash
        s.sendto(hash_archivo.encode('utf-8'),clientAddr)
        print('Se envio el hash del archivo al cliente')
        print(hash_archivo)
        print('El tiempo fue: '+str(tiempo_final))


    else:
        msg = "Error: Archivo: "+str(g)+" no esxite en el servidor "+str(ruta)
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Mensaje error enviado.")


def ServerElse():
    msg = "Error: You asked for: " + \
        t2[0] + " which is not understood by the server."
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent.")


host = "0.0.0.0"
checkArg()
try:
    port = int(sys.argv[1])
except ValueError:
    print("Error. Exiting. Please enter a valid port number.")
    sys.exit()
except IndexError:
    print("Error. Exiting. Please enter a valid port number next time.")
    sys.exit()
checkPort()

#port = 6000
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server socket initialized")
    s.bind((host, port))
    print("Waiting for Client")
    # s.setblocking(0)
    # s.settimeout(15)
except socket.error:
    print("Failed to create socket")
    sys.exit()

# time.sleep(1)
while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print(
            "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
        sys.exit()
    text = data.decode('utf8')
    t2 = text.split()
    #print("data print: " + t2[0] + t2[1] + t2[2])
    if t2[0] == "get":
        print("Go to get func")
        ServerGet(t2[1])
    elif t2[0] == "list":
        print("Go to List func")
        ServerList()
    elif t2[0] == "exit":
        print("Go to Exit function")
        ServerExit()
    else:
        ServerElse()

print("Program will end now. ")
quit()