# The head's suite, no defect, at further legal bounds beyond the Makefile's 100 and 37.
PROBES = {"base": []}
RUNS = [("base", m, t) for t in (20, 21, 64, 1000, 1001)
        for m in ("pristine", "coincident completion", "unsolicited completion", "lazy erase",
                  "short read", "silent")]
