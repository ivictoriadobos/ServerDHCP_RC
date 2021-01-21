from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional

import server
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
            print("\n\tRaspundem la DHCPDISCOVER")

            #schimbam tipul mesajului  ca sa fie de tip raspuns de la server + sa fie offer
            mesaj.setTypeOfMessage("DHCPOFFER")
            mesaj.op = "02"#setam ca mesaj de la server

            #ii dam clientului o adresa
            getIP = context.address_pool.getIPAddress(mesaj.optiuni, mesaj.chaddr)
            mesaj.setYiaddr(getIP)



            #implementarea ierarhiei modalitatii de alocare a lease timeului :
            # 1: cererea clientului
            # 2(nu): lease timeul predefinit pentru un anumit MAC
            # 3: lease time default
            if 51 in mesaj.optiuni:
                requested_lease_time = int(mesaj.optiuni[51])
                if requested_lease_time > 8000:
                    requested_lease_time = context.selected_options[51]
                mesaj.optiuni[51] = requested_lease_time
            else:
                    mesaj.optiuni[51] = context.selected_options[51]


            # ii punem identifierul de server
            mesaj.optiuni[54] = context.address_pool.server_identifier

            # configure the other options

            if 55 in mesaj.optiuni.keys():
                for optiune in mesaj.optiuni[55]:
                    # aici punem in optiunile mesajului chestiile configurate pe interfata serverului
                    if optiune in context.selected_options.keys():
                        mesaj.optiuni[optiune] = context.selected_options[optiune]
            else:
                for i in mesaj.optiuni.keys():
                    if i in context.selected_options.keys():
                        mesaj.optiuni[i] = context.selected_options[i]

            for removeopt in [option for option in mesaj.optiuni if option not in context.selected_options and option not in [ 53,54,51,50]]:
                mesaj.optiuni.pop(removeopt)

            print("\n\tAm terminat de raspuns la DHCPDISCOVER\n")

            return mesaj


        else:
            return super().raspunde(mesaj)


class RequestHandler(AbstractHandler):
    def raspunde(self, mesaj:Mesaj) -> str:
        if mesaj.getTypeOfMessage() == "DHCPREQUEST":
            print("\n\tRaspundem la DHCPREQUEST")

            #schimbam tipul mesajului  ca sa fie de tip raspuns de la server + sa fie offer
            mesaj.setTypeOfMessage("DHCPACK")
            mesaj.op = "02"#setam ca mesaj de la server
            print("\n\tAici ar trebui sa verificam daca mesajul de request se adreseaza serverului nostru inainte sa continuam, in caz contrar eliberam resursele alocate si dam drop la pachet")
            print("\n\tAm terminat de raspuns la DHCPREQUEST\n")

            return mesaj


        else:
            return super().raspunde(mesaj)



class ReleaseHandler(AbstractHandler):
    def raspunde(self, request: Any) -> str:
        if request == "MeatBall":
            return f"Dog: I'll eat the {request}"
        else:
            return super().raspunde(request)



