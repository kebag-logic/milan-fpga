`ifndef ethernet_events_svh

`define ethernet_events_svh

typedef enum int {
  TX_ERROR_UNDERFLOW = 0,
  TX_FIFO_OVERFLOW,
  TX_FIFO_BAD_FRAME,
  TX_FIFO_GOOD_FRAME,
  RX_ERROR_BAD_FRAME,
  RX_ERROR_BAD_FCS,
  RX_FIFO_OVERFLOW,
  RX_FIFO_BAD_FRAME,
  RX_FIFO_GOOD_FRAME,
  _ETH_EVENT_COUNTER
} ethernet_events_t;

`endif //!ethernet_events_svh
