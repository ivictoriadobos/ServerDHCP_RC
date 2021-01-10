import math

from AddressStuff.IPAddress import *

class AddressPool:

    def __init__(self, _ip, _mask):

        self.adreseIP = [] #aici vom stoca adresele ip generate in urma adresei de retea si masca

        self.adresa_retea = _ip

        self.adresa_difuzie = ""

        self.masca = []


        for val in _mask.split('.'):
            self.masca.append(int(val))

        total_ips = 0
        nr_zeroes =0
        for x in range(0,4): #0 1 2 3
            if self.masca[x] == 255:
                continue
            else:
                nr_zeroes_cur = 255-self.masca[x] + 1 # de ex 255-252 = 3 + 1 = 4 ; sqrt(4) = 2 = numarul de zerouri din masca din valoare curenta : 11111100 = 252
                nr_zeroes += math.log2(nr_zeroes_cur)

        total_ips = 2**nr_zeroes   # as formula says : nrOfIPs = 2^x-2, where x is the no of 0's in the subnet mask;
                                #this does include the first(gateway) and the last (broadcast) addr

        print("\nNr de ipuri pt masca " + _mask + "  = " +str(total_ips))
        print("\nAdresa de retea:" + self.adresa_retea)
        #Build the address pool
        ip = []
        for x in _ip.split('.'):
            ip.append(int(x))
        for i in range (1,int(total_ips)):
            ip[3] += 1
            if ip[3] > 255:
                ip[3] = 0
                ip[2] += 1
                if ip[2] > 255:
                    ip[2] = 0
                    ip[1] += 1
                    if ip[1] > 255:
                        ip[1] = 0
                        ip[0] += 1
            self.adreseIP.append(IPAddress(str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3])))
            # print("\n\tappending this ip addr to the pool : " + str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3]))

        self.adresa_difuzie =  str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3])
        self.server_identifier =  str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3] -1)
        print("\nserver_identifier " + self.server_identifier)


        for client_ip in self.adreseIP:
            if client_ip.ip == self.server_identifier or client_ip.ip == self.adresa_difuzie:#eliminam adresa pt server_identifier, adresa de difuzie
                self.adreseIP.remove(client_ip)


    def getFreeAddress(self, _mac):
        ip = None
        for _ip in self.adreseIP:
            if _ip.free == True and _ip.keep == False:
                _ip.setMac(_mac)
                _ip.set_IP_unavailable()
                _ip.keep_IP_address()
                ip = _ip
        return ip


    def getIPAddress(self, option50, _mac ):
        """
        Functie ce intoarce un obiect IPAddress si care tine cont de urmatoarele:
        1)Intai verificam daca masina care cere o adresa IP este printre cele care au asignat static o adresa IP si aceea le revine doar lor mereu
        2)Verificam preferinta masinii analizand optiunea 50, daca ea exista
        3)Daca niciuna de mai sus nu intoarce un IP masinii, inseamna ca putem aloca un IP oarecare din adress pool ul nostru.
        """

        #cazul in care se aloca acelasi ip unei masini (static binding)
        staticIp = self.findIPByMac(_mac)
        if staticIp != None:
            staticIp.set_IP_unavailable()
            staticIp.keep_IP_address()
            return staticIp

        elif option50.values != None:
            requested = self.findIPObjByIPAddr(option50)




    def findIPObjByIPAddr(self, ip):
        return [ipobj for ipobj in self.adreseIP if ipobj.ip == ip].pop()


    def findIPByMac(self, _mac):
        return [ip for ip in self.adreseIP if ip.mac == _mac].pop()
# if __name__ == '__main__':
#     ap = AddressPool("192.168.1.0", "255.255.255.0")







