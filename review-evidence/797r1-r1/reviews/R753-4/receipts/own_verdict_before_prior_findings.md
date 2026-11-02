[R753] SKELETON - draft verdict and ledger written before reading prior-round reports
Draft verdict: NEGATIVE - exact head 79fdea05ef54e2c99a0aa6efeadaa0f509076e92
F1 MINOR (Conformance, Robustness, Tests, Docs): srp_fresh_r clause "the SRP table answered a poll since the last STRM_SEL/STRMW_CTRL write" is weaker than the RTL (an answered provisioning write after a later poll, and a stolen beat, both clear it); probe receipts/probe_srp_poll_clause.log. The sweep's srppoll reads "latest answer is a poll", not the printed words.
Ledger draft: Conformance UNCLEAN, RTL CLEAN, Robustness UNCLEAN, Tests UNCLEAN, Docs UNCLEAN.
