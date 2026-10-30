cp syn/ooc/pp_resource_baseline.json "$WORK/scratch_baseline.json"
python3 syn/ooc/pp_resource_gate.py record "$WORK/ax7101/gateware" --endpoint route-1x1 --shipping-selection \
  --baseline "$WORK/scratch_baseline.json" --write
