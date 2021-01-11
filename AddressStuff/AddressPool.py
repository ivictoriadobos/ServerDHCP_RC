import math

from AddressStuff.IPAddress import *


class AddressPool:

    def __init__(self, _ip, _mask):

        self.adreseIP = []  # aici vom stoca adresele ip generate in urma adresei de retea si masca

        self.adresa_retea = _ip

        self.adresa_difuzie = ""

        self.masca = []

        for val in _mask.split('.'):
            self.masca.append(int(val))

        self.total_ips = 0
        nr_zeroes = 0
        for x in range(0, 4):  # 0 1 2 3
            if self.masca[x] == 255:
                continue
            else:
                nr_zeroes_cur = 255 - self.masca[
                    x] + 1  # de ex 255-252 = 3 + 1 = 4 ; sqrt(4) = 2 = numarul de zerouri din masca din valoare curenta : 11111100 = 252
                nr_zeroes += math.log2(nr_zeroes_cur)

        self.total_ips = 2 ** nr_zeroes  # as formula says : nrOfIPs = 2^x-2, where x is the no of 0's in the subnet mask;
        # this does include the first(gateway) and the last (broadcast) addr

        print("\nNr de ipuri pt masca " + _mask + "  = " + str(self.total_ips))
        print("\nAdresa de retea:" + self.adresa_retea)
        # Build the address pool
        ip = []
        for x in _ip.split('.'):
            ip.append(int(x))
        for i in range(1, int(self.total_ips)):
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

        self.adresa_difuzie = str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3])
        print("\nadresa_difuzie" + self.adresa_difuzie)
        self.server_identifier = str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3] - 1)
        print("\nserver_identifier " + self.server_identifier)

        adreseIP = self.adreseIP.copy()
        for client_ip in adreseIP:
            if client_ip.ip == self.server_identifier or client_ip.ip == self.adresa_difuzie:  # eliminam adresa pt server_identifier, adresa de difuzie
                self.adreseIP.remove(client_ip)

    def getFreeAddress(self, _mac):
        ip = None
        for _ip in self.adreseIP:
            if _ip.free is True and _ip.keep is False:
                _ip.setMac(_mac)
                _ip.set_IP_unavailable()
                ip = _ip
                break
        return ip.ip

    def getIPAddress(self, option50, _mac):
        """
        Functie ce intoarce un obiect IPAddress si care tine cont de urmatoarele:
        1)Intai verificam daca masina care cere o adresa IP este printre cele care au asignat static o adresa IP si aceea le revine doar lor mereu
        2)Verificam preferinta masinii analizand optiunea 50, daca ea exista
        3)Daca niciuna de mai sus nu intoarce un IP masinii, inseamna ca putem aloca un IP oarecare din adress pool ul nostru.
        """
        return_ip =""
        # cazul in care se aloca acelasi ip unei masini (static binding)
        staticIp = self.findIPByMac(_mac)
        if len(staticIp) != 0:
            staticIp = staticIp.pop()
            staticIp.set_IP_unavailable()
            staticIp.keep_IP_address()
            return_ip = staticIp.ip

        #nu e vorba de static binding, deci incercam sa satisfacem cererea clientului
        elif 50 in option50 :
            requested = self.findIPObjByIPAddr(option50[50])
            if requested != None:
                if requested.free == True and requested.keep == False:
                    requested.setMac(_mac)
                    requested.set_IP_unavailable()
                    return_ip = requested.ip
        #alocam o adresa random
        else:
            return_ip= self.getFreeAddress(_mac)

        print("\nIP for client : " + return_ip)
        return return_ip

    def findIPObjByIPAddr(self, _ip):
        return_ip = ""
        for ip in self.adreseIP:
            if ip.ip == _ip:
                return ip
        return None

    def findIPByMac(self, _mac):
        return [ip for ip in self.adreseIP if ip.mac == _mac]
# if __name__ == '__main__':
#     ap = AddressPool("192.168.1.0", "255.255.255.0")
