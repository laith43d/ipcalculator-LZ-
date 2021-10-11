def findClass(ip):
    if(ip[0] >= 0 and ip[0] <= 127):
        return "A"

    elif(ip[0] >=128 and ip[0] <= 191):
        return "B"

    elif(ip[0] >= 192 and ip[0] <= 223):
        return "C"

    elif(ip[0] >= 224 and ip[0] <= 239):
        return "D"

    else:
        return "E"


def findpps(ip):
    if(ip[0] == 10 | (ip[0] ==169 & ip[1]==254)|(ip[0] ==172 &(ip[1] >= 16 & ip[1] <= 31))|(ip[0] ==192 & ip[1]==168)):
        return "Private"
    elif(ip[0] == 127):
        return "Special"
    else:
        return "Puplic"

def seperate(ip, className):

    #for class A network
    if(className == "A"):
        print("Network Address is : ", ip[0])
        print("Host Address is : ", ".".join(ip[1:4]))

    #for class B network
    elif(className == "B"):
        print("Network Address is : ", ".".join(ip[0:2]))
        print("Host Address is : ", ".".join(ip[2:4]))

    #for class C network
    elif(className == "C"):
        print("Network Address is : ", ".".join(ip[0:3]))
        print("Host Address is : ", ip[3])

    else:
        print("In this Class, IP address is not divided into Network and Host ID")
        print("spestiol")


#driver's code
if __name__ == "__main__":

    ip = input('enter ip  ')
    ip = ip.split(".")
    ip_2 = ip.split("/")
    ip = ip_2[0].split(".")
    ip = [int(i) for i in ip]

Class = findClass(ip)
print(" Class: ",Class,",")
pps=findpps(ip)
print(" Class: ",Class,", P.P.S ",pps)
