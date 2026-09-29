# [A440] Bench lane B2 handoff

Refs #606, #608, #75. Assignment: https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885087413
Branch: b2-bench-0929 from dev 13eda870d1a6cf3f946fc228a98862366b08d102 (lane worktree, physical /data path).
Packet: this directory. Large raw captures stay under /tmp/b2-a440/raw and are indexed by size and SHA-256.

## State

REVIEW READY posted 2026-09-29T07:34:43Z: https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885779526
(REVIEW-READY.md is the posted text; REVIEW-READY.readback.md the API readback, identical but for one trailing newline).

Commit `c37f1d04e39be0344dfde77e793cdfa441bd4869` on b2-bench-0929: one commit on 13eda870, one-line subject, no body, no trailers; local only, not pushed; worktree clean.
Bench work finished 07:21Z; everything restored and proven; bench lock free (non-blocking flock rc 0); no child process.
No DUT flash, reset, reboot or power cycle; no outlet switched; no PHY or CSR write; no wiring or instrument change.

Changed files (docs only):
- docs/findings/606_FIRST_BIND_MEASUREMENT.md (#606 item 3)
- docs/findings/608_75_WITHDRAWAL_AND_RESTART.md (#608 item 3, #75 acceptance)

## Verdicts (operator measurements, not review verdicts)

| Item | Verdict |
|---|---|
| #606 item 3, first bind (1 s) | PASS 5/5, 0.059-0.229 s; first probe SUCCESS 5/5; bridge's first MRPDU is Listener Ready, no LeaveAll |
| #606 item 3, long-hold connect (1 s) | PASS 4/4 (binds 2-5 after 36.9-39.3 s unbound) |
| #608 item 3, stop within one PDU | Literal 100/100: NOT MET (99/100). Recorded reading (IN registrar): PASS 99/99. Cycle 22: own LeaveAll 1.390 ms before the bridge Lv, LV registrar, 1,005 PDUs through the hold. Needs a decision; the pages do not choose |
| #608 item 3, STREAM_STOP counts each stop | PASS 99/99 (cycle 22 +0/+0) |
| #608 non-stop holds | 1/100 (9e9954e9: 3/100) |
| #75 first valid PDU < 1 s | PASS 99/99 demonstrated restarts, 0.011239-0.139247 s, median 0.013195, p95 0.081912 |
| #75 no growth | PASS: slope -8.28e-5 s/cycle, 95% [-2.35e-4, +6.93e-5]; blocks flat; MSRP ~1.8-2.1 PDU/s |
| #75 >= 100 talker restarts | NOT MET, 99/100 |

## Step ledger

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | TAKEN on #606 | POSTED 06:47Z: https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885168213 | TAKEN.md, identity/taken-url.txt |
| 1 | Identity gate | PASS 06:49-06:50Z: VERSION 00020060; ROM acad92b9 (53,344 B), QSPI payload d84bce7b (seed eto; eppo bf44ccc9, asl 809fcffa), AEM 93742dd2; ENTITY 312 B at 0x110 and CONFIGURATION 106 B at 0x248 byte-exact; entity 020000fffe000001; grader 10/10; RST_EPOCH 1; MAC_STATUS 0x0d; start census: 18/18 stream states unbound, DUT clock source 0, peer configuration 1 at 48 kHz | identity/, restore/census-start.jsonl |
| 1b | Capture prerequisite | 06:51Z: tap had no capture interface; the three driver inputs (Makefile 98a10075, source 0e3130d8, header 3ab62ff3) matched B1's and #75's hashes, built in a temporary directory, module loaded; interface up. Built .ko 6d6a38e2 (build not bit-reproducible; B1's was 9a3e8d75) | capture/ |
| 1c | Baseline observe | 06:53-06:54Z: 16 s tap, one DUT LeaveAll, no DUT declaration of the target Talker Advertise (Mt only) | bind/baseline/ |
| 2 | #606 five fresh first binds | PASS 06:55-06:59Z: 5/5 fresh (>= 17.3 s tap pre-window with >= 1 DUT LeaveAll and zero target TA declarations); first probe SUCCESS 5/5; response to first valid PDU 0.059-0.229 s; bridge's first MRPDU is Listener Ready (New), no LeaveAll; fresh state reached by unbind + DAFRESH expiry + >= 26 s, no reset. Bind 5 left bound for step 3 | bind/, table below |
| 3 | #608/#75 100 cycles | DONE 07:00-07:19Z: 100/100 actions rc 0, one lock window each. 99 cycles stopped within one PDU of the bridge Listener Lv (START/STOP +1/+1 each) and restarted in < 1 s. Cycle 22 is a non-stop hold: the DUT's own MSRP LeaveAll crossed the tap 1.39 ms before the bridge's Lv (registrar LV, documented LV + rLv), 1,005 PDUs through the hold, START/STOP +0/+0, not a restart. No early stop | cycles/, table below |
| 4 | Restore and proof | PASS 07:19-07:21Z: pair unbound (stop within one PDU, DUT TA Lv +0.108 s, 10.1 s quiet); census 53/53 non-counter reads equal; AVB_INTERFACE counters unchanged (DUT LINK_UP/DOWN 12/11, GM_CHANGED 50); DUT output 1 START/STOP 11/11 -> 115/115 (5 binds, 4 unbinds, 99/99 cycles, 1 restore stop); final 16.9 s tap: no CRF; grader 10/10; RST_EPOCH 1; CRFT_CTRL 0x3; NVM status unchanged; controller scripts removed; capture script removed, module unloaded, build removed, capture host interfaces as found; outlets OUT1/OUT3 OFF, others ON (read at end only; never switched); lock free (non-blocking flock rc 0), no child | restore/ |
| 5 | Findings pages, gates, commit | PASS: two pages generated from the analyses (tools/b2_pages.py, tools/b2_assemble.py, templates in summary/); commit c37f1d04; all nine gates rc 0 at that head (gates/gates.txt) | gates/ |
| 6 | REVIEW READY on #606 | POSTED: https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885779526 | REVIEW-READY.md, REVIEW-READY.readback.md |

## #606 per-bind table

Seconds after the tapped `CONNECT_RX` response unless stated.

<!-- binds:start -->
| Bind | Fresh (pre-window s, DUT LeaveAll PDUs, target TA declarations) | First probe status | First DUT TA (s) | First bridge MRPDU (s) | Bridge Listener Ready (s) | First valid PDU (s) | Unbind after: bridge Lv / last PDU / DUT TA Lv (s) | Result |
|---|---|---|---|---|---|---|---|---|
| 1 | True (17.3, 2, 0) | 0 | 0.171413 | 0.227724 | 0.227724 | 0.228304 | 0.009225 / 0.008539 / 0.021 (SETTLED) | PASS |
| 2 | True (17.3, 1, 0) | 0 | 0.068868 | 0.125289 | 0.125289 | 0.126451 | 0.008669 / 0.007266 / 7.168 (SETTLED) | PASS |
| 3 | True (17.3, 1, 0) | 0 | 0.074340 | 0.129176 | 0.129176 | 0.130400 | 0.009364 / 0.007875 / 7.144 (SETTLED) | PASS |
| 4 | True (17.4, 1, 0) | 0 | 0.172822 | 0.227576 | 0.227576 | 0.229360 | 0.009182 / 0.008618 / 7.122 (SETTLED) | PASS |
| 5 | True (17.3, 2, 0) | 0 | 0.000337 | 0.057989 | 0.057989 | 0.059352 | - | PASS |
<!-- binds:end -->

## #608/#75 per-cycle table

Seconds on the tap clock. "Registrar at Lv" is IN unless a Listener-type LeaveAll preceded the bridge's `Lv` with no bridge re-declaration of the stream in between.

<!-- cycles:start -->
| Cycle | Bridge Lv after disconnect (s) | Registrar at Lv | Last PDU after Lv (s) | PDUs after Lv + 2 ms | Settled hold PDUs | START/STOP delta | TA declared in hold | Restart (s) | #608 stop | #75 restart |
|---|---|---|---|---|---|---|---|---|---|---|
| 001 | 0.008466 | UNDETERMINED | -0.000525 | 0 | 0 | 1/1 | no | 0.105876 | PASS | PASS |
| 002 | 0.009184 | UNDETERMINED | -0.001176 | 0 | 0 | 1/1 | yes | 0.014236 | PASS | PASS |
| 003 | 0.009582 | UNDETERMINED | -0.001385 | 0 | 0 | 1/1 | yes | 0.012014 | PASS | PASS |
| 004 | 0.009435 | UNDETERMINED | -0.000897 | 0 | 0 | 1/1 | no | 0.126519 | PASS | PASS |
| 005 | 0.009216 | IN | -0.000601 | 0 | 0 | 1/1 | yes | 0.013848 | PASS | PASS |
| 006 | 0.009562 | UNDETERMINED | -0.000763 | 0 | 0 | 1/1 | yes | 0.012657 | PASS | PASS |
| 007 | 0.008820 | UNDETERMINED | -0.001962 | 0 | 0 | 1/1 | yes | 0.012462 | PASS | PASS |
| 008 | 0.009189 | UNDETERMINED | -0.000137 | 0 | 0 | 1/1 | yes | 0.013260 | PASS | PASS |
| 009 | 0.009597 | UNDETERMINED | -0.000360 | 0 | 0 | 1/1 | yes | 0.013076 | PASS | PASS |
| 010 | 0.009612 | UNDETERMINED | -0.000183 | 0 | 0 | 1/1 | yes | 0.012888 | PASS | PASS |
| 011 | 0.009171 | IN | -0.001678 | 0 | 0 | 1/1 | yes | 0.013670 | PASS | PASS |
| 012 | 0.013235 | IN | -0.000553 | 0 | 0 | 1/1 | yes | 0.014413 | PASS | PASS |
| 013 | 0.008929 | UNDETERMINED | -0.000184 | 0 | 0 | 1/1 | yes | 0.012221 | PASS | PASS |
| 014 | 0.009328 | UNDETERMINED | -0.001399 | 0 | 0 | 1/1 | yes | 0.014034 | PASS | PASS |
| 015 | 0.008671 | UNDETERMINED | -0.000548 | 0 | 0 | 1/1 | yes | 0.011846 | PASS | PASS |
| 016 | 0.008856 | UNDETERMINED | -0.000669 | 0 | 0 | 1/1 | yes | 0.011662 | PASS | PASS |
| 017 | 0.026166 | UNDETERMINED | -0.000664 | 0 | 0 | 1/1 | yes | 0.013470 | PASS | PASS |
| 018 | 0.009703 | IN | -0.000138 | 0 | 0 | 1/1 | yes | 0.014279 | PASS | PASS |
| 019 | 0.009080 | IN | -0.001323 | 0 | 0 | 1/1 | yes | 0.013093 | PASS | PASS |
| 020 | 0.009355 | IN | -0.000537 | 0 | 0 | 1/1 | yes | 0.012903 | PASS | PASS |
| 021 | 0.008708 | IN | -0.000706 | 0 | 0 | 1/1 | yes | 0.013730 | PASS | PASS |
| 022 | 0.010791 | LV | 1.997430 | 998 | 755 | 0/0 | yes | 0.001547 | LV-WINDOW | NOT RESTART |
| 023 | 0.009307 | IN | -0.000048 | 0 | 0 | 1/1 | yes | 0.013361 | PASS | PASS |
| 024 | 0.009690 | UNDETERMINED | -0.000245 | 0 | 0 | 1/1 | yes | 0.013176 | PASS | PASS |
| 025 | 0.009062 | UNDETERMINED | -0.001425 | 0 | 0 | 1/1 | yes | 0.013987 | PASS | PASS |
| 026 | 0.009425 | IN | -0.001603 | 0 | 0 | 1/1 | yes | 0.013804 | PASS | PASS |
| 027 | 0.009251 | IN | -0.000357 | 0 | 0 | 1/1 | yes | 0.013016 | PASS | PASS |
| 028 | 0.009478 | IN | -0.000522 | 0 | 0 | 1/1 | yes | 0.012834 | PASS | PASS |
| 029 | 0.009428 | UNDETERMINED | -0.001276 | 0 | 0 | 1/1 | yes | 0.014128 | PASS | PASS |
| 030 | 0.008830 | UNDETERMINED | -0.000491 | 0 | 0 | 1/1 | yes | 0.011938 | PASS | PASS |
| 031 | 0.009656 | UNDETERMINED | -0.000255 | 0 | 0 | 1/1 | yes | 0.013640 | PASS | PASS |
| 032 | 0.009566 | UNDETERMINED | -0.001974 | 0 | 0 | 1/1 | yes | 0.013450 | PASS | PASS |
| 033 | 0.008950 | UNDETERMINED | -0.001169 | 0 | 0 | 1/1 | yes | 0.013227 | PASS | PASS |
| 034 | 0.009357 | UNDETERMINED | -0.000500 | 0 | 0 | 1/1 | yes | 0.013037 | PASS | PASS |
| 035 | 0.098486 | IN | -0.001450 | 0 | 0 | 1/1 | yes | 0.012844 | PASS | PASS |
| 036 | 0.009333 | IN | -0.000111 | 0 | 0 | 1/1 | yes | 0.012653 | PASS | PASS |
| 037 | 0.009327 | UNDETERMINED | -0.000034 | 0 | 0 | 1/1 | yes | 0.013394 | PASS | PASS |
| 038 | 0.008689 | UNDETERMINED | -0.000212 | 0 | 0 | 1/1 | yes | 0.012207 | PASS | PASS |
| 039 | 0.009069 | UNDETERMINED | -0.000402 | 0 | 0 | 1/1 | yes | 0.012027 | PASS | PASS |
| 040 | 0.009323 | IN | -0.000594 | 0 | 0 | 1/1 | yes | 0.012802 | PASS | PASS |
| 041 | 0.008713 | IN | -0.000794 | 0 | 0 | 1/1 | yes | 0.011607 | PASS | PASS |
| 042 | 0.009168 | IN | -0.001059 | 0 | 0 | 1/1 | yes | 0.013442 | PASS | PASS |
| 043 | 0.009451 | UNDETERMINED | -0.001271 | 0 | 0 | 1/1 | yes | 0.016165 | PASS | PASS |
| 044 | 0.008967 | IN | -0.000183 | 0 | 0 | 1/1 | no | 0.139247 | PASS | PASS |
| 045 | 0.008790 | IN | -0.000810 | 0 | 0 | 1/1 | yes | 0.013574 | PASS | PASS |
| 046 | 0.009342 | IN | -0.001173 | 0 | 0 | 1/1 | yes | 0.014273 | PASS | PASS |
| 047 | 0.008519 | UNDETERMINED | -0.000292 | 0 | 0 | 1/1 | yes | 0.012084 | PASS | PASS |
| 048 | 0.010018 | UNDETERMINED | -0.001598 | 0 | 0 | 1/1 | yes | 0.013863 | PASS | PASS |
| 049 | 0.009335 | UNDETERMINED | -0.001852 | 0 | 0 | 1/1 | yes | 0.013587 | PASS | PASS |
| 050 | 0.010345 | IN | -0.001669 | 0 | 0 | 1/1 | yes | 0.012280 | PASS | PASS |
| 051 | 0.009191 | UNDETERMINED | -0.001329 | 0 | 0 | 1/1 | yes | 0.013069 | PASS | PASS |
| 052 | 0.009676 | UNDETERMINED | -0.001621 | 0 | 0 | 1/1 | yes | 0.011782 | PASS | PASS |
| 053 | 0.008948 | UNDETERMINED | -0.000825 | 0 | 0 | 1/1 | yes | 0.013597 | PASS | PASS |
| 054 | 0.011162 | UNDETERMINED | -0.000838 | 0 | 0 | 1/1 | yes | 0.014363 | PASS | PASS |
| 055 | 0.009709 | IN | -0.000338 | 0 | 0 | 1/1 | yes | 0.013110 | PASS | PASS |
| 056 | 0.009082 | IN | -0.000522 | 0 | 0 | 1/1 | yes | 0.081912 | PASS | PASS |
| 057 | 0.009568 | IN | -0.001814 | 0 | 0 | 1/1 | yes | 0.013605 | PASS | PASS |
| 058 | 0.008813 | UNDETERMINED | -0.000998 | 0 | 0 | 1/1 | yes | 0.011382 | PASS | PASS |
| 059 | 0.009083 | UNDETERMINED | -0.000205 | 0 | 0 | 1/1 | yes | 0.013195 | PASS | PASS |
| 060 | 0.085791 | IN | -0.001849 | 0 | 0 | 1/1 | yes | 0.013936 | PASS | PASS |
| 061 | 0.009797 | IN | -0.001789 | 0 | 0 | 1/1 | yes | 0.011733 | PASS | PASS |
| 062 | 0.009195 | UNDETERMINED | 0.000001 | 0 | 0 | 1/1 | yes | 0.013428 | PASS | PASS |
| 063 | 0.009404 | UNDETERMINED | -0.000147 | 0 | 0 | 1/1 | yes | 0.015254 | PASS | PASS |
| 064 | 0.009701 | UNDETERMINED | -0.001375 | 0 | 0 | 1/1 | yes | 0.012037 | PASS | PASS |
| 065 | 0.009125 | UNDETERMINED | -0.000613 | 0 | 0 | 1/1 | yes | 0.011839 | PASS | PASS |
| 066 | 0.009334 | UNDETERMINED | -0.000763 | 0 | 0 | 1/1 | yes | 0.012665 | PASS | PASS |
| 067 | 0.008673 | UNDETERMINED | -0.000030 | 0 | 0 | 1/1 | yes | 0.012370 | PASS | PASS |
| 068 | 0.009701 | IN | -0.000870 | 0 | 0 | 1/1 | yes | 0.012187 | PASS | PASS |
| 069 | 0.009301 | IN | -0.001410 | 0 | 0 | 1/1 | yes | 0.014001 | PASS | PASS |
| 070 | 0.008739 | UNDETERMINED | -0.000652 | 0 | 0 | 1/1 | yes | 0.011782 | PASS | PASS |
| 071 | 0.009255 | UNDETERMINED | -0.000109 | 0 | 0 | 1/1 | yes | 0.013502 | PASS | PASS |
| 072 | 0.009444 | UNDETERMINED | -0.000106 | 0 | 0 | 1/1 | yes | 0.013312 | PASS | PASS |
| 073 | 0.047490 | IN | -0.001082 | 0 | 0 | 1/1 | yes | 0.014509 | PASS | PASS |
| 074 | 0.009539 | IN | -0.001068 | 0 | 0 | 1/1 | yes | 0.012334 | PASS | PASS |
| 075 | 0.008913 | UNDETERMINED | -0.001253 | 0 | 0 | 1/1 | yes | 0.015142 | PASS | PASS |
| 076 | 0.009172 | UNDETERMINED | -0.001449 | 0 | 0 | 1/1 | yes | 0.012948 | PASS | PASS |
| 077 | 0.009661 | IN | -0.000873 | 0 | 0 | 1/1 | yes | 0.012757 | PASS | PASS |
| 078 | 0.008820 | IN | -0.000844 | 0 | 0 | 1/1 | yes | 0.015567 | PASS | PASS |
| 079 | 0.009175 | UNDETERMINED | -0.000137 | 0 | 0 | 1/1 | yes | 0.013266 | PASS | PASS |
| 080 | 0.009483 | UNDETERMINED | -0.000377 | 0 | 0 | 1/1 | yes | 0.013048 | PASS | PASS |
| 081 | 0.008858 | UNDETERMINED | -0.000565 | 0 | 0 | 1/1 | yes | 0.011778 | PASS | PASS |
| 082 | 0.009700 | UNDETERMINED | -0.001338 | 0 | 0 | 1/1 | yes | 0.012085 | PASS | PASS |
| 083 | 0.009205 | IN | -0.001656 | 0 | 0 | 1/1 | yes | 0.013783 | PASS | PASS |
| 084 | 0.008795 | UNDETERMINED | -0.001068 | 0 | 0 | 1/1 | yes | 0.013326 | PASS | PASS |
| 085 | 0.009089 | UNDETERMINED | -0.000301 | 0 | 0 | 1/1 | yes | 0.012139 | PASS | PASS |
| 086 | 0.009296 | IN | -0.000450 | 0 | 0 | 1/1 | yes | 0.012952 | PASS | PASS |
| 087 | 0.008618 | IN | -0.001577 | 0 | 0 | 1/1 | yes | 0.012761 | PASS | PASS |
| 088 | 0.008830 | IN | -0.001852 | 0 | 0 | 1/1 | yes | 0.013567 | PASS | PASS |
| 089 | 0.009413 | IN | -0.001121 | 0 | 0 | 1/1 | yes | 0.014272 | PASS | PASS |
| 090 | 0.009698 | UNDETERMINED | -0.001340 | 0 | 0 | 1/1 | yes | 0.012087 | PASS | PASS |
| 091 | 0.009120 | IN | -0.000573 | 0 | 0 | 1/1 | yes | 0.011862 | PASS | PASS |
| 092 | 0.010473 | IN | -0.000864 | 0 | 0 | 1/1 | yes | 0.013592 | PASS | PASS |
| 093 | 0.008951 | IN | -0.001150 | 0 | 0 | 1/1 | yes | 0.101353 | PASS | PASS |
| 094 | 0.009105 | UNDETERMINED | -0.001243 | 0 | 0 | 1/1 | yes | 0.013109 | PASS | PASS |
| 095 | 0.008945 | UNDETERMINED | -0.001008 | 0 | 0 | 1/1 | yes | 0.013400 | PASS | PASS |
| 096 | 0.009328 | UNDETERMINED | -0.001204 | 0 | 0 | 1/1 | yes | 0.014195 | PASS | PASS |
| 097 | 0.008826 | IN | -0.000515 | 0 | 0 | 1/1 | yes | 0.011917 | PASS | PASS |
| 098 | 0.008930 | IN | -0.001679 | 0 | 0 | 1/1 | yes | 0.012731 | PASS | PASS |
| 099 | 0.009393 | IN | -0.000954 | 0 | 0 | 1/1 | yes | 0.014426 | PASS | PASS |
| 100 | 0.008779 | UNDETERMINED | -0.001149 | 0 | 0 | 1/1 | yes | 0.011239 | PASS | PASS |
<!-- cycles:end -->

## Gates at c37f1d04 (all rc 0, foreground, not piped, physical /data worktree; gates/gates.txt)

1. md-venv python scripts/docs_check.py: 0 findings, 176 md + 938 scrubbed
2. md-venv python scripts/check_doc_style.py: OK (22 current documents)
3. md-venv python scripts/gen_toc.py --check: OK (118 pages)
4. md-venv python scripts/check_em_dash.py --base 13eda870: 0 findings over 802 added lines in 2 pages
5. md-venv python scripts/check_doc_paths.py: OK (854 paths)
6. python3 scripts/ci_scope.py --selftest: PASS
7. python3 scripts/check_baremetal_only.py --check: OK, 0 findings (the script needs a mode; --check is the tree scan)
8. python3 scripts/check_feature_status.py --self-test: 46/46, 0 findings
9. git diff --check: clean; git diff --check 13eda870 HEAD: clean

## Deviations and incidents

- Outlets were read at the end only (07:20Z: OUT1 and OUT3 OFF, the others ON, identical to lane B1's recorded start and end). No outlet was switched in this lane; a start read was not taken.
- The baseline observe ran an earlier b2_action.py whose bind pre-window wait counted host time (15.0 s window); it was changed to tap time before bind 1. Every bind, unbind, cycle and restore ran the final revision.
- b2_analyze.py's registrar classification was refined after cycles 1-3 (IN had been assumed when no LeaveAll was in the capture; it now needs an observed declaration or the measured re-declaration bound). All 112 analyses were re-run with the final analyzer; the summary was byte-identical before and after the re-run.
- The tap again had no capture interface; the same three hash-identical driver inputs were rebuilt in a temporary directory on the capture host and removed at restore. The built module hash differs from B1's (the build is not bit-reproducible); inputs are identical.
- Interface, module and home-path strings were masked in the packet after acquisition (116 files: capture.txt records, identity-aecp.jsonl, capture and cleanup records). Raw captures are unmodified.
- NVM status read "pend=1 ... commits ok=2" at both the identity read and the final read (unchanged across the lane).

## Open questions for the manager

1. #608 item 3: which reading applies? Literal 100/100 is not met (cycle 22); the recorded reading (withdrawal reaching an IN registrar) is met 99/99. A stricter target for the genuine LeaveAll window would need its own requirement decision, as #608 recorded.
2. #75: the talker direction has 99 demonstrated restarts, one short of "at least 100". Additional cycles would need an assignment.
3. #606: the post-reset allocation path (the original cause) needs a DUT reset and is not exercised; the DUT's destinations were already held. Observation only: DUT Stream Output 0, never bound in this lane, held a MAAP destination, while on 9e9954e9 both outputs read all-zero at the #75 start census (consistent with processor PR 129's auto-acquisition).
4. The LV-window stop time (T-MRP-LEAVE, 4.5-7.5 s) is not observable with a 2 s hold; a longer-hold measurement would need an assignment.

## Packet layout

| Path | What |
|---|---|
| TAKEN.md, REVIEW-READY.md, REVIEW-READY.readback.md | posted texts and readback |
| PR-BODY.md | proposed PR body |
| identity/ | console CRC readback, grader, AECP descriptor comparison, expected CRCs, csr.csv, image hashes, lock windows |
| capture/ | temporary capture-driver preflight and load records (names masked) |
| bind/<action>/ | baseline, bind-1..5, unbind-1..4, unbind-restore, final: result.json, analysis.json, msrp.tsv, acmp.tsv, console and snapshot readbacks, controller transactions, capture.txt, raw-artifacts.json |
| cycles/cycle-NNN/ | the same per cycle, plus action.log |
| restore/ | censuses start/end and comparison, final console and grader, host cleanup, outlets, lock checks |
| summary/ | summary.json, generated page tables (page-*.md), page templates, review-ready URL |
| tools/ | every script used; ORIGIN-A386.sha256 and ORIGIN-B1.sha256 pin the reused tools as copied |
| gates/ | gate outputs and gates.txt |
| RAW-ARTIFACTS.json | all 112 raw captures (43,137,232 bytes) by relative path, size and SHA-256; kept under /tmp/b2-a440/raw on the build box |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
