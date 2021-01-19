from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
from Mesaj import Mesaj


context = None
"""Referinta la contextul actual"""


def getResponseHandlerChain():
    handleDiscover = DiscoverHandler()
    handleRequest = RequestHandler()
    handleRelease = ReleaseHandler()

    handleRelease.set_next(handleRequest).set_next(handleDiscover)
    # handleDiscover.raspunde("01")
    return handleRelease




# un lant de responsabilitati care sa fie apelat de exemplu o data in finish discover state; ce sa se intample? sa preia mesajul discover parsat si acest handler sa si dea
# seama ca e vorba de un mesaj discover si ca trebuie sa trimita un offer inapoi spre client. sa fie ceva de genu chainRaspunde.raspunde(mesajulMeuParsat)


class ResponseHandler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """
    options_from_discover ={}
    lease_time = {} #dictionar de retine ce leasetime are fiecare client

    @abstractmethod
    def set_next(self, handler: ResponseHandler) -> ResponseHandler:
        pass

    @abstractmethod
    def raspunde(self, request) -> Optional[str]:
        pass


class AbstractHandler(ResponseHandler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: ResponseHandler = None

    def set_next(self, handler: ResponseHandler) -> ResponseHandler:
        self._next_handler = handler
        print("\nCalling from " + self.__class__.__name__)
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def raspunde(self, mesaj: Mesaj) -> str:
        print("\nType of messaje to respond to : " + mesaj.getTypeOfMessage())
        if self._next_handler:
            return self._next_handler.raspunde(mesaj)

        print("\nNu stiu sa raspund la acest mesaj : " + mesaj.getTypeOfMessage())
        return None


"""
All Concrete Handlers either handle a request or pass it to the next handler in
the chain.
"""


class DiscoverHandler(AbstractHandler):

    def raspunde(self, mesaj:Mesaj) -> str:
        if mesaj.getTypeOfMessage() == "DHCPDISCOVER":
            print("\nOoo, raspundem la DHCPDISCOVER")

            #schimbam tipul mesajului  ca sa fie de tip raspuns de la server
            mesaj.setTypeOfMessage("02") #setam ca mesaj de la server

            #ii dam clientului o adresa
            getIP = context.address_pool.getIPAddress(mesaj.optiuni, mesaj.chaddr)
            mesaj.setYiaddr(getIP)

            # ii punem identifierul de server
            mesaj.optiuni[54] = context.address_pool.server_identifier

            # configure the other options

            if 55 in mesaj.optiuni.keys():
                for optiune in mesaj.optiuni:


            # if 55 in message.options:#daca avem lista de optiuni cerute de client
            #     for option in message.options[55]:#printre optiunile cerute de client
            #         if option in self.configurations:#daca aceste optiuni sunt oferite de serverul nostru
            #             message.options[option] = self.configurations[option]
            # else:
            #     for i in message.options.keys():
            #         if i in self.configurations:
            #             message.options[i] = self.configurations[i]
            #
            # # remove useless option
            # for roption in [option for option in message.options if option not in self.configurations and option != 53 and option != 51 and option != 54]:
            #     message.options.pop(roption)
            #
            # # save options send for the future use
            # self.optionSendInDiscovery[message.chaddr] = message.options
            # logger.info(" DHCPOFFER ready to transmit!")
            #


            print("\nAm terminat de raspuns la DHCPDISCOVER")
        else:
            return super().raspunde(mesaj)


class RequestHandler(AbstractHandler):
    def raspunde(self, request: Any) -> str:
        if request == "Nut":
            return f"Squirrel: I'll eat the {request}"
        else:
            return super().raspunde(request)


class ReleaseHandler(AbstractHandler):
    def raspunde(self, request: Any) -> str:
        if request == "MeatBall":
            return f"Dog: I'll eat the {request}"
        else:
            return super().raspunde(request)



