//------------------------------------------------------------------------------
// File       : parameters.svh
// Description: Global parameter definitions for AXI-Stream and Ethernet logic
//------------------------------------------------------------------------------

`ifndef PARAMETERS_SVH
`define PARAMETERS_SVH

//! AXI-Stream interface width
`define AXIS_DATA_WIDTH  64
`define AXIS_TDEST_WIDTH 2

//! Ethernet constants
`define ETH_FIFO_DEPTH 64

//! Other global settings
`define USE_BIG_ENDIAN 1

`endif
