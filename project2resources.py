import time
import os
import glob
import math
from coapthon import defines

from coapthon.resources.resource import Resource

#Needed for temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


class TemperatureResource(Resource):

    def __init__(self, name="TemperatureResource", coap_server=None):
        super(TemperatureResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        #Should never return this, if you do there could be an error somewhere
        self.payload = "No Temperature Recorded Yet"

    def render_GET(self, request):
        #Read temperature sensor, convert for a second reading in F, and format string
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            temp_c = math.trunc(temp_c * 20) / 20
            temp_f = math.trunc(temp_f * 20) / 20
            self.value = temp_c, temp_f

        #Return temp on GET
        self.payload = str(self.value)
        return self

#Per project2 guidelines, only GET is implemented, this is standard code from default resources class
    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, TemperatureResource())
        return res

    def render_DELETE(self, request):
        return True

