import threading
from tkinter import *

import server
from AddressStuff import AddressPool
import re
import time
from datetime import datetime

def getUTCdiffInSeconds():
    ts = time.time()
    utc_offset = (datetime.fromtimestamp(ts) -
              datetime.utcfromtimestamp(ts)).total_seconds()
    return int(utc_offset)


class GUI:
    check_options = [2, 28]
    entry_options = [1, 3, 6, 15]
    values_of_options = {}
    options_name = {
        1: "Masca de subretea",
        2: "Diferenta in secunde fata de UTC",
        3: "Ruter",
        6: "DNS Servers",
        15: "Domain Name",
        28: "Adresa de difuzie"
    }
    selected_options = {}
    """
    Dictionar ce memoreaza setarile serverului in materie de optiuni
    """

    address_pool = None

    def __init__(self, _parent):
        self.parent = _parent
        self.createGUI()

    def createGUI(self):
        self.parent.title("Server interface")

        # Frame pentru de retea
        adresaRetea_masca_Frame = LabelFrame(self.parent, text="Adresa de retea si masca", width=40, height=10)
        adresaRetea_masca_Frame.grid(row=0, column=2, sticky=(N, E, W, S), ipadx=20, ipady=10, padx=5, pady=5)

        self.adresaRetea = Entry(adresaRetea_masca_Frame, width=25)
        self.adresaRetea.grid(row=0, column=1)
        self.adresaRetea.insert(0, "192.168.1.0")

        self.masca = Entry(adresaRetea_masca_Frame, width=25)
        self.masca.grid(row=1, column=1)
        self.masca.insert(0, "255.255.255.0")

        leaseFrame = LabelFrame(self.parent, text="Lease Time", width=40, height=10)
        leaseFrame.grid(row=2, column=2, sticky=(N, E, W, S), ipadx=20, ipady=10, padx=5, pady=5)

        self.leaseTime = Entry(leaseFrame, width=25)
        self.leaseTime.grid(row=2, column=1)
        self.leaseTime.insert(0, "1000")

        # frame-ul unde se afla optiunile
        option_frame = LabelFrame(self.parent, width=40, height=150, text="Optiuni:")
        option_frame.grid(row=4, column=2, sticky=(N, E, W, S), ipadx=10, ipady=10, padx=5, pady=5)

        rowNum = 0
        for check in self.check_options:
            val = IntVar()
            chk = Checkbutton(option_frame, text="Option " + str(check) + ": " + self.options_name[check], variable=val)
            chk.grid(row=rowNum, column=0, sticky=W, pady=5)
            self.values_of_options[check] = val
            rowNum += 1


        for entry in self.entry_options:
            Label(option_frame, text="Option: " + str(entry) + ": " + self.options_name[entry]).grid(row=rowNum,
                                                                                                     column=0, sticky=W,
                                                                                                     pady=5)
            ent = Entry(option_frame, width=25)
            ent.grid(row=rowNum, column=1, pady=5)
            self.values_of_options[entry] = ent
            rowNum += 1

        comand_buttons = Frame(self.parent)
        comand_buttons.grid(row=8, column=1, columnspan=2, ipadx=10, ipady=10, padx=5, pady=5)

        self.quitButton = Button(comand_buttons, text="Quit", command=self.exitServer, width=30)
        self.quitButton.grid(column=1, row=0, padx=30)

        self.startButton = Button(comand_buttons, text="Start", command=self.start_server, width=30)
        self.startButton.grid(column=0, row=0, padx=30)

    def exitServer(self):
        server.State.server_socket.close()
        # take care to close server socket
        exit()

    def start_server(self):
        print("\nServerul ofera optiunile 1,2,3,6,15,28,51")
        self.getInput()

        thread = threading.Thread(target=server.start_server, args=[self.adresa_masca, self.selected_options, self.address_pool]).start()
        # server.start_server()

    def getInput(self):
        adresa_retea = self.adresaRetea.get()
        print("\n\tadresa_retea : " + adresa_retea)

        masca = self.masca.get()
        print("\n\tmasca : " + masca)

        leasetime = self.leaseTime.get()

        self.adresa_masca = {"adresa" : adresa_retea, "masca" : masca}

        #intai verificam daca adresa de retea, masca si leasetimeul sunt introduse corect
        if self.checkAddress(adresa_retea) and self.checkAddress(masca) and int(leasetime) > 0:
            self.address_pool = AddressPool.AddressPool(adresa_retea, masca)  # cream address poolul deoarece avem date corecte

            if self.checkAndSaveOptions() == True:  # verificam inputurile optiunilor si le si salvam; daca sunt corecte si acestea trecem la urmt.
                self.selected_options[51] = leasetime
                return # este totul ok si putem porni serverul


        print("\nDate introduse gresit! Aplicatia se inchide.") #trebuie neaparat sa fac ceva aici sa fie mai omeneasca iesirea din aplicatie
        self.exitServer()



    def checkAddress(self, _address):
        address = _address.split(".")
        if len(address) != 4:
            return False
        for value in address:
            if int(value) > 255 or int(value) < 0:
                return False

        return True

    def checkAndSaveOptions(self):
        """
        Verificam valorile introduse in formele de input si le salvam in self.selected_options.
        """
        total_options = self.entry_options + self.check_options
        result = True
        for option in [x for x in total_options if
                       self.values_of_options[x].get() not in ["",0]]:  # selectam toate optiunile care se folosesc
            if option == 1:
                result = result and self.checkAddress(self.values_of_options[1].get())
                self.selected_options[1] = self.values_of_options[1].get()  # memoram masca de subretea

            if option == 3:
                valoaresplituita = re.split("\s|[.]", self.values_of_options[3].get())
                if len(valoaresplituita) < 4 or len(valoaresplituita) % 4 != 0:
                    result = result and False  # este macar o adresa gresit introdusa
                else:
                    adrese = re.split("\s", self.values_of_options[3].get())  # verificam fiecare adresa introdusa sa fie ok
                    for adresa in adrese:
                        self.selected_options[3] = adresa
                        result = result and self.checkAddress(adresa)


            if option == 2:
                self.selected_options[2] = getUTCdiffInSeconds()

            if option == 28 :
                self.selected_options[28] = self.address_pool.adresa_difuzie

            if option == 6:
                self.selected_options[6] = self.values_of_options[6].get()

            if option == 15:
                self.selected_options[15] = self.values_of_options[15].get()

        # la optiunea 6 si 15 ne prefacem ca nu mai trebuie sa facem vreo verificare din moment ce se poate introduce cam orice combinatie litera/cifra

        print("\nS-au ales din interfata optiunile de server:" , end='')
        for optiunek, optiunev in self.selected_options.items():
            print(str(optiunek) + " cu valoarea " + str(optiunev) + "\n")
        return result
#
#
if __name__ == '__main__':
    root = Tk()
    root.resizable(0, 0)
    root.geometry("800x800")
    serverr = GUI(root)
    root.mainloop()

