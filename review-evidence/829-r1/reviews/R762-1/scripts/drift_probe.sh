#!/bin/bash
# Tamper one tracked file at a time in the review clone, run the artifact check at
# both levels, restore it. usage: drift_probe.sh <clone> <pinned python>
cd "$1" || exit 2; PY=$2
G=tb/verilator/gptp_txts/generated
check() { # label file
  p=$("$PY" sw/litex/gen_mac_tx_model.py --check >/tmp/r762_p.$$ 2>&1; echo $?)
  q=$(python3 -B sw/litex/gen_mac_tx_model.py --check >/tmp/r762_q.$$ 2>&1; echo $?)
  echo "$1: pinned_rc=$p plain_rc=$q :: $(grep -m1 -E 'STALE|stale|re-converting' /tmp/r762_p.$$ | cut -c1-110)"
  git checkout -q -- "$2"; rm -f /tmp/r762_p.$$ /tmp/r762_q.$$
}
echo "clean: pinned=$("$PY" sw/litex/gen_mac_tx_model.py --check >/dev/null 2>&1; echo $?) plain=$(python3 -B sw/litex/gen_mac_tx_model.py --check >/dev/null 2>&1; echo $?)"
sed -i '0,/assign phy_sink_ready/s//assign  phy_sink_ready/' $G/mac_tx_chain_mii.v; check "hand edit of mac_tx_chain_mii.v" $G/mac_tx_chain_mii.v
sed -i 's/"tx_sf_param_depth": 8/"tx_sf_param_depth": 9/' $G/manifest_mii.json; check "manifest_mii.json edited" $G/manifest_mii.json
sed -i 's/phy_rst = (self.eth_phy_rst if self.shape == "mii"/phy_rst = (self.eth_phy_rst | self.eth_rst if self.shape == "mii"/' sw/litex/gen_mac_tx_model.py; check "generator's MII reset changed" sw/litex/gen_mac_tx_model.py
sed -i 's/# RTL, not glue: the record/# RTL, not  glue: the record/' sw/litex/milan_soc.py; check "product region touched" sw/litex/milan_soc.py
rm -f $G/manifest_mii.json; check "manifest_mii.json removed" $G/manifest_mii.json
git status --short | wc -l
