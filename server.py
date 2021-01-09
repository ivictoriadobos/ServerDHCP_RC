from __future__ import annotations
import socket
import abc
import threading
from Mesaj import Mesaj

from inspect import currentframe, getframeinfo

#pentru debug
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
    message = "" #the message received from client at various moments of the process
    client = ("255.255.255.255", 68)
    """("255.255.255.255", 68)"""

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind(('', 67)) #server binds to 67 port

    def __init__(self):
        print("Server is waiting for messages")

    @abc.abstractmethod
    def execute(self):
        pass

    @property
    def context ( self ) -> Context:
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
                    msg = self.server_socket.recvfrom(4096) #The return value is a pair (bytes, address) where bytes is a bytes object
                    # representing the data received and address is the address of the socket sending the data.
                    print("\nS:Received discover" )
                    break
                except:
                    print("\nExcept in receiving from socket! find me at server.py, line :" + str(frameinfo.lineno))
            if msg:
                try:
                    tthread = threading.Thread(target=self.parseMessageReceived, args=(msg[0],1))
                    tthread.start()
                    #threading.Thread(target=self.parseMessageReceived, args= msg[0]).start()
                except:
                    print("S:Thread can't be started!")



    def parseMessageReceived(self, message, ceva): # the parsing step would be interesting to be implemented with chain of resp pattern
        message = Mesaj.Mesaj(message.decode("utf-8"))

        if message.parseazaMesaj() == -1:
            print("\nS:Mesaj gresit, srry")
            print("\nS:Try again!")
            return

        else:
            self.finishDiscoverState()


    def finishDiscoverState(self):
        self.server_socket.sendto(b'Got you discover message! \nWhat else? ',self.client)
        while 1:
            try:
                msg = self.server_socket.recvfrom(4096) #The return value is a pair (bytes, address) where bytes is a bytes object
                # representing the data received and address is the address of the socket sending the data.
                print("\nS:received this DHCP Request :" + msg[0].decode())
            except:
                break
            if msg:
                self.context.transition_to(WaitForRequest())
                self.context.execute()
                break





class WaitForRequest(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def execute(self):
        print("\n\nWaiting for request! TBD...")



def main():
    concrete_state = WaitForDiscover()
    context = Context(concrete_state)
    context.execute()


if __name__ == "__main__":
    main()

