from socket import *
from numpy import gcd
from _thread import start_new_thread
import socket
import random
import datetime

TCP_HOST_SERVER = "localhost"
TCP_PORT = 13000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((TCP_HOST_SERVER, TCP_PORT))
serverSocket.listen(1)

print("""
           _     ____ _____  ___
|\   /| | | \  |     |     |      \      / | |\   | |
| \_/ | | |__| |__   |___  |__     \    /  | | \  | |
|     | | |\   |         | |        \  /   | |  \ | |
|     | | | \  |___  ____| |____     \/    | |   \| |
      """)
print('@@-------Serveri u startua ne localhost me portin:' + str(TCP_PORT) + '-------@@')
print('@@---------Serveri eshte i gatshem te pranoj kerkesa----------@@ \n \n')


def IPADDRESS():
    return ('IP Adresa e klientit e klientit eshte: %s ' % clAddress[0])


def PORT():
    if clAddress[1] is not None:
        return 'Klienti është duke përdorur portin: %s ' % clAddress[1]


def COUNT(text, socket):
    if text != "":
        zanore = 0
        bashktingellore = 0
        for char in text:
            if char in "aeiouyAEIOUY":
                zanore += 1
            elif char in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ":
                bashktingellore += 1
        var = "Teksti i pranuar përmban " + str(zanore) + " zanore dhe " + str(bashktingellore) + " bashketingellore"
        socket.send(var.encode("utf-8"))
    else:
        socket.send("NULL!".encode("utf-8"))


def REVERSE(text, socket):
    revtext = ""
    for char in text:
        revtext = char + revtext
    var = revtext.strip()
    socket.send(var.encode("utf-8"))


def PALINDROME(text, socket):
    if text == text[::-1]:
        var = str(True)
    else:
        var = str(False)
    socket.send(var.encode("utf-8"))


def TIME():
    if datetime.datetime.now() is not None:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def GAME():
    var = [random.randint(1, 35) for rand in range(0, 5)]
    var.sort()
    return str(var)


def GCF(number1, number2, socket):
    var = str(gcd(number1, number2))
    socket.send(var.encode("utf-8"))
    
    
def CONVERT(option, number, socket):
    var = None
    if option == "cmToFeet":
        var = number * 0.0328084
    elif option == "FeetToCm":
        var = number * 30.48
    elif option == "kmToMiles":
        var = number * 0.621371
    elif option == "MilesToKm":
        var = number * 1.609344
    else:
        raise Exception("wrong convert option")
    var = str(var)
    socket.send(var.encode("utf-8"))





# Metoda ---1#
def LOTTO(number1, number2, number3, socket):
    numbers = [number1, number2, number3]
    nr_zgjedhur = numbers
    generated = random.sample(range(21), 3)
    nr_sakte = []
    for numbers in nr_zgjedhur:
        if numbers in generated:
            nr_sakte.append(numbers)

    var = "Nr qe ju zgjedhet: " + str(nr_zgjedhur)
    var1 = "\nNr e gjeneruar: " + str(generated)
    var2 = "\nNr qe ju qelluat: " + str(nr_sakte)
    count_nr_sakte = len(nr_sakte)
    var3 = "\nJu keni qelluar: " + str(count_nr_sakte) + " numra!"
    var4 = "\nTRY AGAIN!"
    if count_nr_sakte == len(generated):
        var4 = "\nWIN!"
    socket.send(
        var.encode("utf-8") + var1.encode("utf-8") + var2.encode("utf-8") + var3.encode(
            "utf-8") + var4.encode("utf-8"))


# Metoda ---2#
def HIDE(text, socket):
    var = '*' * (len(text) - 4) + text[-4:]
    socket.send(var.encode("utf-8"))


def newThread(socket, clAddress):
        try:

            Receive = socket.recv(128)

            socketReceive = str(Receive.decode().strip())
            request = Receive.decode("utf-8").split(' ')

            try:
                if socketReceive == "IPADDRESS":
                    socket.send(IPADDRESS().encode())
                elif socketReceive == "PORT":
                    socket.send(PORT().encode())
                elif request[0].upper() == "COUNT":
                    COUNT(" ".join(request[1:]), socket)
                elif request[0].upper() == "REVERSE":
                    REVERSE(" ".join(request[1:]), socket)
                elif request[0].upper() == "PALINDROME":
                    PALINDROME(" ".join(request[1:]), socket)
                elif socketReceive == "TIME":
                    socket.send(TIME().encode())
                elif socketReceive == "GAME":
                    socket.send(GAME().encode())
                elif request[0].upper() == "GCF":
                    try:
                        GCF(int(request[1]), int(request[2]), socket)
                    except Exception:
                        raise Exception("GCF Argumentet Gabim/Mungojne!")
                elif request[0].upper() == "CONVERT":
                    try:
                        CONVERT(request[1], float(request[2]), socket)
                    except Exception:
                        raise Exception("Convert Argumentet Gabim/Mungojne!")
                elif request[0].upper() == "LOTTO":
                    try:
                        LOTTO(int(request[1]), int(request[2]), int(request[3]), socket)
                    except Exception:
                        raise Exception("LOTTO Argumentet Gabim/Mungojne!")
                elif request[0].upper() == "HIDE":
                    HIDE(" ".join(request[1:]), socket)
                else:
                    socket.send("Pass the method right!".encode("utf-8"))

            except Exception as error:
                var = ""

                if str(error) == "GCF Argumentet Gabim/Mungojne!":
                    var = "\"GCF\" pranon 2 numra integjer si argumente!."
                elif str(error) == "Convert Argumentet Gabim/Mungojne!":
                    var = "\"CONVERT\" args must be (cmToFeet, FeetToCm, kmToMiles, MilesToKm) and its value to convert!"
                elif str(error) == "LOTTO Argumentet Gabim/Mungojne!":
                    var = "\"LOTTO\" Miresevini ne Lotto. Zgjedh tre numra prej rangut 0-20"

                socket.send(var.encode("utf-8"))
            socket.close()
        except:
            return


while True:
    try:
        socket, clAddress = serverSocket.accept()

        start_new_thread(newThread, (socket, clAddress))

    except:
        continue

serverSocket.close()
quit()
