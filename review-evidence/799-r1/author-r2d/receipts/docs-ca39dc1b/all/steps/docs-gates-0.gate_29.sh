python3 scripts/check_soc_sources.py
python3 scripts/check_soc_sources.py --selftest
command -v tclsh >/dev/null || {
  sudo apt-get update -qq
  sudo apt-get install -y --no-install-recommends tcl
}
python3 sw/litex/iob_pack_selftest.py
