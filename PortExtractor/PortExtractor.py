import re
from NullHandler import NullHandler
from Exceptions import *
import logging

module_name_re = re.compile(r'^\s*module\s+(\w+)')
port_re = re.compile(r'^\s*(input|output|inout)\s+(wire|reg)?\s+(\[\d+:\d+\])?\s*(\w+),?\s*/?/? *(.*)')

class Port():
    def __init__(self, port):
        (   self.direction,
            self.type,
            self.range,
            self.name,
            self.comment
        ) = port

class Module():
    def __init__(self, name):
        self.name = name
        self.ports = []

    def addPort(self, port):
        self.ports.append(Port(port))

class PortExtractor():
    def __init__(self):
        self.logger = logging.getLogger("PortExtractor")
        h = NullHandler()
        logging.getLogger("PortExtractor").addHandler(h)

        self.modules = []

    def parseFile(self, file):
        f = open(file)
        for line in f.readlines():
            # Search for module name
            mn = module_name_re.match(line)
            if(mn is not None):
                module_name = mn.group(1)
                module = Module(module_name)
                self.modules.append(module)
            m = port_re.match(line)
            if(m is not None):
                module.addPort(m.groups())
        f.close()
