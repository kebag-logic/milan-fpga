# R437-3: is 20 the suite's floor? The head's suite with only its TMO >= 20
# static_assert removed, at bounds below 20, under pristine and coincident.
PROBES = {"no_floor_assert": [("SIM",
    'static_assert(TMO >= 20, "tb/nvm_port\'s waits are derived for MEM_TIMEOUT_CYC_P >= 20");',
    '')]}
RUNS = [("no_floor_assert", m, t) for t in (19, 15, 10, 5) for m in ("pristine", "coincident completion")]
