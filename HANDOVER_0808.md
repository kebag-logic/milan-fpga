# HANDOVER 2026-08-08 — Milan AVB FPGA (AX7101)

LOCAL-ONLY. Never commit this file (docs charter: handovers stay untracked).
It names the peer device and bench hosts; the public repo must never do that
(say "certified peer"; the certification suite = "internal COMPLIANCE suite";
the A-word and the word CERT never appear in tracked text).

State at writing: tree at `32997f51` on `main-push` (VERSION 0x0030), t532
three-directive sweep running, traceability doc MERGED to main (2eeb0267), board still runs
t531-asl (0x002D era — 0x002E/2F/30 are NOT on silicon yet).

---

## 1. ROADMAP

### Product (tracked, bottom of README.md)
Five phases → v1.0 in Q1 2027. The README arrow is the authoritative copy;
keep it in sync when phases complete.

### Engineering — next rounds, in order
(items 2-4 are EXPANDED with full fix/TB/compliance designs in section 1b below)

1. **t532 flash + silicon verify** (sweep running now, watcher armed).
   Carries three unproven versions. Proof list:
   - 0x002E: Hive/GET_STREAM_INFO — disconnected input shows ONLY
     STREAM_FORMAT_VALID (0x80000000); disconnected output shows
     FORMAT+ACC_LAT (0xA0000000); no stream id/dest on idle CRF output.
   - 0x002F: fill target — servo report fill ≈ 16 samples, not 256.
     Latency ~167 microseconds input→cluster once locked.
   - 0x0030: (a) bind sink 0, stream, DISCONNECT_RX → LATE stays frozen,
     no 1-per-second unsolicited GET_COUNTERS, Hive quiet;
     (b) MEDIA_UNLOCKED increments on the unbind (Table 5.6
     LOCKED = UNLOCKED+1 restored); (c) the odmap discriminator below.
   - Post-flash discriminator (seeder hoist): read CSR 0x910 capture key0 =
     0x1300 after boot, 0x1400 after ADD_AUDIO_MAPPINGS {0,0,8,0}.
   - Flash rule: best-WNS directive wins; always flash+verify autonomously,
     then soak streams (standing orders).
2. **#33 ACMP listener conformance round** — from the 08-08 audit (24
   findings) + the adversarial traceability review. Confirmed defects, in
   priority order:
   - a1/a2: SRP params (dmac/vlan) not cleared on TMR_NO_TK expiry and on
     EVT_TK_UNREGISTERED (Milan 5.5.3.5.36/.48, 5.3.8.9).
   - a4: invented RSV_OK→NO_RSV branch arms a timer that nothing serves —
     permanent wedge if entered. Delete the branch.
   - a3: EVT_TK_REGISTERED fires on TalkerAdvertise only; Table 5.29 says
     TA **or** TalkerFailed.
   - b1: registrar match is stream-id-only; should qualify the source.
   - b2: BIND_RX step 1 locked-controller check absent (5.5.3.5.3).
   - b4/b5: PROBE_TX_RESPONSE match validates listener fields only; a
     talker retransmit is not deduplicated.
   - b3: tk_avail/adp_age survive an unbind.
   - b6: GET_RX_STATE echoes command stream_id/vlan in settled states
     instead of the record's authoritative values.
   - b7: TMR_NO_ADP is a fixed 63 seconds — ignores the received
     valid_time; no available_index-regression or gm/domain checks (5.6.4).
   - c3: FAST_CONNECT/STREAMING_WAIT/REGISTERING_FAILED flag laws in
     GET_RX_STATE payloads.
   - c4: responses echo old talker_unique_id / stream_dest_mac where Tables
     5.32/5.36 say zero.
3. **#35 adversarial-review round** — 12 refuter-confirmed divergences from
   the traceability review (docs/reference/PROTOCOL_TRACEABILITY.md,
   commit 2eeb0267; none overlaps #31-#34). The one HIGH first:
   - **SET_STREAM_FORMAT is accepted on a BOUND Stream Input** — no
     STREAM_IS_RUNNING refusal per Milan 5.4.2.7, so a mid-stream reformat
     flips the RX monitor into rejecting the live stream
     (KL_aecp_response_builder.sv:3291). This is the RTL half of
     guardrail 1: the fabric must refuse what the bench bans.
   - Medium: PROBE_TX_RESPONSE flag law inverted vs Table 5.43
     (KL_acmp_tlkr_ctx.sv:397); GET_TX_STATE forces REGISTERING_FAILED=0
     vs Table 5.47 (:421); 5.5.4.1 step-3 valid-DMAC check missing so
     TALKER_DEST_MAC_FAILED is unreachable (:394); channel-shrink
     SET_STREAM_FORMAT silently prunes mappings where 5.4.2.7 says
     BAD_ARGUMENTS (builder:3340); SET_STREAM_INFO rejects every
     STREAM_OUTPUT except 0 on 9-output shapes (builder:3504); no
     unsolicited notify on the 60 s auto-unlock, Table 5.22
     (KL_aecp_l0_state.sv:219).
   - Low: GET_TX_STATE/DISCONNECT_TX field-zeroing echoes (Tables
     5.47/5.45), invalid-uid ctx-0 cross-sink leak (Table 5.27),
     TMR_ADVERTISE around DELAY sends (5.6.3.5.9), ADP valid_time reset
     31 vs Milan 5.6.2's 10 (milan_csr.sv:1177).
   - 17 further candidates are carried as `suspect` in the doc tables —
     triage when the round opens.
4. **#34** — u=1 replay of a succeeded REMOVE_AUDIO_MAPPINGS answers
   BAD_ARGUMENTS; must be idempotent SUCCESS.
5. **#32 coverage residue** (standing test-growth directive): rxmon ctx case
   lock→bind_fall→UNLOCKED+1; dp nxn case bind k>0 → frames →
   DISCONNECT → tbl_en falls → exactly one UNLOCKED → pushes quiet;
   window-armed entry survives ACMP unbind and release-to-alias restores it.
6. **#28 completion** — setpoint is landed (0x002F); remaining: silicon
   latency measurement (tap TX capture vs I2S edge), then source-invariance
   proof across Internal/CRF/Stream clock sources. Wander to ±6 pairs needs:
7. **#22 software half** — PipeWire-style DLL on the board replacing the
   phc2sys-class chain; GM-change reaction must be fast (2-minute re-lock is
   unacceptable — user order). Rides the rootfs work.
8. **#7 rootfs** — persistence (priority1 248 baked, entity state), LiteSPI
   mtd decision, /dev/null fuse forever in mind (see learnings).
9. **#23 CRF observe** — bind sink 1 from the peer, watch the 8-PDU/16 ms
   settle, MMCM engage iff clk_src=CRF. CRF sink locks as a MONITOR even
   when not the recovery source (user roadmap).
10. **#15 ALSA capture driver deploy** (fixed at ca50bc2 in milan-tests-avb,
   compiles RV32) — awaits a live-test window on the board.
