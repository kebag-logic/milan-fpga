`ifndef ethernet_events_svh

`define ethernet_events_svh

//! RMON lane map ABI: STAT lane n reads at CSR 0x210 + 4*n (milan_csr
//! A_STATS_BASE = 0x210, stride 4). This enum is the single source of truth;
//! docs/reference/REGISTER_MAP.md mirrors it row for row.
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
