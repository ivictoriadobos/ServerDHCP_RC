from Mesaj import Optiuni
from time import time


class Mesaj:
    def __init__(self, _mesajDHCP):
        self.mesajDHCP = _mesajDHCP
        self.op = ""
        """
        Tipul mesajului : # 1  client -> server, 2  server -> client (1 octet)
        """

        self.htype = 1
        """
        Hardware type (by default 1) (1 octet)
        """

        self.hlen = 6
        """
        Hardware Address Length: Specifies how long hardware addresses are in this message
        (pentru ethernet (htype = 1) e 6) ( 1 octet )
        """

        self.hops = 0
        """
        Set to 0 by a client before transmitting a request and used by relay agents to control the forwarding of BOOTP 
        and/or DHCP messages  ( 1 octet )
         """

        self.xid = ""
        """Transaction Identifier : field generated by the client, to allow it to match up the request with replies 
        received from DHCP servers. ( 4 octeti )"""

        self.secs = ""
        """For DHCP, it is defined as the number of seconds elapsed since a client began an attempt to acquire or renew a 
        lease. This may be used by a busy DHCP server to prioritize replies when multiple client requests are outstanding 
         (2 octeti) """

        self.flags = ""
        """B subfield ( 1 octet ) : a client that doesn't know its own IP address at the time it sends its request sets 
        this flag to 1. This serves as an immediate indicator to the DHCP server or relay agent that receives the request 
        that it should send its reply back by broadcast. Reserved subfield (1 octet) : set to zero and not used (2 
        octeti) """

        self.ciaddr = ""
        """The client puts its own current IP address in this field if and only if it has a valid IP address while in the 
        BOUND, RENEWING or REBINDING states; otherwise, it sets the field to 0. The client can only use this field when 
        its address is actually valid and usable, not during the process of acquiring an address. Specifically, 
        the client does not use this field to request a particular IP address in a lease; it uses the Requested IP 
        Address DHCP option. (4 octeti) """

        self.yiaddr = ""
        """“Your” IP Address: The IP address that the server is assigning to the client.
        (4 octeti)"""

        self.siaddr = ""
        """In DHCP, it is the address of the server that the client should use for the next step in the bootstrap 
        process, which may or may not be the server sending this reply. 
    The sending server always includes its own IP address in the Server Identifier DHCP option.
        (4 octeti)"""

        self.giaddr = ""
        """This field is used just as it is in BOOTP, to route BOOTP messages when BOOTP relay agents are involved to 
        facilitate the communication of BOOTP requests and replies between a client and a server on different subnets or 
        networks. (4 octeti) """

        self.chaddr = ""
        """Client Hardware Address: The hardware (layer two) address of the client, which is used for identification and 
        communication. (16 octeti) """

        self.sname = ""
        """Server Name: The server sending a DHCPOFFER or DHCPACK message may optionally put its name in this field. This 
        can be a simple text “nickname” or a fully-qualified DNS domain name (such as “myserver.organization.org”). (64 
        octeti ) """

        self.file = ""
        """
        Optionally used by a client to request a particular type of boot file in a DHCPDISCOVER message. Used by a server in a
         DHCPOFFER to fully specify a boot file directory path and filename. (128 octeti)"""
        self.magic_cookie = "63.82.53.63"
        """
        Magic cookie (4 octeti)"""

        self.optiuni = {}


    def parseazaMesaj(self):
            startIndex = 0
            endIndex = 0
            # valorile sunt hardcodate deoarece nu ne intereseaza sa oferim functionalitate variabila unor lungimi definite
            # OP
            endIndex += 2
            self.op = self.mesajDHCP[startIndex:endIndex]
            print("\nMesaj:\t op : " + str(self.op))

            # HTYPE
            startIndex = endIndex
            endIndex += 2
            self.htype = self.mesajDHCP[startIndex:endIndex]
            print("\nMesaj:\t htype : " + str(self.htype))


            # HLEN
            startIndex = endIndex
            endIndex += 2
            self.hlen = self.mesajDHCP[startIndex:endIndex]

            # HOPS
            startIndex = endIndex
            endIndex += 2
            self.hops = self.mesajDHCP[startIndex:endIndex]

            # XID
            startIndex = endIndex
            endIndex += 8
            self.xid = self.mesajDHCP[startIndex:endIndex]

            # SECS
            startIndex = endIndex
            endIndex += 4
            self.secs = self.mesajDHCP[startIndex:endIndex]

            # FLAGS
            startIndex = endIndex
            endIndex += 4
            self.flags = self.mesajDHCP[startIndex:endIndex]

            # CIADDR
            startIndex = endIndex
            endIndex += 8
            self.ciaddr = self.mesajDHCP[startIndex:endIndex]
            self.ciaddr = self.parseazaAdresaIP(self.ciaddr)
            print("\nMesaj:\t ciaddr : " + str(self.ciaddr))

            if not self.ciaddr:
                return -1

            # YIADDR
            startIndex = endIndex
            endIndex += 8
            self.yiaddr = self.mesajDHCP[startIndex:endIndex]
            self.yiaddr = self.parseazaAdresaIP(self.yiaddr)
            if not self.yiaddr:
                print("\nHere in yiaddr")
                return -1

            # SIADDR
            startIndex = endIndex
            endIndex += 8
            self.siaddr = self.mesajDHCP[startIndex:endIndex]
            self.siaddr = self.parseazaAdresaIP(self.siaddr)
            if not self.siaddr :
                print("\nHere in siaddr")
                return -1

            # GIADDR
            startIndex = endIndex
            endIndex += 8
            self.giaddr = self.mesajDHCP[startIndex:endIndex]
            self.giaddr = self.parseazaAdresaIP(self.giaddr)
            if not self.giaddr :
                print("\nHere in giaddr")
                return -1

            # CHADDR
            startIndex = endIndex
            endIndex += 32
            self.chaddr = self.mesajDHCP[startIndex:endIndex]
            self.chaddr = self.parseazaMAC(self.chaddr)
            if not self.chaddr:
                print("\nHere in chaddr")
                return -1

            # SNAME
            startIndex = endIndex
            endIndex += 128
            self.sname = self.mesajDHCP[startIndex:endIndex]
            self.sname = self.parseazaString(self.sname)
            if self.sname is False:
                print("\nHere in sname")
                return -1
            else:
                print("\n%%% SNAME = "  + self.sname)

            # FILE
            startIndex = endIndex
            endIndex += 256
            self.file = self.mesajDHCP[startIndex:endIndex]
            self.file = self.parseazaString(self.file)
            if  self.file is False:
                print("\nMesaj: \t file : " + str(self.file))
                return -1

            # MAGIC COOKIE
            startIndex = endIndex
            endIndex += 8
            self.magic_cookie = self.mesajDHCP[startIndex:endIndex]
            print("\nMesaj:\t magic cookie : " + str(self.magic_cookie))

            # OPTIONS
            startIndex = endIndex
            print("\n!!!!!!!!!!!!!!\tIf endIndex = 480, set endIndex = len(self.mesajDHCP); endIndex = " + str(endIndex))
            endIndex += len(self.mesajDHCP) - 240*2 # 240*2 = lungimea by default a unui mesaj dhcp pana la optiuni in cifre/litere (240 de octeti)


            _optiuni = Optiuni.Optiuni(self.mesajDHCP[startIndex:endIndex])

            _optiuni.parseazaOptiuni()
            _optiuni.decodeazaOptiuni()
            self.optiuni = _optiuni.getOptiuni()

            for option in self.optiuni:
                if not self.optiuni[option] : #daca vreo optiune e eronata/ nu s-a parsat bine
                    return -1
            return 0

    def parseazaAdresaIP(self, adresa):

        if len(adresa) != 8:
            return False
        else:
            _adresa = str(int(adresa[0:2], base=16)) + "." + str(int(adresa[2:4], base=16)) + "." + str(int(adresa[4:6], base=16)) + "." + str(int(adresa[6:8], base=16))

        return _adresa

    def parseazaMAC(self, adresa):
        if len(adresa) != 32: #in mesaj sunt 16 octeti pentru adresa MAC, desi ea e compusa doar din 6..
            return False
        else:
            # newAddress = "%s:%s:%s:%s:%:%s" %
            # (address[0:2], address[2:4], address[4:6],address[6:8],address[8:10],address[10:12])
            mac = adresa[0:2] + ":" + adresa[2:4] + ":" + adresa[4:6] + ":" + adresa[6:8] + ":" + adresa[8:10] + ":" + adresa[10:12]
            return mac

    def parseazaString(self, _string):
        if _string == None:
            _string = "Nothing to show"
        print("\nMesaj : Parsing string : " + _string)
        if len(_string) == 0:
            print("\nMesaj : string length = 0! ")
            return False
        else:
            string = ""
            startIndex = 0 # mergem din octet in octet (deci verificam cate 2 litere/cifre)
            endIndex = 2
            while _string[startIndex:endIndex] != "00" and endIndex <= len(_string):
                string += chr(int(_string[startIndex:endIndex], base=16))
                startIndex = endIndex
                endIndex += 2
            print("\nMesaj : returning this string after parsing : " + string )
            return string

    def getTypeOfMessage(self):
        return self.op

    def setTypeOfMessage(self, string):
        self.op = string

    def setYiaddr(self, string):
        self.yiaddr = string
