#!/usr/bin/env python3
"""Plant: remove the transmit hold from MAAP, AAF and CRF only (processor hold and stamp kept)."""
import sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_text()
edits = [
 ("  assign maap_tx_tvalid    = maap_txs_tvalid_w & tx_sa_ok_w;", "  assign maap_tx_tvalid    = maap_txs_tvalid_w;"),
 ("  assign maap_txs_tready_w = maap_tx_tready    & tx_sa_ok_w;", "  assign maap_txs_tready_w = maap_tx_tready;"),
 ("  assign aaf_tx_tvalid     = aaf_txs_tvalid_w  & tx_sa_ok_w;", "  assign aaf_tx_tvalid     = aaf_txs_tvalid_w;"),
 ("  assign aaf_txs_tready_w  = aaf_tx_tready     & tx_sa_ok_w;", "  assign aaf_txs_tready_w  = aaf_tx_tready;"),
 ("  assign crft_tx_tvalid    = crft_txs_tvalid_w & tx_sa_ok_w;", "  assign crft_tx_tvalid    = crft_txs_tvalid_w;"),
 ("  assign crft_txs_tready_w = crft_tx_tready    & tx_sa_ok_w;", "  assign crft_txs_tready_w = crft_tx_tready;"),
]
for a, b in edits:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
p.write_text(t)
print("planted", len(edits), "edits")
