import re
from NullHandler import NullHandler
from Exceptions import *
import logging

module_name_re = re.compile(r'^\s*module\s+(\w+)')
module_end_re = re.compile(r'.*\)\s*;')
#port_re = re.compile(r'^\s*(input|output|inout)\s+(wire|reg)?\s+(\[\d+:\d+\])?\s*(\w+),?\s*/?/? *(.*)')
#port_re = re.compile(r'^\s*(input|output|inout)\s+(signed wire|signed reg|wire|reg|signed)?\s*(\[\w+:\w+\])?\s*(\w+)')
port_re = re.compile(r'^\s*(input|output|inout)\s+(signed wire|signed reg|wire|reg|signed)?\s*(\[.+:.+\])?\s*(\w+)')
meta_re = re.compile(r'\/\/\s*(.*)')
comments_re = re.compile(r'\s*\/\/\s?(.*)')

class Port():
    def __init__(self):
        self.direction = ""
        self.type = "wire"
        self.range = ""
        self.name = ""
        self.comments = []
        self.meta = None

    def setDirection(self, dir):
        if(dir is None):
            raise Exception
        else:
            self.direction = dir

    def setType(self, type):
#        print "TYPE:", type
#        if(type == ""):
        if(type is None):
            self.type = 'wire'
        else:
            self.type = re.sub(r' +',',',type.strip())

    def setRange(self, range):
        self.range = range

    def setName(self, name):
        if(name is None):
            raise Exception
        else:
            self.name = name

    def setMeta(self, meta):
        self.meta = meta

    def addComment(self, comment):
        self.comments.append(comment)

class Module():
    def __init__(self, name):
        self.name = name
        self.ports = []
        self.comment = []

    def addPort(self, port):
        self.ports.append(port)

    def addPortComment(self, comment):
        pass

    def addComment(self, comment):
        self.comment.append(comment)

class PortExtractor():
    def __init__(self):
        self.logger = logging.getLogger("PortExtractor")
        h = NullHandler()
        logging.getLogger("PortExtractor").addHandler(h)

        self.modules = []

    def parseFile2(self, file):
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

    def parseFile(self, file):
        state = None
        found_module = False
        in_ports = False
        f = open(file)
        port = None
        for line in f.readlines():
            mn = module_name_re.match(line)
            if(mn is not None):
                self.logger.debug("== Begin Module")
                module_name = mn.group(1)
                module = Module(module_name)
                self.modules.append(module)
                found_module = True
            if(found_module):
                m = port_re.match(line)
                if(m is not None):
                    if(port is not None):   ## Add previous port
                        module.addPort(port)
                        port = None
                        meta = None

                    self.logger.debug("==== Ports")
                    port = Port()
                    self.logger.debug(m.groups())

                    meta_m = meta_re.search(line)
                    if(meta_m is not None):
                        port.setMeta(meta_m.group(1))
                        self.logger.debug("META: %s" % (port.meta))
                    port.setDirection(m.group(1))
                    port.setType(m.group(2))
                    port.setRange(m.group(3))
                    port.setName(m.group(4))
                    in_ports = True
                else:
                    c = comments_re.match(line)
                    if(c is not None):
                        if(not in_ports):
                            module.addComment(c.group(1))
                            self.logger.debug("  = Module Comments")
                        else:
                            self.logger.debug("  = Port Comments")
                            port.addComment(c.group(1))
                        self.logger.debug("    %r" % c.groups(1))
                mend = module_end_re.match(line)
                if(mend is not None):
                    self.logger.debug("== End Module")
                    module.addPort(port)
                    found_module = False
                    in_ports = False

        f.close()
