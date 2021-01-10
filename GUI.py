import threading
from tkinter import *
from AddressStuff import AddressPool
import server

class GUI:
    check_options = [2,28]
    entry_options = [1,3,6,15]
    values_of_options ={}
    options_name = {
        1 : "Masca de subretea",
        2: "Diferenta in secunde fata de UTC",
        3 : "Ruter",
        6 : "DNS Servers",
        15 : "Domain Name",
        28 : "Adresa de difuzie"
    }

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
        leaseFrame.grid(row=2, column=2,sticky=(N,E,W,S), ipadx=20, ipady=10, padx = 5, pady = 5)

        self.leaseTime = Entry(leaseFrame, width=25)
        self.leaseTime.grid(row=2, column=1)
        self.leaseTime.insert(0, "1000")

        # frame-ul unde se afla optiunile
        option_frame = LabelFrame(self.parent, width=40, height=150, text="Optiuni:")
        option_frame.grid(row=4, column=2, sticky=(N, E, W, S), ipadx=10, ipady=10, padx=5, pady=5)

        rowNum=0
        for check in self.check_options:

            val = IntVar()
            chk = Checkbutton(option_frame, text="Option " + str(check) + ": " + self.options_name[check], variable = val)
            chk.grid(row = rowNum, column = 0, sticky = W,pady =5)
            self.values_of_options[check] = val
            rowNum+=1


        for entry in self.entry_options:
                Label(option_frame, text="Option: "+str(entry) + ": "  + self.options_name[entry]).grid(row=rowNum, column=0, sticky=W, pady=5)
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
        #take care to close server socket
        exit()

    def start_server(self):
        adresa_retea = self.adresaRetea.get()
        print("\nadresa_retea : " + adresa_retea)
        masca = self.masca.get()
        print("\nmasca : " + masca)
        address_pool = AddressPool.AddressPool(adresa_retea, masca)
        thread = threading.Thread(target=server.start_server).start()
        # server.start_server()
