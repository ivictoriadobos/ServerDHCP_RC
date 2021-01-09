import time
from datetime import datetime

DHCPMessageType = {
    1: "DHCPDISCOVER",
    2: "DHCPOFFER",
    3: "DHCPREQUEST",
    4: "DHCPDECLINE",
    5: "DHCPACK",
    6: "DHCPNAK",
    7: "DHCPRELEASE",
    8: "DHCPINFORM"
}



class Optiuni:

    # DESCRIERE DE OPTIUNI INTALNUTE IN ACEST PROGRAM
    # Optiunea 1 : Ofera masca de retea.
    # Optiunea 2 : Ofera diferenta in secunde fata de UTC.
    # Optiunea 3 : Ofera adresa de retea (gatewayul) clientului.The router option specifies a list of IP addresses for routers on the client's subnet. Routers SHOULD be listed in order of preference.
    # Optiunea 6 : Această opțiune specifică o listă de servere DNS disponibile pentru client.
    # Optiunea 12 : Ofera numele clientului ( e optiune de client, clientul ar fi interesat sa trimita numele pentru a putea fi recunoscut de server)
    # Optiunea 15 : Această opțiune specifică numele de domeniu pe care clientul ar trebui să îl utilizeze atunci când rezolvă numele de gazdă prin intermediul DNS.
    # Optiunea 28 : Această opțiune specifică adresa de difuzare utilizată în subrețeaua clientului
    # Optiunea 50 : Această opțiune  este utilizată într-o cerere de client (DHCPDISCOVER) pentru a permite clientului să solicite alocarea unei anumite adrese IP.

     # Optiunea 51 : Această opțiune este utilizată într-o cerere de client (DHCPDISCOVER sau DHCPREQUEST) pentru a permite clientului să solicite un timp de închiriere pentru adresa IP. Într-un răspuns server (DHCPOFFER), un server DHCP folosește această opțiune pentru a specifica timpul de închiriere pe care este dispus să îl ofere.
    # Optiunea 53 : Această opțiune este utilizată pentru a transmite tipul mesajului DHCP.
    # Optiunea 54 : Server Identifier (the ip of the selected server) : Aceasta optiune este utilizata in DHCPOFFER si DHCPREQUEST (optional in DHCPACK si DHCPNAK) pentru a putea oferi clientului posibilitatea de a distinge ofertele de lease.
    # Optiunea 55 :
    # Optiunea 61 :This option is used by DHCP clients to specify their unique identifier.DHCP servers use this value to index their database of address bindings.

    # Optiunea 60 :
