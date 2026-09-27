R348-2 packet for issue #397 / PR #588 at ff75a70807c151517860c73a06d7ea36e2a46008.
REPORT.md is the verdict. scripts/ are the reviewer's portable scripts (scripts/round1/
holds the unchanged round-1 probe and mutation scripts; compile_probe_j1.py differs from
compile_probe.py only in -j 1). receipts/ are raw outputs. Build trees, native logs and
probe side files stayed in an unpublished scratch area; receipts/raw-logs-sha256.txt and
receipts/probe-raw-sha256.txt list their digests.
Reproduce: export or clone the exact head; set LITEX_VENV and RV32_SDK (scripts/env.sh);
scripts/build_shape.sh <repo> <scratch> <shape>; scripts/run_plan.sh <repo> <scratch> <1x1|8x8> <plan>;
scripts/compare_run.py <run.json> <published.json>; scripts/check_tables_r2.py <repo> <receipt-dir>;
scripts/liveness_check.py <receipts...>; scripts/strip_compare.py <round2.log> <round1.json>;
scripts/round1/mutate_grader.py <export> <out.json> (legacy receipt paths supplied from the
round-2 'all' receipts); scripts/mutate_grader_r2.py <export> <out.json>;
scripts/round1/compile_probe_j1.py <repo> <build> <mdir>; scripts/probe_one.sh ...;
scripts/round1/analyze_probe.py <log> <probe> <aem_bytes>.
