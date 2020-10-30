import socket

TCP_Server = "localhost"
TCP_Port = 13000

while True:
    try:
        clSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clSocket.connect((TCP_Server, TCP_Port))

        print("Operacioni (IPADDRESS, PORT, COUNT, REVERSE, PALINDROME, TIME, GAME, GCF, CONVERT, LOTTO, HIDE)? ", end=" ")
        request = input("")

        if request == "":
            continue
        elif request == "QUIT":
            print("Ju u shkyqet nga serveri!\n")
            break

        clSocket.send(request.encode("utf-8"))

        NewData = clSocket.recv(128)

        print(NewData.decode("utf-8") + '\n')

    except:
        print("Serveri nuk eshte aktiv!.")
        break

clSocket.close()
quit()

