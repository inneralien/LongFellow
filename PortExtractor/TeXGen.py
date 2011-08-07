import sys
import re

indent_re = re.compile("^\s+(?!$)")

class TeXGen():
    def __init__(self):
        self.string = ""

    def write(self, filename=None):
        """Writes formatted TeX output file tha describes
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
        syntax.  If the comments are indented more than 2 spaces they are
        considered
        verbatim sections:
        // This is a standard comment in the code
        // that can extend to multiple lines
        //      This will be verbose
        //      and so will this
        //      1'b0 = Even Parity
        """
#        self.string += "\subsection{%s}\n\n" % (module.name)
        verbatim = False
        for port in module.ports:
            name = port.name
            if(port.range is None):
                range = ""
            else:
                range = "%s" % port.range

            if(port.meta is not None):
                meta = "[%s]" % port.meta
            else:
                meta = ""
            # Add escape characters before underscores
#            describe_string = "\Describe{Option}{%s}{%s%s,%s}%s\n" % (name, range, port.direction, port.type, meta)
            describe_string = "\\begin{description}\n"
            describe_string += "    \item[%s]{\\tt %s}\hfill{\\tt %s %s}\\\\\n" % (name, range, port.direction, port.type)
            sub_describe_string = re.sub(r'_','\_',describe_string)
#            self.string += "\Describe{Option}{%s}{%s%s,%s}%s\n" % (name, range, port.direction, port.type, meta)
            self.string += sub_describe_string
            if(len(port.comments) != 0):
                for line in port.comments:
                    m = indent_re.match(line)
                    if((m is not None) and (verbatim == False)):
                        self.string += "\\begin{verbatim}[backgroundcolor=,frame=]\n"
                        verbatim = True
                    if((m is None) and (verbatim == True)):
                        self.string += "\\end{verbatim}\n"
                        verbatim = False
                    if(verbatim == True): # Don't substitute _ with \_
                        self.string += " %s\n" % line
                    else:
                        # Add escape characters before underscores
                        sub_line = re.sub(r'_','\_',line)
                        self.string += " %s\n" % sub_line
                if(verbatim == True):
                    self.string += "\\end{verbatim}\n"
                    verbatim = False
            self.string += "\end{description}"
            self.string += "\n\n"
            # Add escape characters before underscores
#        self.string = re.sub(r'_','\_',self.string)

    def format_old(self, module):
        """
        Takes a Module object and formats the data into LaTeX
        syntax. This requires the \Describe macros provided in dtasheet.sty.
        If the comments are indented more than 2 spaces they are considered
        verbatim sections:
        // This is a standard comment in the code
        // that can extend to multiple lines
        //      This will be verbose
        //      and so will this
        //      1'b0 = Even Parity
        """
#        self.string += "\subsection{%s}\n\n" % (module.name)
        verbatim = False
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
            # Add escape characters before underscores
            describe_string = "\Describe{Option}{%s}{%s%s,%s}%s\n" % (name, range, port.direction, port.type, meta)
            sub_describe_string = re.sub(r'_','\_',describe_string)
#            self.string += "\Describe{Option}{%s}{%s%s,%s}%s\n" % (name, range, port.direction, port.type, meta)
            self.string += sub_describe_string
            if(len(port.comments) != 0):
                for line in port.comments:
                    m = indent_re.match(line)
                    if((m is not None) and (verbatim == False)):
                        self.string += "\\begin{verbatim}[backgroundcolor=,frame=]\n"
                        verbatim = True
                    if((m is None) and (verbatim == True)):
                        self.string += "\\end{verbatim}\n"
                        verbatim = False
                    if(verbatim == True): # Don't substitute _ with \_
                        self.string += " %s\n" % line
                    else:
                        # Add escape characters before underscores
                        sub_line = re.sub(r'_','\_',line)
                        self.string += " %s\n" % sub_line
                if(verbatim == True):
                    self.string += "\\end{verbatim}\n"
                    verbatim = False
            self.string += "\n"
            self.string += "\\medskip\n"
            # Add escape characters before underscores
#        self.string = re.sub(r'_','\_',self.string)
