from __future__ import annotations
import socket
import abc
import threading
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

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        print(f"Context: Transition to {type(state).__name__}")
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
        print("Server is waiting for messages")

    @abc.abstractmethod
    def execute(self):
        pass

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context


class WaitForDiscover(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def execute(self):
        while 1:
            try:
                msg = self.server_socket.recvfrom(
                    4096)  # The return value is a pair (bytes, address) where bytes is a bytes object
                # representing the data received and address is the address of the socket sending the data.
                print("\nS:Received discover")
                break
            except:
                print("\nExcept in receiving from socket! find me at server.py, line :" + str(frameinfo.lineno))
        if msg:
            try:
                tthread = threading.Thread(target=self.parseMessageReceived, args=(msg[0], 1)) #acest parametru "1" nu e folosit nicaieri, dar daca las doar parametrul
                                                                                                # msg[0] o ia razna functia si crede ca fiecare caracter din msg[0] e un parametru separat
                tthread.start()
            except:
                print("\nS:Thread can't be started!")

    def parseMessageReceived(self, message, ceva):
        message = Mesaj.Mesaj(message.decode("utf-8"))

        if message.parseazaMesaj() == -1:
            print("\nS:Mesaj gresit, srry")
            print("\nS:Try again!")
            return

        else:
            self.finishDiscoverState(message)

    def finishDiscoverState(self, mesaj):
        """
        Aceasta functie termina starea WaitForDiscover prin trimiterea de mesaj offer catre client si schimbarea starii catre WaitForRequest.
        """

        print(self.responseHandler.__class__.__name__)
        self.responseHandler.raspunde(mesaj)
        self.server_socket.sendto(b'Got you discover message! \nWhat else? ', self.client)
        self.context.transition_to(WaitForRequest())
        self.context.execute()


class WaitForRequest(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def execute(self):
        while 1:
            try:
                msg = self.server_socket.recvfrom(
                    4096)  # The return value is a pair (bytes, address) where bytes is a bytes object
                # representing the data received and address is the address of the socket sending the data.
                print("\nS:received this DHCP Request :" + msg[0].decode())
                break
            except:
                break
        print("\n\nThe rest : TBD...")
        self.context.transition_to(WaitForDiscover())
        self.context.execute()



def start_server():
    concrete_state = WaitForDiscover()
    context = Context(concrete_state)
    context.execute()

