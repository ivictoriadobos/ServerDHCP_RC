from __future__ import annotations
import socket
import abc
import threading
import chainOfResp
from AddressStuff import AddressPool
from Mesaj import Mesaj
from chainOfResp import getResponseHandlerChain
from inspect import currentframe, getframeinfo

# pentru debug
frameinfo = getframeinfo(currentframe())



class Context:
    """
    Define the interface of interest to clients.
    Maintain an instance of a ConcreteState subclass that defines the
    current state.
    """
    _state = None
    """
   A reference to the current state of the Context.
   """

    selected_options = {} #optiunile selectate din interfata
    address_pool : AddressPool = None
    adresa_masca ={}



    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        print(f"\n\t***Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def execute(self):
        self._state.execute()


class State(metaclass=abc.ABCMeta):
    """
    Define an interface for encapsulating the behavior associated with a
    particular state of the Context.
    """

    message = ""
    """mesajul primit de la client la diverse momente de timp (discover, request, release...)"""

    client = ("255.255.255.255", 68)
    """tupla pentru a adresa un client fara configurari de retea : ("255.255.255.255", 68)"""

    responseHandler = getResponseHandlerChain()
    """Obiect ce reprezinta un lant de obiecte ce incearca sa raspunda mesajului dat ca parametru metodei "raspunde" """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind(('', 67))  # server binds to 67 port



    def __init__(self):
        print("\n\t***Server is waiting for messages")

    @abc.abstractmethod
    def execute(self):
        pass

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context


class AscultaMesaj(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def execute(self):
        while 1:
            msg = None
            try:
                msg = self.server_socket.recvfrom(
                    4096)  # The return value is a pair (bytes, address) where bytes is a bytes object
                # representing the data received and address is the address of the socket sending the data.
                print("\n\t***Serverul a detectat un mesaj")
                break
            except:
                # pentru debug
                frameinfo = getframeinfo(currentframe())
                print("\n\t***Except in receiving from socket! find me at server.py, line :" + str(frameinfo.lineno))
                break

        if msg != None:
            try:
                tthread = threading.Thread(target=self.parseMessageReceived, args=(msg[0], 1)) #acest parametru "1" nu e folosit nicaieri, dar daca las doar parametrul
                                                                                                # msg[0] o ia razna functia si crede ca fiecare caracter din msg[0] e un parametru separat
                tthread.start()
            except:
                print("\n\t***Server : Thread can't be started!")
        else:
            return

    def parseMessageReceived(self, message, ceva):
        print("\nMesajul:")
        print(message.decode("utf-8"))


        message = Mesaj.Mesaj(message.decode("utf-8"))

        if message.parseazaMesaj() == -1:
            print("\n\t***Server : Mesaj gresit, srry")
            return

        else:

            #de spart mesajul primit si de afisat : serverul a primit mesajul...
            message.printeazaMesaj()
            self.reactioneazaLaMesaj(message)

    def reactioneazaLaMesaj(self, mesaj):
        """
        Aceasta functie termina starea WaitForDiscover prin trimiterea de mesaj offer catre client si schimbarea starii catre WaitForRequest.
        """

        mesajClient = self.responseHandler.raspunde(mesaj)
        mesajClient.printeazaMesaj()

        #mesajul e bun, trebuie de trimis la client
        # self.server_socket.sendto

        #de splituit mesajul pe care l-am trimis inapoi (pe care trebuie sa-l trimitem clientului)
        #si de afisat gen : serverul raspunde cu mesjul ...
        m = b''
        m=mesajClient.messageToBytes()
        print()
        self.server_socket.sendto(b'Mi-ai dat mesaj si ti-am raspuns, what else? ', self.client)

        self.execute()




def start_server(adresa_masca, optiuni_selectate, address_pool):
    concrete_state = AscultaMesaj()
    context = Context(concrete_state)

    context.address_pool = address_pool
    context.adresa_masca = adresa_masca
    context.selected_options = optiuni_selectate
    chainOfResp.context = context  #urat tare, stiu, da' altfel nu reusesc
    context.execute()


