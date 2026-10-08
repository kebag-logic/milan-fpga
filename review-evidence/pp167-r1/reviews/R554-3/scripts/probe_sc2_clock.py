#!/usr/bin/env python3
"""R554-3 probe Q1: in a copy of tb/aecp_notify/sim_main.cpp, log the clock of every
availability cancellation in SC2 relative to the coincidence clock (met_at), so the
09 section 8.4 phrase "presented in the deferred cancellation's clock" can be checked.
usage: probe_sc2_clock.py <copy of tb/aecp_notify/sim_main.cpp>"""
import sys
p = sys.argv[1]
s = open(p).read()
old = """      if (d->ca_cancel_valid_o) {
        if (d->ca_cancel_owner_o < N_CTRL) ++cancels[d->ca_cancel_owner_o];
        else exact = false;
      }
      if (d->uns_valid_o && d->uns_kind_o == KIND_DEREG"""
new = """      if (d->ca_cancel_valid_o) {
        printf("  [probe] SC2 expired %u: cancel owner %u at clock met%+d, failure presented %d\\n",
               expired, (unsigned)d->ca_cancel_owner_o, c - met_at, (int)d->ca_fail_valid_i);
        if (d->ca_cancel_owner_o < N_CTRL) ++cancels[d->ca_cancel_owner_o];
        else exact = false;
      }
      if (d->uns_valid_o && d->uns_kind_o == KIND_DEREG"""
assert s.count(old) == 1, "anchor not unique"
open(p, "w").write(s.replace(old, new))
