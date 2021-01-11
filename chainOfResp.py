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

    def getContext(self):
        return self.context

    def setContext(self, _context):
        self.context = _context


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
        if mesaj.getTypeOfMessage() == "01":
            print("\nOoo, raspundem la DHCPDISCOVER")
            mesaj.setTypeOfMessage("02") #setam ca mesaj DHCPOFFER
            mesaj.setYiaddr(context.address_pool.getIPAddress(mesaj.optiuni, mesaj.chaddr))
            # print("\nTEST : clasa address poolului la care avem acces + nr de ipuri " + str(type(context.address_pool)) + str(context.address_pool.total_ips))

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


