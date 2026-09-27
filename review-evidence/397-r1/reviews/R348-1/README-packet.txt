R348-1 packet for issue #397 / PR #588 at 7f997b60d5a74d46beca5c263d27496ccce0ae4f.
REPORT.md is the verdict. scripts/ are the reviewer's portable probe scripts;
receipts/ are raw outputs. Large probe side files and build trees stayed in an
unpublished scratch area; receipts/raw-logs-sha256.txt lists their digests.
Reproduce: export a tree of the exact head; set LITEX_VENV and RV32_SDK;
scripts/faithful.sh <repo> <scratch>; scripts/compile_probe.py <repo> <build> <mdir>;
scripts/probe_runs.sh <scratch>; scripts/analyze_probe.py <log> <probe> <aem_bytes>;
scripts/compare_receipt.py <repo> 1X1|8X8 <log>; scripts/check_tables.py <repo>;
scripts/mutate_grader.py <export> <out.json>.