#explicatii mai bune : http://wiki.snom.com/Networking/DHCP/Options
    optiuni_valabile = [1,2,3,6,12,15,28,50,51,53,54,55]

    def __init__(self, optiuni):
        self.optiuni = optiuni
        """Sir de cifre/litere in hexa de codeaza optiunile serverului.
        """
        self.optiuni_data = {}
        """Dictionar ce mapeaza pentru fiecare cod de optiune si valoarea sa. Codul optiunii = cheie in dictionar
        """

    def parseazaOptiuni(self):
        """
        Functie ce parseaza sirul in hexa primit la instantiere, cel ce reprezinta optiunile, si mapeaza in dictionarul "optiuni_data" pentru fiecare cod de optiune (cheie in acest dictionar) valoarea
        ce ii revine, faca a face vreo decodare (valorile sunt in continuare codate in hexa).
        """
        idx = 2
        if self.optiuni == "" :
            print("\nclass Optiuni, method parseazaOptiuni : No options found!")

        else:
            while idx < len(self.optiuni):
                codul_optiunii = int(self.optiuni[idx-2:idx], base= 16)
                # codul optiunii are lungimea de 1 octet (deci 2 litere/cifre in hexa, iar optiunile constituie un string de cifre/litere in hexa)

                lungime_optiune = int(self.optiuni[idx:idx+2], base=16) *2
                #lungimea optiunii reprezinta numarul de octeti al optiunii (valorii ei de fapt), prin urmare numarul efectiv de litere/cifre ce codeaza optiunea e numarul de octeti al optiunii * 2

                print("\nOptiuni.parseazaOptiuni : just parsed option " + str(codul_optiunii) + " ; length of the option is : " + str(lungime_optiune))
                print("This option looks like:\n\tcode : " + str(self.optiuni[idx-2:idx])+"\n\tlength, length*2 : " + str(self.optiuni[idx:idx+2]) + "," +
                  str(int(self.optiuni[idx:idx+2], base=16)*2) + "\n\toptiuni_data[codul_optiunii] : " + str(self.optiuni[idx:idx+2+lungime_optiune]) + "\n")
                if codul_optiunii in self.optiuni_valabile :
                    self.optiuni_data[codul_optiunii] = self.optiuni[idx+2 : idx+2+lungime_optiune]
                idx+=lungime_optiune+4
                #folosind aceasta formula vom fi mereu la "granita" dintre codul optiunii viitoare si lungimea sa
                # (practic optiuni[idx] va fi egal cu prima litera din cadrul lungimii optiunii viitoare


    def decodeazaOptiuni(self):
        """
        Functie ce traduce din hexa in zecimal/sir de caractere valorile optiunilor parsate in "parseazaOptiuni"
        """

        for cod_optiune in self.optiuni_data.keys():

            #Masca de subretea
            if cod_optiune == 1:
                self.optiuni_data[1] = self.parseazaAdresaIP(self.optiuni_data[1])

            # Diferenta in secunde fata de UTC
            if cod_optiune == 2:
                ts = time.time()
                utc_offset = (datetime.fromtimestamp(ts) - datetime.utcfromtimestamp(ts)).total_seconds()
                self.optiuni_data[2] = str(int(utc_offset))

            # Adresa de retea (gateway)
            if cod_optiune == 3:
                aux = ""
                startIndex = 0
                endIndex = 8
                lungimeOptiune = len(self.optiuni_data[cod_optiune])
                while endIndex <= lungimeOptiune:
                    aux += self.parseazaAdresaIP(self.optiuni_data[cod_optiune][startIndex:endIndex])
                    if endIndex != lungimeOptiune: #pot fi mai multe adrese de rutere
                        aux += " "
                    startIndex = endIndex
                    endIndex += 8
                self.optiuni_data[cod_optiune] = aux

            # Lista de servere DNS disponibile pentru client
            if cod_optiune == 6:
                aux = ""
                startIndex = 0
                endIndex = 8
                lungimeOptiune = len(self.optiuni_data[cod_optiune])
                while endIndex <= lungimeOptiune:
                    aux += self.parseazaAdresaIP(self.optiuni_data[cod_optiune][startIndex:endIndex])
                    if endIndex != lungimeOptiune: #pot fi mai multe adrese
                        aux += ", "
                    startIndex = endIndex
                    endIndex += 8
                self.optiuni_data[cod_optiune] = aux

            # Numele de domeniu
            if cod_optiune == 15:
                self.optiuni_data[cod_optiune] = self.parseazaString(self.optiuni_data[cod_optiune])

            # Adresa de difuzie
            if cod_optiune == 28:
                self.optiuni_data[cod_optiune] = self.parseazaAdresaIP(self.optiuni_data[cod_optiune])

            # Adresa ip ceruta
            if cod_optiune == 50:
                self.optiuni_data[cod_optiune] = self.parseazaAdresaIP(self.optiuni_data[cod_optiune])
                print("\nOptiuni.decodeazaOptiuni; clientul a cerut adresa ip : " + self.optiuni_data[cod_optiune])

            # Lease time ul cerut
            if cod_optiune == 51:
                self.optiuni_data[cod_optiune] = int(self.optiuni_data[cod_optiune], base=16)

            # tipul de mesaj DHCP
            if cod_optiune == 53:
                self.optiuni_data[cod_optiune] = DHCPMessageType[int(self.optiuni_data[cod_optiune], base=10)]

            # Server Identifier : The identifier is the IP address of the selected server.
            if cod_optiune == 54:
                self.optiuni_data[cod_optiune] = self.parseazaAdresaIP(self.optiuni_data[cod_optiune])


                # Parameter Request List
            if cod_optiune == 55:
                optiuni_cerute= []
                optiuni = self.optiuni_data[cod_optiune]
                ind = 0
                print("\nOptiuni.decodeazaOptiuni; valoarea optiunii 55 este : ")
                while ind < len(optiuni):
                    optiuni_cerute.append(int(optiuni[ind:ind+2], base=16))
                    print(str(int(optiuni[ind:ind+2], base=16)))
                    ind += 2
                self.optiuni_data[cod_optiune] = [cod for cod in optiuni_cerute if cod in self.optiuni_valabile] #poate clientul a cerut si luna de pe cer, dar noi avem doar
                                                                                                                # o submultime din optiunile posibile


    def parseazaAdresaIP(self, adresa):

        if len(adresa) != 8:
            return False
        else:
            _adresa = str(int(adresa[0:2], base=16)) + "." + str(int(adresa[2:4], base=16)) + "." + str(int(adresa[4:6], base=16)) + "." + str(int(adresa[6:8], base=16))

        return _adresa

    def parseazaString(self, _string):
        if len(_string) == 0:
            return False
        else:
            string = ""
            startIndex = 0 #lungimea minima a acestei optiuni e 1 octet (deci 2 litere/cifre din _string), lungimea putand (sau nu) sa creasca cu minim cate 1 octet
            endIndex = 2
            while endIndex <= len(_string):
                string += chr(int(_string[startIndex:endIndex], base=16))
                start = endIndex
                endIndex += 2
            return string

    def getOptiuni(self):
        return self.optiuni_data