11. Campaign residue: honest churn leg (equal-format churn, post-0x0030),
    ep-library DUT-selection race, analog THD+N loop (blocked on the user
    routing the peer's internal loop), pw1 restart (user).
12. **Coverage build-out** (user asked 08-08): `coverage:` targets exist in
    only 2 suites. If a repo-wide line number is wanted, clone the
    avtp_rxmon pattern (obj_cov + verilator_coverage + cov_gate.py 95) into
    aecp, milan_dp, acmp, acmp_lstn, crossbar, lwsrp, tkdiag, pcm_playback,
    servo, csr, persist suites.


## 1b. CONFORMANCE ROADMAP — every traceability issue, grouped, with fixes
(Generated 2026-08-08 from docs/reference/PROTOCOL_TRACEABILITY.md 2eeb0267 by
12 analysis agents — one per package, 2 on the HIGH finding — each quoting the
governing clause from /home/alex/standards before proposing. Every item below
carries: the fix, the TB proof (including which existing checks pin today's
WRONG value and must flip), and the conformance-phase proof (behave + live
bench observable). Suspects were adversarially verified first: all confirmed
except D5-GET (refuted, read-only correctly exempt) and I1's three guessed
mechanisms (symptom real, root cause = the handshake-blind tap, task #36 / gh #65).

MASTER LANDING ORDER (per-package internal order inside each):
 1. B1+B2  ACMP listener round (#33) — one coordinated landing, same file;
           two VERSION stories max (B1a-c+e + B2 field-law = story 1;
           B1d registrar-match = follow-on story 2).
 2. D      AECP stream-command law (#35 core): story A = D1+D5+D3 gate
           vectors, story B = D2 shrink-refusal, story C = D6 (#34),
           story D = D4 lock push.
 3. A      ACMP talker response-field law (#35): A1+A5+A4 → A3 → A2.
 4. C      ADP: C2 valid_time reset → C1 timer restart (+C3/C4 memos).
 5. F      Push coverage/rate: F1 → F4 decision → F2 → F3.
 6. I1/I3  SRP quick wins (tap tready #36 lwsrp leg + rIn deletion).
 7. H      AVTP: H1 version gate → H2 mr plumbing → H3 Eq-14 rounding.
 8. G1     CRF counter widening (+G2 memo).
 9. E      Controller liveness (M-AECP-11) — the one absent feature, L.
10. J      gPTP: J2 INCR reset → J3 asCapable (paired flash) → J1 latency
           split (bench campaign) → J4 AS_PATH depth.
11. I5/I2/I4  SRP deep items (CBS wire-time, TA-declare gating, Domain
           adopt) — each wants its own bench window.
12. Memos to carry: C3 (partial-conform startup/link-up jitter), C4 (keep),
    G2 (keep coalesced FRX + sharpened defense), H5 (keep family-accept),
    I6 (keep, conform-lite = class-CBS enable after I5), B1e (keep
    declare-on-bound), H4 (stale doc closure, zero RTL).

VERSION budget estimate: roughly 8-10 minor bumps if landed as grouped above.
Rules that bind every landing: check the clause in /home/alex/standards before
coding; both boards same VERSION before bench; flash+verify+soak; all ten
A_STRMW_CNT twice; TB check-count only grows; one-line commits.

## PACKAGE B1 [gh #54] — ACMP listener SRP coupling (#33 a1-a4/b1; 2 VERSION stories)
Landing: (1) B1b+B1c together (same lines 896-899/954-987, one event-law
edit) → (2) B1a → (3) B1e docs ride along = ONE VERSION story (no interface
change). B1d = SEPARATE follow-on VERSION (ports+area). Keep sid-zeroing OUT
until #32's t531 silicon proof closes.

- B1b (S, DELETE): invented fail_rise branch RSV_OK→NO_RSV (981-983). Wedge
  mechanism PRECISE: destination serves only TMR_NO_TK but the branch lands
  with tmr=0 (RSV_OK entry zeroed it) and wheel decrement gates on tmr!=0 →
  disarmed forever; NO_RSV exits = reg_rise (needs fresh TA 0→1) or fire
  (needs armed tmr); entered when TF JoinIn services in an EARLIER sweep pass
  than the TA leave (real MSRPDU-ordering race). Recovery only UNBIND/full TA
  cycle. Table 5.30 marks every RSV_OK row except EVT_TK_UNREGISTERED "x".
  KEEP srv_fail_r service (w_srp_diff self-clear). TB [6]/[N7] PIN TODAY'S
  DEFECT — rewrite: TF-rise stays state 7; add wedge-regression case (TF rise,
  8 cycles, TA fall, 8 cycles, TF fall → PRB_W_* + probe_count advancing).
  Header note: deliberate divergence from the pipewire reference (REF-BUG
  pattern — reference wrong vs Table 5.30).
- B1c (S, same edit set): EVT_TK_REGISTERED = TA OR TF (Table 5.29 "either
  Talker Advertise or Talker Failed", once on Not-registered→Registered).
  Fix: attr_rise/attr_fall from combined (ta_registered|ta_failed) vs
  (srv_reg|srv_fail). Both levels ALREADY reach ctx ports (121-124; datapath
  g_acmpl_ta projects per sink). Today: TF-holding talker never promotes →
  NO_TK fires every 10 s → probe-churn forever. Companion IN SCOPE: settled
  w_resp_flags (478-481) gains REGISTERING_FAILED 0x0040 from
  ta_failed_i[cur_idx_r] (Table 5.39). TB: TF-alone settles RSV_OK, flags
  0x0048, NO probe for 12 s; live: deny class A on switch → Hive shows
  failed-registration, PROBE_TX storm disappears.
- B1a (S): settled exits skip "Clear the SRP parameters and stop SRP"
  (5.5.3.5.36/.48 step 1; 5.3.8.9 zeros law). NO_TK fire branch (959-967)
  keeps sid/dmac/vlan AND active=1 (stale declare + stale params after 10 s
  silence); reg_fall (971-980) clears active only. Fix in sweep_next: fire
  branch += dmac=0, vlan=0, active=0; reg_fall branch += dmac=0, vlan=0.
  SID STAYS in first landing (record sid = lwsrp row key + stream-table alias
  + lstn_sid lane; zeroing re-keys mid-flight of #32 proof; E1 restore proves
  sid-0-while-bound safe → land full sid-zeroing WITH #32 closure + provisioner
  guard want &= |sid). TB: NO_TK-lapse case (10050 ms) → dmac/vlan/active/
  declare all 0 + GET_RX_STATE bytes 54-59 zero (dmac echo fails today);
  ctx isolation case. Live: withdraw peer TA → GET_RX_STATE/GET_STREAM_INFO
  zeros + ONE Listener LV on tap.
- B1d (M-L, FOLLOW-ON): registrar match sid-only (walker 242-262 65-bit
  borrow-out); TA vlan captured never compared, dmac not captured. Table 5.29
  match = ALL THREE params; 5.3.8.9 mismatch → ignore + re-probe. Fix: stage
  expected {dmac,vlan} with row provisioning (~60 flops/sink), walker ematch
  += dmac+vlan compare (FirstValue bytes 13-18/19-20 stream past anyway);
  mismatch-pulse-to-sweep = stretch (non-registration already prevents false
  RSV_OK; NO_TK re-probes lawfully). Risk today = sid collision only (rogue/
  misconfig; sids derive from unique EIDs). TB: lwsrp TA matching sid wrong
  vlan → no areg rise (registers today). Desk-first (needs tsn-gen injector).
- B1e (S docs, KEEP deviation): declare-on-BOUND vs 5.3.8.5. Mandate
  (settled+TA ⇒ Ready) satisfied; clause silent for bound-not-settled; early
  attach = ordinary MSRP ordering + 07-29 silicon finding is WHY the
  provisioner exists (gating on settled re-slows every connect). Fix stale
  cites while there: KL_acmp_listener 72-76 + milan_datapath 1349-1350 cite
  5.5.3.5.27/.33 (UNBIND rows) where they mean .42/.48.

Shared: record layout UNCHANGED (317 bits has all fields), no new write-event
classes, w_swp_commit fencing valid. Files: KL_acmp_lstn_ctx (896-987,
478-481), KL_acmp_listener, lwsrp walker/ctx (B1d), milan_datapath (B1d),
tb acmp_lstn sim_main/sim_ctx, behave acmp_listener_tsn_gen.feature + model.

## PACKAGE B2 [gh #55] — ACMP listener response/field laws (#33 b/c items + ctx-0 leak)
CROSS-CUTTING CAVEAT: behave acmp feature validates a Python model that is
ALREADY conformant (lock check present at steps 88-104) — it can NOT catch
these RTL gaps; protection = Verilator suites + live cert-recreate only.
Landing (one coordinated round WITH B1 — same file, hard conflict zones):
(1) B2c delete → (2) unified response-field function absorbing B2d/e/f/g +
B2a/B2g refusal echo → (3) B2b + B2h together (both grow the record struct;
BRAM re-fit priced once; cbits() offset map re-derived ONCE) → (4) B2a
cross-module plumbing last. VERSION: one story with B1 (0x0031-class) or
split B1/B2 — single bump cleaner (co-edited always_comb).

- B2a (M): locked-controller check absent on BIND+UNBIND (step 1 repeated in
  EVERY bound-state clause; refusal = CONTROLLER_NOT_AUTHORIZED 5'd16 already
  in pkg; Tables 5.31/5.35 = command echo; GET_RX_STATE has NO lock check —
  reads exempt). Lock state never reaches ACMP: locking_controller_id NOT
  exported from KL_aecp_top (only locked_o, line 424). Chain: aecp_top
  locking_ctlr_o → datapath (same clk domain, no CDC) → listener wrapper →
  ctx w_lock_deny = locked_i && (w_ctlr != lock_ctlr_i), suppresses
  wr_frame/probe_set. TB sim_ctx [L]: C0 locks, C1 BIND → 16 + record
  unchanged; C0 → SUCCESS; C1 GET → SUCCESS (exempt); auto-unlock releases.
  Live: two-controller race via avdecc_l2 from two MACs.
- B2b (M): probe-response match = listener fields only; seq NEVER CAPTURED
  (beat-7 bytes 62-63 unlatched, record has no seq field; probe_seq_r =
  shared post-increment). Fix: acmp_lstn_ctx_t += seq[15:0] (317→333 bits,
  still in BRAM budget); latch emitted seq at LAUNCH_S; RESP2 resend REUSES
  it (5.5.3.5.16 "duplicate" = same seq — coordinate with B1 probe ladder,
  agree ONCE); cap_seq_r at wbeat 7; w_probe_resp += ctlr+talker+tuid+seq
  match. Duplicate = automatic (settled state guard rejects). TB: [G] OPEN 3
  gap() pin PROMOTES to ck() (today a wrong-talker response settles the
  sink); sim_ctx [N10] mismatch leg. Live: spoof response with foreign
  talker/seq → sink stays PRB_W_RESP.
- B2c (S, delete 4 lines): UNBIND arm preserves tk_avail/adp_age when
  w_sm_en (823-831) — record sits UNBOUND with tk_avail=1, aging keeps
  running, NEXT bind INHERITS stale tk_avail from a possibly different
  talker → phantom fast-ladder re-probes. 5.5.3.5.39/.45 "Stop the ADP
  Discovery SM" + fresh bind restarts "(talker has not been discovered)".
  TB [N6] += cbits(312,1)==0 + cbits(298,7)==0 + X-visible/unbind/rebind-Y-
  silent regression leg.
- B2d (S): settled GET_RX_STATE stream_id/vlan = command echo (w_str_echo
  457) → controllers send zeros → we report zeros; Tables 5.38/5.39 say
  "copied from the SRP parameters". dmac already right (cur_r.dmac). TB:
  [G] OPEN 4 gap() pins promote to ck().
- B2e (M/L): per-state flag matrix derived from Tables 5.34/5.37/5.38/5.39:
  FAST_CONNECT=1 in ALL FOUR bound states (RTL NEVER sets it); probing =
  saved SW (RTL forces SW=1 + wrong RF=ta_failed); NO_RSV = saved SW, RF=0;
  RSV_OK = saved SW, RF=ta_failed. WIDE test churn: 6 sim_main + 2 sim_ctx
  flag pins ALL encode the wrong value and flip (0x0008→0x0002 class) —
  land RTL + TB atomically. Live: walk all four states, audit bytes 64-65.
- B2f (S): BIND success echoes command's stream_dest_mac (Table 5.32 pins
  0 — fast-connect BIND with non-zero dmac echoes it back); UNBIND success
  emits OLD tuid (cur_r still pre-unbind at response time; Table 5.36 pins
  0). TB: new fast-connect-dmac + unbind-tuid byte pins (under-tested today).
- B2g (S/M): invalid-uid refusal reads cur_r = CTX-0 record (cur_idx forced
  0) → sink 0's bound talker/tuid LEAK into another sink's refusal; Table
  5.27 = command echo for every named field. Fix = the unified refusal path
  (shared with B2a): !w_uid_valid | w_lock_deny → all fields from
  fword_r/cap_* echo, independent of cur_r.
- B2h (M): TMR_NO_ADP fixed 63 s ignores valid_time (1722.1 6.2.2.5: timeout
  = vt × 2 s). CHEAP: valid_time already captured (cap_status_r bits[7:3] IS
  adp byte 16 vt for ADP frames). Fix: record += adp_vt[4:0]; age compare =
  adp_age >= {adp_vt,1'b0}. TB [15] TIMING CHANGES: its adp() helper writes
  byte 16 = 0x1F ⇒ vt=3 ⇒ 6 s not 63 — update loop + add vt=15/30 s leg.
  DEFER with rationale: interface_index (single-AVB-interface platform,
  no-op); gm/domain check (needs new gPTP→ACMP ports — follow-up); avail-
  index regression (needs bytes 36-39 capture + 32 bits/record — NEXT
  increment after vt).
- CONSOLIDATION (recommended, verified true): B2d/e/f/g + refusals = ONE
  authoritative always_comb computing {talker_eid, tuid, count, flags,
  sid, dmac, vlan} keyed on (resp_kind, cur_r.state, valid|lock_deny) —
  kills the whole class; B2a and B2g converge there.
MERGE HAZARDS with B1 (land as ONE round): classify_writeback 763-852
(B2a/b/c vs B1 arms), response assembly 442-598 (function rewrite vs B1
w_resp_flags edit), acmp_lstn_ctx_t struct (B2b seq + B2h adp_vt + any B1
field = ONE struct edit), probe_seq_r resend semantics (agree once).

## PACKAGE A [gh #56] — ACMP talker response-field law (5 confirmed; task #35)
One VERSION story, three commits: (1) A1+A5+A4 = the "Milan 5.5.4 response-field
law" table rework; (2) A3 dmac-valid; (3) A2 laf chain (deepest, lands last).

Shared mechanism: responses = echoed request RAM (fword_r) + per-beat overrides
(w_beat, KL_acmp_tlkr_ctx.sv:227-285); flags = echo AND-NOT flag_clr_r (beat 8
lanes 0-1 = bytes 64-65). Add flag_set_r[15:0] (only ever RF bit) + lstn_zero_r.
Success-table law: PROBE Table 5.43 (PDF p103) = echo FC/SW, force RF 0;
DISCONNECT Table 5.45 (p105) = all three 0; GET_TX_STATE Table 5.47 (p107) =
all three 0 except RF=1 iff registering Listener Asking Failed, listener ids
ZEROED. Error rows keep full echo (already correct).

- A1 flag inversion: replace flag_clr mask at :397 with RF-only clear.
  TB pins WRONG today: acmp sim_main case 4 line 217 expects 0x0040 → rewrite
  to 0x000A; sim_ctx T3 + header comments; traceability M-ACMP-6 row.
  Compliance: behave PROBE echo scenario (offline model ALREADY asserts echo —
  model right, RTL wrong); live raw PROBE flags 0x004A → tap 0x000A. S.
- A5 disconnect flags: flag_clr <= 0x004A in the DISCONNECT arm. TB pins WRONG:
  sim_main case 5 line 235 expects 0x004A echo → 0x0000; sim_ctx T6. S.
- A4 listener-id zeroing: lstn_zero_r gates beat 5 lanes 2-7 + beat 6 lanes
  0-1/4-5 to 0x00 (GET_TX_STATE success only; TALKER_UNKNOWN_ID keeps echo per
  Table 5.46). TB pins WRONG: sim_main case 1 lines 171/173. S.
- A3 dmac-valid (5.5.4.1 step 3 + Table 5.42, status TALKER_DEST_MAC_FAILED=5'd3):
  new src_dmac_valid_i[N] per-source; invalid → status 3, echo body, window
  STILL arms (4.3.3.1 condition 2 counts probe RECEPTION). Datapath: every bit
  = ~cfg_maap_enable | maap_addr_valid (one MAAP engine = one block).
  UNDRIVEN trap: port + wiring + TB init land in ONE commit. TB additive:
  dmac-invalid case + per-source T9 + GET_TX_STATE unaffected. Compliance:
  behave MAAP-conflict scenario (8021q feature has the declare half already);
  live: inject overlapping MAAP ANNOUNCE → CSR 0x6D0 leaves ANNOUNCE → probe
  answers status 3 → after re-address SUCCESS with new base. M.
- A2 REGISTERING_FAILED live (Table 5.47): chain = KL_lwsrp_ctx export
  row_ask_fail_o (adecl_r==ASKING_FAIL per talker-dir row, sibling of
  row_ready_o) → KL_lwsrp_top lstn_ask_fail_o[N_TALKERS] (same index law as
  stream_gate_o) → datapath acmp_laf_v_w (mirror g_lobs0/g_lobsn/g_acmp_crf_src
  1505-1528) → tlkr_ctx lstn_ask_fail_i → flag_set_r in GET_TX_STATE arm only
  (PROBE keeps RF=0 even while failing — tables differ on purpose).
  TB: laf case both flag inputs; per-source [T8]; lwsrp four-pack AskingFailed
  raises/drops. Compliance: bench oversubscribe class A → bridge turns our TA
  into Listener Asking Failed → GET_TX_STATE reads 0x0040. M; index-mapping =
  the known trap zone, pin T8 BEFORE datapath wiring.

Live proof round (all of A): both boards same VERSION, then tap probe/gts/disc
each with flags 0x004A. Files: KL_acmp_tlkr_ctx.sv, acmp_pkg.sv,
KL_acmp_responder.sv, milan_datapath.sv (1470-1546, 2733), KL_lwsrp_{ctx,top,
registrar}.sv, tb acmp sim_main/sim_ctx, behave milan_acmp_conformance.feature.

## PACKAGE C [gh #57] — ADP timing + valid_time (2 fixes + 2 decision records)
Landing: C2 → C1 (both = ONE VERSION story "ADP advertise clause-true");
C3/C4 memos ride as banner-comment updates (also retire stale DEVIATION 3 —
already closed by the MIN clamp).

- C2 (S, confirmed): ADP_CTRL reset 0x0000_1F00 → 0x0000_0A00 (valid_time 10
  per Milan 5.6.2 "shall be set to 10"; wire byte 16 = 0x50 not 0xF8).
  Consumers audited: TMR_ADVERTISE clamp MIN(5,MAX(1,vt/2)) → period STAYS 5 s;
  discover-delay envelope identical (both 10/31 take the >=4 arm); parser reads
  REMOTE vt only. NO tracked script writes ADP_CTRL (bench-side private only).
  TRAP: whole-word CSR — bare enable write 0x1 would zero vt (1 s floor +
  advertises 0); enable steps must RMW/write 0xA01. B2 interaction: acmp_pkg
  LSM_ADP_AGE_S_C=63 mirrors the OLD 62 s horizon — B2 must derive from stored
  peer vt (derive-never-mirror). TB pins to change: csr sim line 379
  (0x00001F00 → 0x00000A00), adp case 18 retarget vt 10 (keep one 31 spin as
  max-value clamp pin), milan_dp 604-605 cosmetic. Behave: steps already
  default vt 10 + assert from wire — becomes self-sufficient from reset.
- C1 (S, confirmed): TMR_ADVERTISE never restarted around DELAY-path sends
  (5.6.3.5.9 step 2 + 5.6.3.5.4 step 1 + Table 5.51 "x in DELAY"). Fix = 2
  lines in trigger_capture: tmr_advertise_w gains "&& !disc_pend_r" (timer dead
  while window open); adv_restart_w = ENTITY_AVAILABLE frame start → counter 0
  (covers every AVAILABLE flavor; DEPARTING excluded via available_r already).
  Caveat: restart not tick-aligned → next periodic 4-5 s (early-biased, legal
  under the 5 s upper bound). TB: adp case 19 (counter ripe + discover →
  NO frame for period-1 ticks; GM-path leg too); sim_dly Table 5.51 leg (tick
  mid-window → tvalid low till draw). Existing cases 2/11/14b/16/17/18 stay
  green (all enter with counter 0). Live: 30 DISCOVERs at 7 s phase-sweep →
  gap histogram floors at 4 s (today uniform 0..5).
- C3 (memo, RECOMMENDED SPLIT): skipped TMR_DELAY randomization (DEVIATION 2).
  Conform ONLY startup + link-up (the simultaneous-power-up storm cases, fire
  once, reuse disc window ~15 lines); KEEP un-jittered periodic (5.000 s
  cadence = the bench liveness oracle; discover path already randomized+
  coalescing, es-2.1 passed). Land the partial-conform as its own follow-up so
  the wire diff stays auditable. Risk kept: low operational, medium on paper.
- C4 (memo, KEEP): available_index monotonic across DEPARTING (DEVIATION 1).
  Decisive: Milan 5.6.3.5.8/.11 enumerate departing steps with NO index-reset;
  5.6.4.5.2 only requires never-repeat/regress while available — monotonicity
  guarantees it unconditionally. Power-cycle reset honored. la_avdecc/Hive
  compat proven 07-12. Reserve conform = 1 line at frame egress + ~15 TB
  expectation shifts if a pure-1722.1 audit forces it.

Files: adp_advertiser.sv (208-265, 443-473, 519-539), milan_csr.sv:1177,
tb adp sim_main/sim_dly, tb csr, behave milan_adp_advertisements.feature;
doc sweep: milan_system_map.gen.py:172 stale vt note.

## PACKAGE D [gh #58] — AECP stream-command laws (4 stories inside one window)
D2 (adversarial) CONVERGES with D on every point. D5 verdict: CONFIRMED for
SET_CONFIGURATION, REFUTED for GET (read-only, correctly l0-exempt).
Landing: Story A (D1+D5+D3, one VERSION = "running/bound stream-command law")
→ Story B (D2, own commit same window, only piece rewriting green checks) →
Story C (D6, independent, any order) → Story D (D4, grows IDLE arbiter, last).

Shared plumbing (A): two 16-bit builder ports via KL_aecp_top —
lstn_bound_v_i = zero-ext acmpl_bound_v_w (dp 1342; CRF = index N_STREAMS);
out_streaming_v_i = zero-ext {crft_emit_en_w, aaf_stream_en_w} (dp 1641,
5.3.7.3 rendered; CRF output licence-gated). Derive-never-mirror: these ARE
the live wire gates. FLAG: cfg_aaf_bypass ⇒ outputs count streaming ⇒
SET_CONFIG/SET_FMT(out) refuse — truthful, will surprise bypass bring-up.

- D1 (M, HIGH): gate rung between NO_SUCH_DESCRIPTOR and BAD_ARGUMENTS in
  BOTH ifdef arms (3291-3350 + 3352-3396): input = bound level EXACTLY
  (5.3.8.2 note = the licence for narrowness — NOT reservation, NOT lwsrp,
  or the adaptation flow breaks); output = streaming per 5.3.7.3. status 12,
  seg 12, cdl 24. Precedence l0 > NSD > SIR > BAD_ARGS. Refusal auto: no wb,
  no fmt_in0_r, no prune, no journal, no u=1 replay. TB rewrites: [22e] 7→12,
  [22f2] restage unbind-first + bound twin, [12f] restimulate via vector.
  New: fmt2/fmt4 per-index isolation, output leg, sim_nxn END-TO-END real
  BIND_RX → SET → 12. Live: Hive reformat-while-connected → STREAM_IS_RUNNING
  dialog; adaptation regression proof = cert-recreate flow: DISCONNECT → SET
  (byte 16 0x00) → CONNECT → audio, UF stays 0. Wire refusal = bytes 16-17
  0x60 0x18.
- D5 (S after A): SET_CONFIGURATION rung: w_entity_streaming =
  |(lstn_bound_v & in_served_mask) | |(out_streaming_v & out_served_mask)
  (served masks from shape constants — unbacked lanes can never wedge).
  Same-value SET while streaming STILL refuses (what CERT pokes). GET exempt.
  Multi-config note: L0 current_config_r commit must gate too IF multi-config
  ever lands (comment only now). TB: new sim_main pair + lock-outranks case.
- D3 (S): SET_STREAM_INFO index gate 3504: w_gs_index != 0 →
  >= PRES_N_C (legacy shape identical); AND 3508 listener_observed_i →
  out_streaming_v_i[idx] (stream 0's listener must not block output 3).
  pres_file_r verified per-index (670-698; CRF entry feeds crf_tx
  transit_ns_i). TB new sim_nxn: SET(out5) ACC_LAT 3ms → GET(out5) reflects,
  out0 isolated; out9 → NSD; streaming[5] → 12 while out4 succeeds. Live:
  Hive per-stream PTO edit on outputs 1-8 (errors NSD today); AAF talker 3
  avtp_timestamp lead shifts by delta (latency-taps observable).
- D2 (M): shrink-prune → refuse BAD_ARGUMENTS (5.4.2.7 sentence overturns the
  1140-1147 judgment call — it cited 7.4.9/5.4.2.6, the wrong clause).
  DMAP_PRUNE_S → DMAP_FCHK_S pre-commit checker: hit ⇒ status 7, cancel wb
  (wb_len 0, seg SEG_NONE), NEVER writes; clean ⇒ deferred dm_sch_r commit
  then WRITE_S. Prune write path DIES (no legal trigger remains: accepted
  shrink orphans nothing by construction; outputs identity-only so vacuous;
  single config; reset re-seeds). Delicate: deferred commit under two ifdef
  arms. TB sim_dynmap2 [6] rewrite list (5 checks flip incl "st0 ch5 BAD_ARG
  again" 7→0 + remove-then-reshrink restage); sim_odmap [8] already aligned.
  Live: Hive ADD ch5 map → reformat 2ch → BAD_ARGUMENTS (bytes 16-17 0x38
  0x18), map intact; REMOVE → retry → SUCCESS.
- D6 (S, #34): replay demote sites gated !unsol_frame_r (4276 input, 4216
  output). Root: CONCLUDE pend4 re-RUNS DECIDE against capture RAM u=1;
  REMOVE already cleared store → validate pass misses → BAD_ARGUMENTS u=1
  frame announces a failure that never happened. Commit passes ALREADY
  idempotent (sim_dynmap 363 pins ADD re-commit). Do NOT skip-the-walk (kills
  that pin). Genuine second REMOVE still refuses per 7.4.46.1. State can't
  drift mid-replay (tready gated while pend4). TB: replay status quartet
  pins (status byte UNCHECKED today at sim_dynmap 383); sim_odmap output-dir
  case. Live: A removes map → B's u=1 shows SUCCESS (today la_avdecc logs
  invalid non-success unsolicited).
- D4 (S/M): lock auto-expiry push: l0 lock_expired_p_o pulse (218-226) →
  builder pend10 (arm ALL registered slots incl the locker if registered —
  5.4.2.2 note), IDLE arm LAST priority: u=1 LOCK_ENTITY response, SUCCESS,
  flags 0x00000001 UNLOCK, locked_id 0, desc ENTITY/0, cdl 28. No rate law
  needed (one-shot per lock by construction; the 1/s cap is GET_COUNTERS-row
  only). Do NOT revive the dead KL_aecp_timers lock_expired_o (tied off; live
  counter is L0's). TB sim_unsol: A+B registered, C locks, 60000 ticks (6M
  cycles at -G100k, simulable) → exactly 2 pushes (A,B not C), then B locks
  immediately (state clear, no double push); explicit UNLOCK → NO push.
  Live: Hive lock indicator self-clears at 60 s (goes stale today); tap byte
  36 0x80 + cmd 0x0001 + flags bytes 38-41 00 00 00 01.

## PACKAGE D2 — Adversarial second opinion on D1 (SET_STREAM_FORMAT gate): CONFIRMED
Independent derivation agrees + STRENGTHENS the finding. Key law:
- INPUT predicate = BOUND (5.3.8.2: "bound does not necessarily mean data is
  flowing or even that bandwidth is reserved") — pure ACMP bind level, NOT
  started/settled/streaming. STOP_STREAMING'd-but-bound must STILL refuse.
- OUTPUT predicate = STREAMING per 5.3.7.3 = declaring TA AND Listener
  Ready/ReadyFailed registered (STREAMING_WAIT cannot exist on outputs).
- Refusal is VALUE-INDEPENDENT: same-format SET while bound → 12 too (no
  nochg carve-out; "In all other cases SUCCESS" excludes bound by
  construction). STREAM_IS_RUNNING = 5'd12, already in aecp_pkg:100.
- ADJACENT CONFIRM: SET_CONFIGURATION arm (2888-2899) violates 5.4.2.5
  identically (l0 gate only) — D5 verified, same predicate reused.
- Extra teeth today: SUCCESS + differing bytes → CONCLUDE u=1 replay
  BROADCASTS the format change of a running stream to other controllers.
Fix design (independent, converges with D1 brief):
- lstn_bound_v_i[16] from acmpl_bound_v_w (dp 1342, exported 2828 — already
  feeds lwsrp provisioner + stream table; index law matches AEM order incl CRF
  pinned last). tlk_streaming_v_i[16] = aaf_stream_en_w | (talker_active &
  lwsrp_stream_gate); CRF bit = crft_emit_en | crft_res_active. Verify
  stream_gate asserts on ReadyFailed too (5.3.7.3 includes it).
- Placement: between NO_SUCH_DESCRIPTOR and BAD_ARGUMENTS, BOTH ifdef
  branches (after 3300 + 3355). STREAM_IS_RUNNING outranks BAD_ARGUMENTS
  ("before accepting" makes format check part of the accept path); l0 stays
  first. seg_len 12, cdl 24 full-size. Refusal auto-produces: no write-back,
  no fmt_in0_r retarget, no prune, no journal capture, no u=1 replay (all
  keyed on SUCCESS/wb_addr).
- Adaptation flow SURVIVES: bound_v rises only on completed BIND_RX, falls on
  unbind — the whole pre-bind window stays writable; persist restore = store
  writes not AECP, no deadlock.
- TB checks that pin the WRONG law today: sim_main [22e] third case expects
  7 must become 12 (bound outranks BAD_ARGUMENTS); [22f2] adaptive SET runs
  while bound expecting SUCCESS — reorder or clear bound. sim_fmt2/4 run
  unbound = green. NEW: [22g] 8-case bound-gate ladder; sim_unsol no-replay-
  on-refusal; sim_fmt4 [5] middle sink + CRF + output legs; sim_nxn
  END-TO-END real BIND_RX → SET → 12 (proves plumbing not just pins).
- Live: bind sink 0 even stream → SET same+different → wire status 12
  (byte 16 = 0x60 class), GET unchanged, counters twice no UF/MR movement,
  audio uninterrupted, Hive sees NO format notification; unbind → SET → 0;
  talker: peer bound FRAMES_TX ticking → SET out0 identity → 12; peer
  disconnect (TA declared, gate falls) → 0. Bench cert-recreate steps that
  SET after connect must reorder to SET-then-BIND.

## PACKAGE E [gh #59] — Departing-controller detection (Milan 5.4.5.3, M-AECP-11; L, MVP=M)
Clause corrections vs my brief: CONTROLLER_AVAILABLE = 1722.1-2021 clause 7.4.4
cmd 0x0003 (NOT 7.4.36; already in aecp_pkg as CMD_CONTROLLER_AVAILABLE=15'd3).
Notification direction settled 3x: DEREGISTER push goes TO THE DEPARTING
CONTROLLER ONLY. Retry law 9.3.2.6/9.3.6: 250 ms timeout, ONE retry with the
SAME sequence_id, then evict. Worst-case detection 60.5 s.

Design:
- "Heard" = any valid AECP command in DECIDE_S with matching controller EID
  (w_unsol_match exists at 1543-1548), INCLUDING reads + error-status replies +
  VU commands; excludes ACMP/ADP + our own frames. CA replies fold into the
  same heard_p vector. Slot key = EID (MAC refreshed on REGISTER only).
- Timer engine wires the KL_aecp_timers stub (its own TODO): per-slot 16-bit
  ms downcounter @tick_1khz, reload on heard/birth with 30000+fold15(LFSR)
  (LFSR seeded from entity_id — boards never probe in lockstep); shared 250 ms
  ack downcounter (probes serialized). Params MONITOR_MIN/RND/ACK_MS_P
  TB-shrinkable, defaults derive from STALE_TIMER_TICKS_C.
- RX: ingress snoop = adp_pend_r witness pattern (fields done by beat 4):
  msg_type==1 + cmd==0x0003 + controller_eid==ours → ca_reply_p_o +
  ca_reply_eid_o (target = who answered). Status IGNORED ("no matter the
  value"). Frame still drains to validator drop path. TODAY the validator
  drops all responses — that's why nothing can reach us.
- TX: FIRST-EVER initiator arm. Two new IDLE_S arms (0 new FSM states), push
  idiom → WRITE_S→EMIT→CONCLUDE. CA command frame 46 B: byte15=0x00
  (AEM_COMMAND), cdl 0x00C, target_entity_id = CONTROLLER EID (needs 8-byte
  mux in hdr_byte — line 1279 hardwires ours; ca_frame_r selects),
  controller_entity_id = OURS, seq from NEW ca_seq_r space (disjoint from
  unsol_seq_r), retry re-sends SAME seq. ca_frame_r must NOT set
  unsol_frame_r (bit-36 u law) — self_frame = unsol|ca takes the no-meta-pop
  role in CONCLUDE.
- Eviction: stage {MAC,EID,seq}, clear unsol_valid_r + pend bits IMMEDIATELY
  (no zombie slot in dedup/arbitration), dereg_pend arm emits u=1 SUCCESS
  DEREGISTER 0x0025 unicast from staging. Re-REGISTER lands fresh with seq 0.
- IDLE priority: pend4 replay FIRST (capture-RAM dependency) → cmd capture →
  pend chain → dereg_pend → ca probe. Ack timer starts at probe CONCLUDE so
  arbitration delay can't fake a timeout.
- NO_RESOURCES arm (5.4.2.21 "may", full phase): refused REGISTER pulses
  force_expire → probe sweep → dead slots free in ~1 s → next REGISTER wins.
  "Never deregister a responder" inherent (reply⇒heard⇒reload).
Sizing: ~310 new FF, 0 new FSM states, one clock domain.

TB: NEW sim_ctrlavail.cpp (sim_unsol 282 checks FROZEN), -G shrunk timers
(300/100/50 ms): 7 cases — probe-on-deadline (frame bytes pinned), answered→
kept (incl nonzero status), unanswered→same-seq retry→evict→dereg unicast to A
only (B unaffected, re-REG seq 0), NO_RESOURCES recovers, read-only controller
never probed, two silent controllers serialized, LFSR randomness witness.
Plus kl-aecp-timers utest update + Makefile obj_ctrlavail leg.

Compliance: live = register Hive on pw0 → kill -9 → tap shows last cmd → CA
probe in 30-60 s → retry 250 ms → u=1 DEREGISTER to Hive's MAC only → SILENCE
(today: pushes to the corpse MAC forever); restart Hive → REGISTER SUCCESS seq
0. Alive path: idle Hive 5 min → probes answered, never evicted (7.4.4 SHALL).
New diag CSR word in free 0x6xx block (probes/replies/evictions) for the
all-counters sweep. Risks: hdr_byte mux in the emit header cone (re-check
100 MHz timing — burned before); bench controller violating 7.4.4 = evicted
while mute = spec-correct (re-registers).
VERSION story: "A DEAD CONTROLLER IS NOTICED, PROBED TWICE, AND SHED".
Files: KL_aecp_timers, KL_aecp_top (229-234), builder (1497-1526, 2359+,
hdr_byte 1268-86, 3826-59, 4417-38), KL_aecp_ingress (146-254), aecp_pkg;
traceability flips milan-v12.md:83 + AEM_AND_AECP.md + PROTOCOL_TRACEABILITY.

## PACKAGE F [gh #60] — Table 5.22 push coverage + rate law (4 items; VERSION 0x0031 sketch)
Clause: "not more than one unsolicited notification per descriptor per second";
row scoped to EVERY descriptor keeping counters. Landing order: F1 → F4
decision → F2 (sources first, then builder) → F3 rides F2.

- F1 (S): AVB_IF push (pend3, builder 2240-2243) armed straight from link/GM
  edges, NO limiter — 5 Hz flap = 5 pushes/s = violation. Fix = clkdom idiom:
  avbif_dirty_r + avbif_rl_ms_r 10-bit, reset SATURATED (first edge pushes at
  once, sim_unsol [4] depends on it), consume-on-send guarded by
  w_unsol_anyvalid. Raw LINK_UP/DOWN/GM totals keep counting unthrottled.
  TB sim_unsol [8]: 5 Hz flap 2 s → 1 immediate + 1 window-expiry frame with
  accumulated totals. Live: bounce switch port >1/s, tap counts ≤1/s.
- F2 (L): sinks 1..N-1 + CRF can NEVER push. Root: ctx monitor dirty_p_o is
  SCALAR ("stream-0"), == '0 gates at 928-930/960/1013/1031 exist only for the
  port contract (index in hand at every site: iv_s_w/ev_s_r); KL_crf_rx has no
  dirty port; builder has no pend class. Fix: (1) vectorize dirty_p_o
  [N_LISTENERS], drop == '0 terms, FRX exclusion stays per-context;
  (2) KL_crf_rx dirty_p_o pulse on lock(442)/unlock(414)/SI(396)/six anomaly
  interval commits(368-376)/bind-rise wipe(490-499) — NEVER pdu_count (healthy
  FRX = the task-21 exclusion); (3) builder: rxdiag_dirty_p_i[15:0] (mirror
  tkdiag cast 16'() at dp 2642) + crf_cnt_dirty_p_i; in_dirty_r/in_rl_ms_r
  per-descriptor limiters (SO shape 1480-1487, reset-saturated); pend10 (AAF
  bitmap, pend5 idiom) + pend11 (CRF scalar); gs_diag_idx pre-mux gains pend10
  term AFTER pend5 (IDLE chain priority matches by construction); payloads =
  load_input_counters_consts (mirror, 0xFFF) / load_crf_input_counters_consts
  (direct ports, 0xF3F — no muxing needed). TB: sim_unsol [9] sink-1 anomaly
  push (desc bytes 00 05 00 01), [10] CRF push at index n_aaf_sinks_i;
  crf_rx "dirty port law" leg; rxmon "dirty vector per-context" leg.
  Live: bind sink 2 (EVEN on silicon — odd = secondary net), force LATE →
  that sink's own push cadence; CRF source muted → STREAM_INPUT[crf] +
  CLOCK_DOMAIN pushes distinct.
- F3 (S riding F2 / M standalone): clk_src==2 mux (dp 2684-2687) splices CRF
  lock tallies into the sink-0 PUSH payload (load_input0_counters_consts @2435)
  while solicited serves the true mirror — push vs solicited DISAGREE on the
  same descriptor. Fix riding F2: retire pend2 + load_input0_counters_consts;
  sink 0 = bit 0 of pend10; in0_cnt_locked/unlocked_i stay ONLY as the
  CLOCK_DOMAIN source (pend9 = the one lawful follower of the active source).
  Hotfix if F2 slips: swap 2435 to the mirror task + pre-mux pend2 term ahead
  of pend5. TB sim_unsol [11]: push byte-equals solicited on all 12 words with
  clk_src=2 (fails today on ML/MU); CLOCK_DOMAIN push still carries the mux.
  Live: Hive pushed view vs manual refresh identical; CRF lock drop moves only
  CRF-sink + CLOCK_DOMAIN panes.
- F4 (S, decision — RECOMMENDED (c) split): M_PDEC_S site 960 arms dirty on
  EVERY accepted PDU (TV/TNV per-PDU) → sink-0 push 1/s while healthy-streaming
  forever. (c): TV joins the FRX exclusion (healthy-path tally, value still
  rides every payload), TNV stays armed (no-valid-timestamp = anomaly). Site
  becomes: arm iff !cur_r.tv || lock_now_w || (seq_mm && lost>=INTERRUPT_MIN).
  MUST be decided before F2 vectorizes site 960. TB rxmon "TV silent, TNV
  armed" (flips today's behavior). Live: healthy 60 s stream → 0 pushes
  (today ~60); forced tv=0 → 1/s + Hive TNV climbs.

Files: builder (pend 1466-1560, arm 2194-2308, emit 2358-2664, tasks 1795-1899,
pre-mux 440-449), KL_avtp_rx_monitor_ctx (928-1031, mirror 735-755), KL_crf_rx
(364-507), milan_datapath (2577-2698, 4155-4174), sim_unsol.

## PACKAGE G [gh #61] — Counter backing law (1 fix + 1 decision record)
- G1 (S, RECOMMENDED widen): CRF sink counters — TWO deviations: UF/SM 8-bit
  SATURATING (saturation itself violates "wraps to zero"; peg at 255 after
  4 min 15 s of persistent fault, then a FROZEN instrument — same class as the
  AVTP-5t advertised-valid-never-moves purge), FRX/MR/TU/LT/ET 16-bit wrap at
  65536 s = 18 h 12 min soak mark (all seven are +1/interval — the "131 s at
  500 PDU/s" premise applies only if the coalesced law ever unifies onto CRF,
  which makes 32-bit MANDATORY then). Why 8/16: CRF_STATUS 0x74C packs
  {pdu16,fmt8,seq8}; 0x738 group is FULL. Fix: widen all seven to 32 in
  KL_crf_rx (drop saturation mux), 0x74C serves documented truncated SLICES
  (ABI byte-identical), builder zero-extends die. +128 flops. Never observed
  on silicon (bench CRF profile-conformant; #23 observe still open) = latent,
  255 s from first wrong-profile exposure. TB: crf_rx wrap cases via
  --public-flat-rw preload (FRX 65534 → 65536 reads 0x00010000 on AECP wire
  while 0x74C[31:16] reads 0; fmt_err 254 → 256 not pegged-255). Compliance:
  GET_COUNTERS on CRF index frozen at 0x000000FF after ~4 min wrong-profile =
  today's defect signature; 18.2 h soak wrap.
- G2 (S, RECOMMENDED (b) keep): FRAMES_RX coalesced law (08-05 ruling) vs
  Table 5.6 letter. Defense SHARPENED: per-frame FRX IS a conformant
  implementation whose observation interval = one packet time (125 us class A,
  legally "implementation-specific <= 1 s"); Milan 1.3's TV/TNV are per-frame
  siblings in the same block and TV+TNV==FRX only exists under that reading;
  TX has NO per-frame siblings + silicon showed raw total misleads → the
  TX-letter/RX-ecosystem split is coherent per-descriptor and matches the
  certified peer. THIRD asymmetry owned: CRF input is ALREADY +1/interval
  (stays — no TV/TNV siblings, and 16-bit backing can't absorb 500/s until
  G1). Residual documented: batched tick commit is wire-distinguishable by two
  polls under 1 s (equal, then ~+8000 step); hardening (b') = commit per
  accepted PDU (indistinguishable from 125 us interval) if certification ever
  flags. Internal checker asserts NEITHER reading (PASS/per-frame,
  INFO/milan-interval, FAIL only FRX>TV+TNV) → device files clean today.
  Flip set if (a) ever ordered: rxmon nx [M13e2][IV0][IV1b]+341/356/373,
  sim_main 131/139/179/346-357, licence feature ~18k/s green threshold,
  torture classifier verdict. Add one cadence case pinning the tick-step
  observable + fix stale [IV1] banner ("+1 (was +6)" prints while asserting
  +6). (a) needs USER sign-off — overturns a standing ruling.

## PACKAGE H [gh #62] — AVTP residuals (3 fixes + 1 stale-doc closure + 1 keep-memo)
Landing: H1 (own VERSION, re-baselines suites) → H2a+b (one VERSION, one
clause family) → H3 (separate VERSION though same file as H2b — clean silicon
attribution; byte-identical at default MTT) → H4/H5 docs no VERSION.

- H1 (S RTL, M with re-baseline): version nibble — 1722 4.4.3.4 says DISCARD
  (stronger than ignore); CRF Table 7.1 pins v=0. Fix: avtp_ver = b1[6:4],
  fire gate += (avtp_ver == 3'd0) — structurally the discard (no parse/match/
  frames tick anywhere downstream). Counter law: discarded PDU moves NOTHING
  on the Stream Input (FRX = "received on this Stream Input"; UF = format
  mismatch, version ≠ format); only MAC RMON interface FRX ticks. Fallout
  AUDITED: tsn_fuzz stream yaml has version expected:0 → zero checks
  affected but zero gate coverage; avtp_parser builder line 128 emits
  VERSION=1 IN EVERY FRAME (~10,400 checks flip — golden frames were illegal;
  one-line builder fix re-greens); avtp_stream same |0x10| (21 checks);
  rxmon [31a] was WRITTEN to characterize the gap — flip + traceability
  AVTP-3 row in the SAME commit (its comment mandates it). New: parser
  Group V version sweep 0-7 AAF+CRF tagged/untagged; rxmon [31b] lock holds +
  SEQ frozen across v1 PDUs with wild seq. Live: inject v1 AAF (byte O+1
  0x91) with bound sid → FRX/UF/SM/ML all frozen, RMON ticks.
- H2 (a S, b M): mr plumbing — PICS CRF-3/4/5 all CRF:M; we fail 3+5
  (constant 0) and 4 (no echo). (a) KL_crf_rx w_ev_mr_w detector EXISTS (300)
  — export mr_toggle_p_o, OR into mcr_restart_p_w under the existing
  clk_src==2 gate (matches 10.4.3 scoping "only the stream being used for
  recovery"); seeding rules already prevent phantom echoes. (b) KL_crf_tx
  mr_i latched at launch beside tu_r, pdu[1] = {1'b1,3'd0,mr_r,2'b00,tu_r},
  mr_last_o export; widen KL_media_clock_restart to ACMP_SRC_C (CRF context
  = index N_STREAMS everywhere already) reusing talker_diag muxing verbatim →
  8-PDU hold + engine-wide target FREE + toggles on SET_CLOCK_SOURCE/upstream
  disruption; ALSO fix talker_diag.frame_mr_i mux so CRF SO MEDIA_RESET
  counts the real wire. Stale banner KL_media_clock_restart 63-69 ("crf_rx
  does not parse it" — false since AVTP-5t). TB: crf_rx toggle/seed/reject
  legs; crf_tx byte 15 = 0x88/0x89 + mr_last_o; tkdiag T14 CRF-context hold.
  Live: slave to peer CRF, interrupt >100 ms → our AAF byte O+1 bit 3 flips
  once, holds 8 PDUs, our CRF output flips, peer's SI MEDIA_RESET scores it
  (today: permanent 0).
- H3 (M): Eq 14 rounding — P = the MEDIA CLOCK period (where-list settles
  it: "nominal period of the clock source"), NOT the 2 ms interval spacing
  (that would add up to 2 ms gratuitous latency). T_C=0 for us. Fix: on MTT
  change (CSR-rate) sequential divide: n = (MTT*3 + 62499)/62500, ofs =
  (n*62500 + 2)/3 (sub-ns ceiling bias 2/3 ns, five orders under the 10.8
  wander budget); launches use PREVIOUS rounded value during conversion.
  MTT 2,000,000 → n=96 → BYTE-IDENTICAL default. TB: transit sweep
  (1,000,001 → +1,020,834; 20,833 → +20,834; mid-stream rewrite between
  frames). Live: SET MTT 1,000,001 → tap T_CRF−gPTP = 1,020,834, deltas stay
  96 periods, peer lock unaffected.
- H4 (S docs, PREMISE STALE): zero-fill ALREADY covers all declared slots
  (ZF_TOTAL_C = full consumption at dp 1004; crossbar walks every slot,
  banner "unmapped slot injects silence"); check_wire_accountability demoted
  W3 to INFORMATIONAL 07-28; gaps-doc line 1121 "still OPEN" PREDATES the
  fill = stale, fix it (+ 8x8 yaml header says TDM16, truth = tdm32).
  Decision: KEEP full-licence silence fill; REJECT builder shrink (silence
  is legal PCM; over-declaration deliberate — rings/tone/loop/crossbar can
  feed any slot; static-shape directive). Shapes: tdm8 EXACT (no exposure);
  8x8 = talkers 4-7 ride the fill, compliant; >32 slots refuses at
  elaboration (fails loud never quiet). TB: milan_dp N=8 leg — over-supply
  talker frames at class rate all-zero payload. Live: bind streams 4+6 on
  8x8 → FRAMES_TX ticks, tap shows 8ch digital silence, listener LOCKS.
- H5 (memo, KEEP family-accept): Milan 6.4 = the defense (input SHALL
  advertise ALL channel counts of the rate family → family member can't be
  UNSUPPORTED); gate still strict on rate/depth/encap/sparse = no misdecode
  possible; mismatch = controller failure by construction (adaptation
  directive); risk = literal 4.4.2.2 injection test only. Strict-mode toggle
  if forced: S — one AEM enable bit + one compare term (equality, or
  p_chans <= f_chans under the Annex I.2.4 up-to convention via Milan 6.5).
  Observable now: family PDU → UF frozen, FRX moves, subset plays; 96k/24bit
  → UF moves.

## PACKAGE I [gh #63] — SRP/802.1Q (5 confirmed + 1 keep-memo; landing I1→I3→I5→I2→I4→I6)
- I1 (S, mechanisms REFUTED, symptom real): the 60-byte keep-0x0F MRPDU walker
  trace is CLEAN (registers at wire byte 30; frame_end_w = the 10.8.1.2 f)
  law; keep honored byte-for-byte). REAL defect: KL_lwsrp_ingress registers
  rx_tvalid_i ONLY (no tready input) while tapping rx_axis_to_dma — a stalled
  DMA parks a beat and the tap consumes EVERY parked cycle as a new beat →
  duplicated/torn frames → next real PDU spent realigning. KL_maap does it
  right (in_acc = tvalid && tready). Silicon-real: DMA lane backpressures in
  the promisc-flood/single-hart-starvation regimes → missed bridge Listener
  Ready re-declarations = licence flap with NO counter. Fix: thread
  rx_tready_i through top→rx→ingress, qualify the tap, wire dp 4700.
  TB: single keep-honest PDU registers first-shot (0x37E); parked-lane
  torture; enable-mid-frame resync; DELETE the empirical double-feed in
  sim_nxn 830-837. Live: iperf-flood till DMA backpressures → one Listener
  Ready → 0x694 = 0x37E first PDU.
  ADJACENT CLASS (tracked separately): same handshake-blind tap in
  KL_acmp_tlkr_ctx, KL_acmp_lstn_ctx, AECP ingress (dp 2701/2745/2831) —
  ACMP/AECP commands can be missed/duplicated under DMA backpressure.
- I3 (S): rIn registers/refreshes where Table 10-4 has NO rIn! row (events =
  New/JoinIn/JoinMt only; In means "sender's registrar holds it, sender NOT
  declaring" — registering on In fabricates a declaration nobody made).
  THREE sites: registrar 113-115 (refresh + CANCELS leave timer — after
  LeaveAll a drained listener is held ~1 LeaveTime/hop, licence held open);
  lwsrp_ctx 289-291 talker-dir refresh + 313-330 listener-dir REGISTERS
  from MT on bare In (worst); ta_registrar 66 w_join_evt includes IN (false
  "remote talker present" from the echo of our own declaration on a loop
  bench). Fix: delete the In arms everywhere. TB: JoinIn→LeaveAll→In-only
  refreshes → expires at LeaveTime; In-from-empty stays MT. Live: switch
  LeaveAll + peer silence → licence closes at 5 s not held.
- I5 (M-L): CBS accrual violates 8.6.8.2 — per-byte DEBIT is exact, but
  "transmit" = FIFO beat acceptance so idleSlope accrues DURING the frame's
  real wire occupation (RTL's own REQ-CBS-07 note pins 9.6%/20.5% over-
  delivery at 100/200 Mb/s). Latent (all queues cbs_shaped=0), live the
  moment per-queue CBS enables. Fix = wire-debt accumulator per queue:
  Q16 bytes += beat bytes + tlast overhead (24 + min-frame pad max(0,60−L) —
  matters for CRF-size frames); drain at port byte-rate elaboration constant
  (1.25 B/cyc @1G/100MHz); wire_transmit = (debt>0) replaces the accrual
  qualifier; credit ≤ standard trajectory inside windows, equal at frame
  boundaries, long-run exactly S/8. SlopeEngineRef unchanged; both ref
  models gain the debt law; REQ-CBS-07 assertion flips to the law. Live:
  cbs_shaped on class-A queue, saturate, tap 10 s → 12.5 MB/s ±1% (13.7
  today). Honest M-L: ref-model + expected-table rewrite is the bulk.
- I2 (M): TA declared from boot = CONFIRMED violation — 4.3.3.1 governs
  DECLARING (5.3.7.2 "as soon as it has VALID SRP parameters"; 5.3.7.4
  "valid SRP parameters shall populate the FirstValue"; the Note kills
  always-declare). The dp 3319 fast-connect counter-argument REFUTED: a
  fast-connecting listener's CONNECT_TX arms our probe window → TA within
  one JoinTime (200 ms), before the listener SM times out. Gate corrections
  vs the naive talker_active reuse: (a) condition-2 listener half = ANY
  Listener attribute registration (lwsrp_listener_reg / ctx_reg_o), NOT
  listener_ready — else AskingFailed can never open the declaration =
  deadlock; (b) AND the MAAP term (same as streaming gate). Fix at datapath:
  row-0 talker_en + fabric want terms gain (talker_active | listener_reg |
  bypass-CSR-bit reset 0). Breaks: cold-boot wire silence until probe/bind/
  listener (bench flows gain a stimulus step; sim_nxn re-sequencing).
  ADJACENT GAP recorded: bw-gate refusal should declare TalkerFailed —
  KL_lwsrp_tx can only declare TA (out of scope here).
  Live: ProfiShark cold boot → no TA until Hive probes; withdraw LV 15 s
  after last probe with no listener.
- I4 (M): Domain mismatch = boundary flag only; Milan 4.2.7.2.1 mandates
  ADOPTING the received FirstValue + declaring matching. Scope settled by
  the clause + 5.3.7.5: OPERATIONAL adoption (tags follow, not just the
  declared attribute). Staged: (1) registrar adopted_{prio,vid} + op pair,
  dom_match compares vs OPERATIONAL pair (else boundary re-latches against
  the adopted net); revert on enable-fall/link-down ONLY (the clause's own
  reset list); (2) Domain FirstValue + MVRP VID + TA DataFrameParameters +
  AAF/CRF tag mux all take op pair; status CSR surfaces it (software
  follows, never mirrors). AAF_CTRL[27:16] stays the sw-owned default.
  Bench VID-2 truth untouched (adoption = no-op vs default; the proof NEEDS
  the switch reconfigured to a non-default SR VID). TB: inject {6,3,VID 5}
  → everything moves to 5, boundary only vs adopted pair, revert on toggle.
- I6 (S memo, KEEP + conform-lite): per-stream CBS absent vs Milan 4.3.4.
  Defense: 34.6.1's own "consistent with" hedge + per-stream placement-rate
  bound met AT SOURCE by construction (one frame per 125 us media tick per
  framer); residual = intra-interval burst ≤ N×(MaxFrame+24) ≈ 16 us at 8x8,
  re-spread by the first bridge's class shaper. Cost to conform: ~3,400 LUT
  + 48 DSP + 8 buffers on a 99.84%-LUT die. Memo carries: cadence proof from
  diag counters + burst bound + wire measurement. CONFORM-LITE staged path:
  once I5 lands, ENABLING the existing class-A queue CBS (+ routing streams
  through it instead of post-shaper injection) closes the "overall SR class"
  half of 4.3.4 for a mux move — record as staged, decline per-stream queues.

## PACKAGE J [gh #64] — gPTP plane (4 confirmed; landing J2 → J3 → J1 → J4)
All four suspects CONFIRMED (with sharpenings). Repo split: J2 fabric-only;
J3 fabric+board-software SAME flash round; J1 board-software only (fabric
half already in + TB-gated); J4 fabric+statd, bench proof needs 2nd bridge.

- J2 (S, fabric): A_PTP_INCR reset 0x0800_0000 = 8 ns tick (125 MHz mirror)
  while AX PHC domain = 100 MHz → PHC free-runs 200,000 ppm SLOW (not fast)
  from reset till kl-eth probe; CLKV tu=1 mitigates. Fix derive-never-mirror:
  milan_csr gains PHC_CLK_FREQ_HZ_P, PTP_INCR_RST_C = rounded (1e9<<24)/freq
  + $error guard <3,906,251 Hz; datapath passes MILAN_CLK_FREQ_HZ; milan_top
  passes 125 MHz explicit. 100 MHz literal = 0x0A00_0000 EXACT. TB: csr line
  182 keeps 125 MHz pin; csr_win override build adds 100 MHz pin with C++
  independent oracle. Live: cold-boot devmem 0x504 pre-driver = 0x0A000000.
- J3 (M, fabric+daemon PAIRED): AS_CAPABLE = |pdelay CSR| proxy (builder
  3599 + push arm 2589) — stale-true forever on daemon death, AND flag-flaps
  on a starved pmc read (script maps unanswered → pd=0). Not the 10.2.5.1
  variable; Milan Table 5.22 names asCapable a push trigger so the proxy also
  corrupts the push law. Fix: CLKV_CTRL bit 2 (currently masked-to-0 =
  backward compatible) carries the daemon's asCapable claim; KL_ptp_clock_
  validity registers as_cap_r cleared ON LEASE LAPSE (deadman = the existing
  lease, 8-26 s); stat_o[16]; builder as_capable_i replaces |pdelay| in flags
  + w_avbi_sig (keep pdelay[31:8] term). Daemon: pmc GET PORT_DATA_SET_NP
  (linuxptp prints asCapable), compose (LEASE<<4)|(as_cap<<2)|...; ALSO fix:
  unanswered pdelay read must HOLD last value not publish 0. TB: clkvalid
  lease-lapse leg; aecp flags 0x07→0x06 + push arrival; csr bit-2 readback.
  Live: kill ptp4l → Hive AS_CAPABLE flips FALSE via push within one lease,
  tu returns 1 simultaneously; restart → returns after LOCK_N.
- J1 (S code + M bench): ILAT/ELAT — fabric DONE and sign-correct (ptp_ts
  186-188, TB-gated); bench applies whole sum as ptp4l ingressLatency ONLY.
  SHARPENED: pdelay needs only the SUM ((iL+eL)/2) so it reads perfect, but
  time transfer offsets the PHC by (eL−iL)/2 — e.g. 1490 all-ingress with
  true 900/590 split = PHC ~295 ns off while every metric reads clean.
  ADVERSARIAL: single-observer tap/loopback schemes measure ONLY the sum
  (PHC-to-tap offset cancels iff summed) — split needs a second observable.
  Recipe: (1) SUM from tap on pdelay exchanges we answer (claimed t2/t3 vs
  tap hw times, A−B differencing drift-immune, ≥100 exchanges, minus 2×
  pigtail ~2.5 ns); (2) split PRIOR from countable MAC pipeline cycles
  (Verilator exact) + RTL8211E datasheet per-direction; (3) split PROOF =
  A_AVTPRX_TSD 0x6EC mean vs local-GM baseline while slaved to certified
  talker — sweep split holding sum, TSD moves 1:1 with X, converges 2 iters
  to ±25 ns. Constants live in yaml gptp: → dtsi kl,ptp-ingress/egress-ns →
  kl-eth probe writes 0x540/0x544; generated ptp4l cfg carries 0 BY
  CONSTRUCTION; S50milan seds DELETED + transition interlock (sed only if
  0x540 reads 0). Sanity: pdelay <200 ns symmetric — but pdelay proves SUM
  only, TSD proves split; claiming otherwise = the error class being fixed.
- J4 (M+M, last): AS_PATH depth-2 cap confirmed (count AND membership wrong
  ≥2 bridges). Fix: N=8 slots (GM + 7 bridges; 179 = medium ceiling not
  target; 448 flops). Slot 0 = GM NEVER stored twice (0x624/8 is it);
  slots 1-7 in csr via staging ABI A_ASP_LO/HI 0x7B8/BC + A_ASP_CMD 0x7C0
  (commit slot [10:8], publish count+gen bump = push edge; read {gen,count});
  count_r==0 → legacy [GM,parent] derivation (old daemons regress nothing).
  Builder: count arm, cdl 14+8*count max 80 (const_q already 66+ bytes ok);
  w_aspath_sig = {gm, parent, count, gen}. Daemon: linuxptp pmc has NO
  PATH_TRACE support (verified) → milan-statd AF_PACKET tap on 0x88F7
  Announce msgType 11, parse PathTrace TLV 0x0008; gptp2csr.sh keeps degrade
  (busybox can't parse frames; document oracle split + canned-Announce
  fixture). TB: 3-hop byte-exact, saturation cdl 80, gen-bump push, count-0
  legacy identity. Live: byte-compare GET_AS_PATH vs simultaneous tap
  PathTrace TLV (tap = oracle); multi-hop needs 2nd switch cabled.

---

## 2. STATE OF THE TREE

- Public repo `milan-fpga`, branch `main-push` (work lands here; merge to
  `main` only on user request — main and main-push both sit at 2eeb0267
  as of 08-08). Private repo `milan-tests-avb` (bench scripts, live suite
  tests/cert-recreate, driver work).
- VERSION ladder this campaign (all on main-push):
  - 0x002C — crossbars in-circuit BY SHAPE (builder-exported constants;
    CHMAP_CTRL[0] demoted to debug override).
  - 0x002D — CRF sink owns an appended lwSRP row (rows never renumber);
    listener Ready declared on CRF bind.
  - 0x002E — GET_STREAM_INFO flag laws, Milan Tables 5.9/5.11.
  - 0x002F — listener latency = SETPOINT ((6*2)+4 = 16 samples ≈ 167 us),
    prefill/recenter/convergence bands setpoint-relative.
  - 0x0030 — unbind reaches the parser (per-sink stream-table alias +
    eviction), bind-wipe fires MEDIA_UNLOCKED, odmap seeder hoist +
    51-check tdm8 aecp leg.
- Gates at land: builder ALL PASS, aecp 11 sims, csr, dp 7 legs, rxmon,
  pcm, yosys 49/49 + tap purity, behave 583 scenarios / 3458 steps.
- Coverage (line, 95% gate, both PASS): KL_avtp_rx_monitor 100.0%,
  KL_aaf_rx_depacketizer 97.4%, avtp_stream_parser 98.0%, KL_maap 100.0%.
- Shipping shape: 1x1x8 TDM8 (`endstation_ax7101_1x1_tdm8.yaml`,
  priority1 248). 8x8 is one SWEEP_CFG away. gen_aem_store CLOBBERS the
  tracked ROM — rerun the builder `--write-rtl` after using it.

---

## 3. GUARDRAILS (operational law — violations burned us on the bench)

1. **SET_STREAM_FORMAT before streaming on a STREAM_INPUT — THE BAN.**
   Formats must be EQUAL before CONNECT_RX. Never `--no-format-check`.
   The controller adapts whichever end is adjustable (07-27 directive:
   normally SET_STREAM_FORMAT the LISTENER to the talker's format; if our
   talker is the source and the sink refuses, set OUR talker instead).
   Unequal-format connects flap the stream and tear the peer's talker
   state. Recovery is quiesce-first: disconnect everything, settle, match
   formats, reconnect, verify with GET_COUNTERS twice.
2. **ATDECC authoritative, nothing manual.** Entity state changes only via
   ATDECC verbs driven by the user/controller. No raw CSR pokes to change
   state, no script re-imposition on boot. Reboot-lost state → persistence
   work, not scripts. (CSR reads for forensics are fine.)
3. **Never force the network GM.** The GM must recover automatically;
   priority1 = 248 (end station default). Never weaken CRF SR class
   (class A mandatory).
4. **Both boards same VERSION before comparative testing** — refuse
   otherwise.
5. **Wire proof before blaming the peer.** Check the standard clause first
   (PDFs at /home/alex/standards/). GET_COUNTERS decode = Table 7-153 WIRE
   order, never the RTL column order (a transposition once framed the
   innocent peer).
6. **Test ALL streams, even indices only carry traffic** (odd indices ride
   the uncabled secondary network) — plus CRF and cross-rebinds.
7. **Check all ten A_STRMW_CNT counters TWICE + GM identity + LWSRP_STATUS**
   in every verification pass (deltas, not snapshots).
8. **Always flash+verify + soak** every closed bitstream autonomously;
   after JTAG warm-reload TX timestamps are dead (ptp4l FAULTY, tu=1) —
   flash+power-cycle, don't JTAG-reload for gPTP work.
9. **Derive, never mirror a constant** (builder-exported constants, not
   copied `define`s). Shape is STATIC from elaboration params — stream
   counts are never a runtime poke.
10. **Repo hygiene:** one-line commits, no trailers, no AI attribution;
    decimal numbers in docs/prose except register addresses/values, bit
    masks, wire bytes; peer never named in public text; handovers local.
11. **Bench safety:** promisc on the switch port voids the RX shield;
    kernel shield mask is /32 not /24; VID 2 is the only SR VID
    (VID 0 floods unshaped); raw AVDECC tools must join 91:E0:F0:01:00:00
    and their cdl EXCLUDES the target id field.
12. **Never edit sweep.sh / build.sh while a chain runs them**; parallel
    sweeps on this box corrupt each other — one lane at a time.

---

## 4. LEARNINGS (this session's scar tissue)

- **Flapping had TWO roots**: my unequal-format connects (operator error →
  guardrail 1) AND a real RTL defect — unbind left the stream-table entry
  live, the departed stream's frames kept feeding the monitor, LATE events
  armed the 0x0028 push law into 1-per-second unsolicited GET_COUNTERS per
  registered controller, which Hive renders as input flapping. Fixed in
  0x0030. If flapping ever recurs on 0x0030+: capture the wire FIRST and
  look for cmd 0x8029 floods before touching connections.
- **Synthesis hazard class**: automatic temporaries assigned-then-used
  inside always_ff can silently diverge in synthesis while every simulator
  agrees (the audio-map key +1 shift: GET readback true, RAM write address
  shifted per-bitstream). House rule now: hoist to module-scope wires.
  Related lineage: 07-21 LUTRAM replica divergence.
- **t530 area explosion** was cfg drift — build.sh's plain cfg_ax7101 body
  had become the nic-perf RV64 SoC; only --sweep carried ship args. Fixed
  845a5436. Lesson: when area/timing jumps absurdly, diff the launch log's
  soc args FIRST (same lesson as the RV64 sweep drift memory).
- **LiteX CSR multi-word registers are MSW-first** (pcm ring base wrote
  LSW-first → DMA aimed nowhere). Layout moved too: length @0x128,
  enable @0x12C, done @0x130 read-only, loop @0x134, offset @0x138 —
  old tools write loop onto done. Trust csr.csv, not tool memory.
- **Tap-capture traps**: AAF is VLAN-tagged — BPF must match
  `ether[40:2]=0x8100` style offsets (+28 ProfiShark inband header);
  expired sudo silently yields a STALE pcap (run the whole extractor under
  `sudo -n` and check the file mtime); tone_thdn ZeroDivisionError = the
  channel is pure silence, i.e. the tone is NOT on that channel — a
  routing clue, not a script bug.
- **Bench hygiene**: pkill -f patterns match your own shell — collect PIDs
  to a file and kill from it; `git add -A` swept junk twice — stage
  explicit paths or -u; rsync to pw0 can silently no-op — scp + grep the
  destination; `pgrep` matches process NAME not cmdline — use -f.
- **THD+N of the emitted tone = -134.4 dB** (1 kHz at -15.1 dBFS, tap
  capture, 40k frames) — the digital chain is clean; remaining THD+N work
  is analog/peer-loop territory.
- **GM flap on 0x002D silicon**: zero unlocks, zero interruptions —
  free-wheel law (0x002B) proven live.
- **es-1.1 posture**: the board is a deferring end station now
  (priority1 248) — the suite's old board-as-GM announce expectations were
  rewritten to pdelay-only; gm-era scenario is @manual.
- **counters_valid**: sink 0 = 0xFFF (Milan Table 5.16 includes TV/TNV);
  sink 1 (CRF) legitimately 0xF3F — per-context, not a defect.

---

## 5. JOBS IN FLIGHT (check these first when picking up)

- **t532 sweep**: /home/alex/litex-milan/work/build_ax7101_{eppo,asl,eto}_t532
  (+ .launch.log next to each). A persistent monitor announces completion +
  WNS lines. On completion: pick best WNS ≥ 0, then
  `cd sw/litex && ./build.sh flash ax7101:build_ax7101_<dir>_t532`,
  verify boot, run the 0x002E/2F/30 proof list (section 1.1), then soak.
- **Traceability synthesis agent**: writing
  docs/reference/PROTOCOL_TRACEABILITY.md from the 18-agent workflow
  result (raw JSON kept at the workflow task output under the session
  scratchpad). DONE 08-08: committed 2eeb0267, pushed, merged to main. The 12
  confirmed findings are task #35 (none overlapped #31-#34).
- **pw1**: down; user restarting it. Until then la_avdecc/controller work
  runs from pw0 only (pw0 may run the controller; NEVER touch pw1's
  config remotely).

---

## 6. TESTS — how to run everything

### Verilator suites (repo tb/verilator/, plain `make` each)
aecp (11 sims incl sim_odmap_tdm8), milan_dp (7 legs: sim_main/nxn/prune/…),
csr, avtp_rxmon, pcm_playback, crossbar, acmp, acmp_lstn, lwsrp(+ctx),
tkdiag, servo, persist, hostplane, maap, txgrant (permanent starvation
guard). Check names containing FAIL/mismatch are NORMAL — grep for
`\[FAIL` or nonzero exit, not the word "fail".

### Coverage
`make coverage` in tb/verilator/avtp_rxmon and tb/verilator/maap
(gate = cov_gate.py 95 on KL_ modules, coverage_off pragmas honored).
The first summary line verilator_coverage prints is ALL-POINTS (toggle
included) — the gate's line-only number is the one that counts.

### Local behave (spec compliance, repo tests/)
`cd tests && behave` → expect 583 scenarios / 3458 steps, 0 failed.

### Live suite (private repo milan-tests-avb, tests/cert-recreate)
Runs on pw0: `AETS_IFACE=enp6s0 AECP_YAML_DIR=... PYTHONPATH=...
~/venv-cert/bin/python -m behave` (see aets-run notes on pw0;
run-remote.sh targets pw1 — off until user restarts it; the private
variant needs CERT_HOST env). Monitor with `pgrep -cf "m behave"`.

### Bench verbs (private repo avdecc_l2.py, run from pw0)
counters --target --descriptor --index / connect --talker-index /
set-format --format / add-audio-mappings --map SI:SC:CO[:CC] /
set-clock-source. Raw cdl EXCLUDES the target id. Validate every round
with la_avdecc + Hive (probe ABI trap: feature defines or SIGSEGV).

### Wire truth
Tap host amx-ubuntu-server, iface enxe8eb1b39111a, ProfiShark inband
header 28 bytes + FCS. AAF extractor /tmp/aaf_pcm.py (VLAN-aware BPF,
whole thing under sudo -n). THD+N: tone_thdn.py --rate --chans --chan
--f0 (numpy venv at the session scratchpad nv/; Hann window trap noted
in its header).

---

## 7. DEPLOYMENT

- Build: `cd sw/litex && TAG=<tag> ./build.sh --sweep ax7101` (3-directive
  place sweep eppo/asl/eto, 3x32 threads, 90 s stagger; --sweep is the
  ONLY path that historically carried ship args — now fixed, but verify
  vexii/soc args in the launch log on every new build class).
- Flash + verify: `./build.sh flash ax7101:<builddir>` (QSPI: bitstream@0
  + xz kernel in 16 MB). Always verify after flash; board net-up takes
  ~5.5 minutes. Rootfs rollback of record: rootfs.cpio.xz.flashed-0804.
  A rootfs missing /dev/null = silent kernel stall ~5 minutes in — check
  the cpio FIRST.
- Board access: ssh root@<board .1> -i /home/alex/.ssh/id_rsa
  -o UserKnownHostsFile=/dev/null (hostkey rotates per flash). File
  transfer to pw0 via dropbear scp.
- Vivado: 2026.1; Artix under /home/alex/Xilinx. 3x32-thread rule; keep
  best WNS of the 3 seeds.
- Yosys desk gate: tb/verilator/../..(sw/builder) full gate = 49 tops +
  tap purity — run before any flash-bound landing.
- Single-hart budget: the softcore starves under load (shell loops froze
  softirq ~570 ms; PipeWire graph → ptp4l starved). Keep service load
  shed during gPTP-sensitive tests; aplay 2048-frame periods.

## 8. WHERE THINGS LIVE

- Standards PDFs: /home/alex/standards/ (Milan v1.2, 1722.1-2021, 1722,
  802.1Q/AS). Always cite the clause before calling a behavior a defect.
- AX7101 reference (schematic, XDCs): /home/alex/refs/AX7101.
- Buildroot: srcs/buildroot + br-milan-output; RV32 tree
  /home/alex/br-milan-rv32.
- Music proof track: /home/alex/07_electric_wizard.flac; replay recipe
  pw0 ~/MUSIC_REPULL.md.
- Session memory index: ~/.claude/projects/...milan-fpga/memory/MEMORY.md
  (the long-term law book — read it before undoing anything odd).
