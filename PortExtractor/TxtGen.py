import sys

class TxtGen():
    def __init__(self):
        self.string = ""

    def write(self, filename=None):
        """Writes a formatted plain text output file tha describes
        the ports of a given module"
        """
        if(filename is None):
            sys.stdout.write(self.string)
            sys.stdout.flush()
        else:
            f = open(filename, 'w')
            f.write(self.string)
            f.close()

    def format(self, module):
        """
        Takes a Module object and formats the data into reStructuredText
        syntax.
        """
        self.string += "%s Ports List\n" % module.name
        for port in module.ports:
            self.string += "%s" % port.name
            if(port.range is not None):
                self.string += "%s" % port.range
            if(port.type is None):
                self.string += "%s" % 'Wire'
            else:
                self.string += " %s" % port.type
            self.string += "\n\n    %s\n\n" % port.comment
