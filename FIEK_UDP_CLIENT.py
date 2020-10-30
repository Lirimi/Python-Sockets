import socket

UDP_Server = "localhost"

UDP_port = 13000

clSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:

        print("Operacioni(IPADDRESS, PORT, COUNT, REVERSE, PALINDROME, TIME, GAME, GCF, CONVERT, LOTTO, HIDE)?", end=" ")
        request = input("")

        if request == "":
            continue
        elif request.upper() == "QUIT":
            print("Ju u shkyqet nga serveri!\n")
            break

        clSocket.sendto(request.encode("utf-8"), (UDP_Server, UDP_port))

        Data, address = clSocket.recvfrom(128)

        print(Data.decode("utf-8"))
    except:
        print("Serveri nuk eshte aktiv (Shtypni QUIT per tu larguar).\n")

clSocket.close()
quit()
