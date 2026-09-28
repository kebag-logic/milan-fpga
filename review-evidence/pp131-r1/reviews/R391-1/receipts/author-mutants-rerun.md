[
 {
  "mutant": "golden-acmp_nvm",
  "build_rc": 0,
  "run_rc": 0,
  "completed": true,
  "failing_checks": [],
  "missing_expected": [],
  "verdict": "PASS",
  "log": "scratch/authmut/golden-acmp_nvm.log"
 },
 {
  "mutant": "golden-pp_top",
  "build_rc": 0,
  "run_rc": 0,
  "completed": true,
  "failing_checks": [],
  "missing_expected": [],
  "verdict": "PASS",
  "log": "scratch/authmut/golden-pp_top.log"
 },
 {
  "mutant": "fourth_attempt_binding",
  "build_rc": 0,
  "run_rc": 2,
  "completed": true,
  "failing_checks": [
   "E8 DR2c count: three attempts in all (4 started, 4 failed)",
   "E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more after the failed attempt's error (642, 642)",
   "E10 DR2c count: no fourth attempt (4)"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/fourth_attempt_binding.log"
 },
 {
  "mutant": "alarm_forgiven_binding",
  "build_rc": 0,
  "run_rc": 2,
  "completed": true,
  "failing_checks": [
   "E11 DR2c revocation: a later successful commit and time leave the alarm set"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/alarm_forgiven_binding.log"
 },
 {
  "mutant": "no_backoff_binding",
  "build_rc": 0,
  "run_rc": 2,
  "completed": true,
  "failing_checks": [
   "E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more after the failed attempt's error (43, 43)"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/no_backoff_binding.log"
 },
 {
  "mutant": "alarm_forgiven_by_success",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3S10 revocation: a later successful write leaves the alarm set"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/alarm_forgiven_by_success.log"
 },
 {
  "mutant": "fourth_attempt",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3S10 count: 4 failed attempts of 0x50 (4 grants), alarm 1, unflushed 0",
   "D3S10 timing: each retry granted RETRY_BACKOFF_CYC_P cycles or more after the failed attempt's error (50014, 50014)",
   "D3S10 count: no fourth attempt (4)"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/fourth_attempt.log"
 },
 {
  "mutant": "no_backoff_d3",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3S10 timing: each retry granted RETRY_BACKOFF_CYC_P cycles or more after the failed attempt's error (15, 15)"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/no_backoff_d3.log"
 },
 {
  "mutant": "hold_released_at_go",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3O1: released at 122, terminal at 880, own fell at 123, the held command taken at 124, 0 busy cycles while owned",
   "D3O2: CLOSED at 164 after the release at 122, cause 7, own 0, 1 descriptor requests",
   "D3O2: CLOSED holds AECP (29998 busy cycles, the command still queued) and leaves the listener released",
   "D3S1: no record outside the nine rows set (36 ops)",
   "D3S4 taint: 2 WRITEs of 0x50, the first carrying the latched value, the last the change made during it",
   "D3S5 premise: the change accepted at 368271, the WRITE's done at 369209",
   "D3S6 group: 0x51 changed during 0x50's WRITE is written after it (1 WRITEs of 0x51)",
   "D3S7: IDENTIFY set, 0 pending cycles, 54 NVM operations",
   "D3R12: the re-walk cannot prove the image: CLOSED 9425, cause 2, the entity held"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/hold_released_at_go.log"
 },
 {
  "mutant": "store_not_rolled_back",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3R10 5000: done -1 closed 6003 cause 6 rolled back 0; the stores in reset from 5077 to 5999, the debt owed 921 cycles of it, fell at 5998",
   "D3R10 16000: done -1 closed 17003 cause 6 rolled back 0; the stores in reset from 5077 to 16999, the debt owed 11921 cycles of it, fell at 16998"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/store_not_rolled_back.log"
 },
 {
  "mutant": "enable_not_released_by_restore",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3R1: the enable requested from reset reaches ADP only at the combined terminal (1989 early enable cycles, 0 early done cycles)",
   "D3R12: the re-walk cannot prove the image: CLOSED 9425, cause 2, the entity held"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/enable_not_released_by_restore.log"
 },
 {
  "mutant": "rollback_ignores_debt",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3R10 5000: done 6537 closed -1 cause 6 rolled back 1; the stores in reset from 5077 to 5079, the debt owed 2 cycles of it, fell at 5998",
   "D3R10 16000: done -1 closed 13277 cause 6 rolled back 0; the stores in reset from 5077 to 5079, the debt owed 2 cycles of it, fell at -1"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/rollback_ignores_debt.log"
 },
 {
  "mutant": "identify_is_a_change",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3S7: IDENTIFY set, 49787 pending cycles, 2 NVM operations"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/identify_is_a_change.log"
 },
 {
  "mutant": "quarantine_released_by_time",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3R5: once the device ends the drained read a later SET persists"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/quarantine_released_by_time.log"
 },
 {
  "mutant": "restore_writes_are_changes",
  "build_rc": 0,
  "run_rc": 1,
  "completed": true,
  "failing_checks": [
   "D3R1: no restore write is a change (50163 pending cycles, 12 device writes)"
  ],
  "missing_expected": [],
  "verdict": "KILLED",
  "log": "scratch/authmut/restore_writes_are_changes.log"
 }
]
