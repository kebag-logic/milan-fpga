`ifndef ethernet_events_svh

`define ethernet_events_svh

//! RMON lane map ABI: STAT lane n reads at CSR 0x210 + 4*n (milan_csr
//! A_STATS_BASE = 0x210, stride 4). This enum is the single source of truth;
//! docs/reference/REGISTER_MAP.md mirrors it row for row.
//!
//! It is ALSO the bit order of STATS_CAP (CSR 0x204), the per-lane capability
//! mask: bit n = 1 means lane n has a real event source in this build, 0 means
//! it is structurally silent. Read it before believing a zero count - a lane
//! with no source and a lane with nothing to report read identically otherwise,
//! which is how a fully tied-off counter group survived on two boards.
typedef enum int {
  TX_ERROR_UNDERFLOW = 0,  //! 0x210
  TX_FIFO_OVERFLOW,        //! 0x214
  TX_FIFO_BAD_FRAME,       //! 0x218
  TX_FIFO_GOOD_FRAME,      //! 0x21C (derived at the MAC AXIS boundary)
  RX_ERROR_BAD_FRAME,      //! 0x220
  RX_ERROR_BAD_FCS,        //! 0x224
  RX_FIFO_OVERFLOW,        //! 0x228
  RX_FIFO_BAD_FRAME,       //! 0x22C
  RX_FIFO_GOOD_FRAME,      //! 0x230 (derived at the MAC AXIS boundary)
  _ETH_EVENT_COUNTER
} ethernet_events_t;

`endif //!ethernet_events_svh
