[A160] Interpretation of receipts

Each run.py receipt records the exact subprocess argv, exit status, commit,
HEAD tree, staged tree where available, worktree status and diff SHA256.
The paired .log retains unfiltered stdout/stderr. Final clean-head receipts
start with final-. The head-* receipts measure the preceding implementation
commit, whose hash is retained in each receipt. Earlier development runs identify their actual dirty state;
they are not retroactively attributed to the final head.

The SDK installer selftest uses a tiny synthetic archive with a replaced test
digest. It executes real tar, relocation and compiler-identification fixture
programs. These are installer controls, not Bootlin measurements.

No archive with the selected production digest completed acquisition in this
session. acquisition-status.json and sdk-fresh-online.json record the blocker.
The last direct installer attempt reached its 180-second external timeout
(exit 124) while downloading, before extraction. No actual compiler realpath,
version, relocation or compiler-backed gate receipt can honestly be supplied.
The selected expected release/version/hash come from the public settled
contract, not a new measurement by this author. Public A10 readiness evidence
is prior compatibility evidence and is not relabeled as this author's result.

The deliberately absent control uses actual host compiler --version and RV32
probes only. All cross candidates raise FileNotFoundError through the test
seam. The full firmware gate then grades every retained text rule, explicitly
registering its compiler instruments as NOT RUN. Its audit is exact argv,
actual return status, and a named marker for deliberately hidden candidates.
No host compiler was used to compile firmware.

Expected negative control: absent-required-refusal exits 1 with the exact
--require-rv32 requirement. head-selector also proves an answering alternate
RV32 candidate cannot satisfy the provisioned absolute selector requirement.
Installer negatives name digest, provenance, inventory, relocation or tool
identity causes; tests fail if a mutation is accepted or refused differently.

Development corrections retained in receipts:
- ci-events-selftest initially found 10 stale expected count/position pins
  after adding workflow steps. Those controls were updated to the new exact
  step sequence, without dropping arms. Subsequent and final selftests pass.
- selftest-final combined mutually exclusive --check and --selftest flags and
  exited 2 at argparse; it was a command error, not a gate verdict. They were
  then run separately, including the final head-workflow-* receipts.
- Concurrent early receipt snapshots contended on git write-tree's index lock;
  their gate subprocesses never started. run.py now serializes that snapshot
  through a management-directory lock and uses git --no-optional-locks so
  read-only status calls cannot refresh the index concurrently. The affected checks were rerun.
- The initial hash check of a still-growing download refused the partial file.
  No extraction or execution followed that refusal.

No hosted/act, full builder, native bank, candidate, review or merge verdict is
implied by these focused results. A10 retains those responsibilities.

Further development corrections:
- baremetal-scope first found 11 real retired-term findings on host SDK
  metadata. This was published on #504 before adding narrow file-pinned masks
  under #259's explicit host-tooling non-goal. No product term or budget was
  broadened. The final 365-arm selftest includes 23 new positive/negative arms.
- sdk-scope-selftest initially expected class P for two product-document
  payloads containing only buildroot. They correctly refused through class T;
  class P is specific to linux substrings. The expected class was corrected
  without changing the refusal. sdk-scope-selftest-fixed and final tests pass.
- sdk-python-after-scope used a nonexistent check_python_idiom.py name, then
  sdk-python-after-scope-fixed passed an unsupported --check option to the
  correct check_py_idiom.py. Both exited 2 without running the gate. The exact
  supported command, python3 scripts/check_py_idiom.py, then passed in
  sdk-python-after-scope-checked on the final source.
- A later pair of snapshot attempts still raced optional git status index
  refreshes before the --no-optional-locks correction. No gate executed in
  those failed wrappers. Their intended scope/docs commands were rerun and
  passed with receipts after the correction.
