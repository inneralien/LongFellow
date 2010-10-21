import sys
import re

class TeXGen():
    def __init__(self):
        self.string = ""

    def write(self, filename=None):
        """Writes a formatted reStructuredText output file tha describes
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
        Takes a Module object and formats the data into LaTeX
        syntax. This requires the \Describe macros provided in dtasheet.sty.
        """
        self.string += "\subsection{%s Ports List}\n\n" % (module.name)
        for port in module.ports:
            name = port.name
            if(port.range is None):
                range = ""
            else:
                range = "%s," % port.range

            if(port.meta is not None):
                meta = "[%s]" % port.meta
            else:
                meta = ""
            self.string += "\Describe{Option}{%s}{%s%s,%s}%s\n" % (name, range, port.direction, port.type, meta)
            self.string += "".join("%s\n" % x for x in port.comments)
            self.string += "\n\n"
            # Add escape characters before underscores
        self.string = re.sub(r'_','\_',self.string)
