#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from optparse import OptionParser
import sys
import logging
import PortExtractor
import RstGen
import TxtGen
import TeXGen

__author__        = "Tim Weaver"
__copyright__     = "Copyright: (c) 2010 RTLCores"
__creation_date__ = "Thu Sep 30 08:08:56 PDT 2010"
__version__       = 'v0.1.0'


if __name__ == '__main__':
#==============================================================================
# Define logging levels for the command line
#==============================================================================
    LEVELS = {  'debug'    : logging.DEBUG,
                'info'     : logging.INFO,
                'warning'  : logging.WARNING,
                'error'    : logging.ERROR,
                'critical' : logging.CRITICAL,
            }

#==============================================================================
# Option Parser
#==============================================================================
    parser = OptionParser(usage="%prog <options> [filename]", version="%s\n%s" % (__copyright__, __version__))
    parser.add_option("-d", "--debug",
                        dest="debug",
                        default='error',
                        help="Run in special debug mode. Valid options are debug, info, warning, error, critical")
    parser.add_option("-l", "--long_messages",
                        default=False,
                        action='store_true',
                        dest="long_messages",
                        help="Print out extra help messages on warnings and errors")

    (options, args) = parser.parse_args()

    if(len(args) == 1):
        filename = args[0]
    else:
        parser.print_help()
        sys.exit(1)

#==============================================================================
# Turn on logging
#==============================================================================
    logging.basicConfig()
    logging.getLogger().setLevel(LEVELS[options.debug])


#==============================================================================
# Do stuff here
#==============================================================================
    rst = RstGen.RstGen()
    txt = TxtGen.TxtGen()
    tex = TeXGen.TeXGen()

    pe = PortExtractor.PortExtractor()
    pe.parseFile(filename)
    num_modules = len(pe.modules)
    if(num_modules > 1):
        sys.stderr.write("Found %d modules\n" % num_modules)
    elif(num_modules == 1):
        sys.stderr.write("Found %d module\n" % num_modules)
    else:
        sys.stderr.write("Found no modules\n")
    for i in pe.modules:
        sys.stderr.write("    %s\n" % i.name)

    for module in pe.modules:
        tex.format(module)
        tex.write()

