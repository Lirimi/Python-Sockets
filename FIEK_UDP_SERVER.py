from numpy import gcd
import socket
import random
import datetime

UDP_Server = "localhost"
UDP_Port = 13000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((UDP_Server, UDP_Port))
print("""
           _     ____ _____  ___
|\   /| | | \  |     |     |      \      / | |\   | |
| \_/ | | |__| |__   |___  |__     \    /  | | \  | |
|     | | |\   |         | |        \  /   | |  \ | |
|     | | | \  |___  ____| |____     \/    | |   \| |
      """)
print('@@-------Serveri u startua ne localhost me portin:' + str(UDP_Port) + '-------@@')
print('@@---------Serveri eshte i gatshem te pranoj kerkesa----------@@ \n \n')


def IPADDRESS():
    if clAddress[0] is not None:
        return 'IP Adresa e klientit është:  %s ' % clAddress[0]


def PORT():
    if clAddress[1] is not None:
        return 'Klienti është duke përdorur portin: %s ' % clAddress[1]


def COUNT(text, clAddress):
    if text != "":
        zanore = 0
        bashktingellore = 0
        for char in text:
            if char in "aeiouyAEIOUY":
                zanore += 1
            elif char in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ":
                bashktingellore += 1
        var = "Teksti i pranuar përmban " + str(zanore) + " zanore dhe " + str(bashktingellore) + " bashketingellore"
        serverSocket.sendto(var.encode("utf-8"), clAddress)
    else:
        serverSocket.sendto("NULL!".encode("utf-8"), clAddress)


def REVERSE(text, clAddress):
    revtext = ""
    for char in text:
        revtext = char + revtext
    var = revtext.strip()
    serverSocket.sendto(var.encode("utf-8"), clAddress)


def PALINDROME(text, clAddress):
    if text == text[::-1]:
        var = str(True)
    else:
        var = str(False)
    serverSocket.sendto(var.encode("utf-8"), clAddress)


def TIME():
    if datetime.datetime.now() is not None:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def GAME():
    var = [random.randint(1, 35) for rand in range(0, 5)]
    var.sort()
    return str(var)


def GCF(number1, number2, clAddress):
    var = str(gcd(number1, number2))
    serverSocket.sendto(var.encode("utf-8"), clAddress)


def CONVERT(request, number, clAddress):
    if request == "cmToFeet":
        var = str(number * 0.0328084)
    elif request == "FeetToCm":
        var = str(number * 30.48)
    elif request == "kmToMiles":
        var = str(number * 0.621371)
    elif request == "MilesToKm":
        var = str(number * 1.609344)
    else:
        raise Exception("wrong convert request")

    serverSocket.sendto(var.encode("utf-8"), clAddress)


# Metoda ---1#
def LOTTO(number1, number2, number3, clAddress):
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
    serverSocket.sendto(
        var.encode("utf-8") + var1.encode("utf-8") + var2.encode("utf-8") + var3.encode(
            "utf-8") + var4.encode("utf-8"), clAddress)


# Metoda ---2#
def HIDE(text, clAddress):
    var = '*' * (len(text) - 4) + text[-4:]
    serverSocket.sendto(var.encode("utf-8"), clAddress)


while True:
    socket, clAddress = serverSocket.recvfrom(128)
    request = socket.decode("utf-8").split(" ")
    socketReceive = str(socket.decode().strip().upper())

    try:
        if socketReceive == "IPADDRESS":
            serverSocket.sendto(IPADDRESS().encode(), clAddress)
        elif socketReceive == "PORT":
            serverSocket.sendto(PORT().encode(), clAddress)
        elif request[0].upper() == "COUNT":
            COUNT(" ".join(request[1:]), clAddress)
        elif request[0].upper() == "REVERSE":
            REVERSE(" ".join(request[1:]), clAddress)
        elif request[0].upper() == "PALINDROME":
            PALINDROME(" ".join(request[1:]), clAddress)
        elif socketReceive == "TIME":
            serverSocket.sendto(TIME().encode(), clAddress)
        elif socketReceive == "GAME":
            serverSocket.sendto(GAME().encode(), clAddress)
        elif request[0].upper() == "GCF":
            try:
                GCF(int(request[1]), int(request[2]), clAddress)
            except Exception:
                raise Exception("GCF Argumentet Gabim/Mungojne!")
        elif request[0].upper() == "CONVERT":
            try:
                CONVERT(request[1], float(request[2]), clAddress)
            except Exception:
                raise Exception("Convert Argumentet Gabim/Mungojne!")
        elif request[0].upper() == "LOTTO":
            try:
                LOTTO(int(request[1]), int(request[2]), int(request[3]), clAddress)
            except Exception:
                raise Exception("LOTTO Argumentet Gabim/Mungojne!")
        elif request[0].upper() == "HIDE":
            HIDE(" ".join(request[1:]), clAddress)
        else:
            serverSocket.sendto("Pass the method right! Type \"QUIT\" if you want to quit".encode("utf-8"),
                                clAddress)

    except Exception as error:
        var = ""

        if str(error) == "GCF Argumentet Gabim/Mungojne!":
            var = "\"GCF\" pranon 2 numra integjer si argumente!."
        elif str(error) == "Convert Argumentet Gabim/Mungojne!":
            var = "\"CONVERT\" args must be (cmToFeet, FeetToCm, kmToMiles, MilesToKm) and its value to convert!"
        elif str(error) == "LOTTO Argumentet Gabim/Mungojne!":
            var = "\"LOTTO\" Miresevini ne Lotto. Zgjedh tre numra prej rangut 0-20"

        serverSocket.sendto(var.encode("utf-8"), clAddress)

serverSocket.close()
quit()
