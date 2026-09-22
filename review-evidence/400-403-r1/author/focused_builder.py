import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "sw/builder"))
import test_builder as t
from test_declarations import test_declaration_contracts
for fn in (test_declaration_contracts, t.test_lwsrp_reset_words_match_rtl,
           t.test_lwsrp_class_constants_match_rtl, t.test_lwsrp_tspec_and_params,
           t.test_lwsrp_rejects, t.test_csr_defaults_header_consumed,
           t.test_optional_block_gates_bite, t.test_optional_block_prune_accounting,
           t.test_boot_policy_follows_the_declaration):
    print(fn.__name__, flush=True)
    fn()
