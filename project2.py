import time
import os
import glob
from coapthon.server.coap import CoAP
from project2resources import TemperatureResource

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('office_temperature/', TemperatureResource())

def main():
    server = CoAPServer("0.0.0.0", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print ("Server Shutdown")
        server.close()
        print ("Exiting...")

if __name__ == '__main__':
    main()
