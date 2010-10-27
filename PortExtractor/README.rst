Copyright (c) RTLCores LLC. 2010

PortExtractor
=============

The PortExtractor reads in a Verilog file and extracts all of the port details
and generates reStructuredText output for documentation.

Modules should be formatted like the following:

::

    module uart_kern (
    // Top level UART Kernel module
    // All pins are blah blah blah
      input  wire           clk, // posedge active
                            // The main clock for the system. The
                            // valid frequency range is 25MHz to
                            // 250MHz
    
      input  reg            reset,  // asynch
                            // Core reset. Active high in all cases.
                            // More text that describes this port
                            // Even more text to describe what this port does
    
      input  wire  [7:0]    tx_data,
                            // Transmit data bus.
