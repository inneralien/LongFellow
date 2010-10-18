import sys

class RstGen():
    def __init__(self):
        self.string = ""

    def write(self, filename=None):
        """Writes a formatted reStructuredText output file tha describes
        the ports of a given module"
        """
        if(filename is None):
            sys.stdout.write(self.string)
            self.stdout.flush()
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
            self.string += ".. describe:: %s\n\n" % port.name
            self.string += "   %s\n\n" % port.comment
