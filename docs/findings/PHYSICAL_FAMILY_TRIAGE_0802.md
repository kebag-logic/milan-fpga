<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# The first silicon run of the physical family — both FAILs triaged (2026-08-02)

Run `ax-phys-a` (88 records: 29 PASS / 2 FAIL / 45 SKIP / 10 INFO / 2
CONFORMANT-REFUSAL) was the first time the powerstrip-driven `physical` area
(commits `6dcc3fca` / `9528d90`) ran on silicon. **Both power cycles executed
and the bench recovered**, so the family itself works. This page triages the
two FAILs clause-first. One was a wrong assertion; one is a real open gap that
the assertion described correctly and graded wrongly.

Context: [TORTURE_CAMPAIGN.md](../testing/TORTURE_CAMPAIGN.md) §7.1 (the
family), [BENCH_TOPOLOGY.md](BENCH_TOPOLOGY.md) (what is cabled to what),
[MILAN_COMPLIANCE_GAPS.md](../MILAN_COMPLIANCE_GAPS.md) (the persistence
column).

> **HOW MUCH OF THIS RUN IS STILL RUNNABLE (2026-08-13).** The triage stands as
> reasoning; what changed is which assertions can reach an answer. This
> repository's AECP/AEM engine was deleted and the pinned `protocol-processor`
> submodule's AECP µCPU took over: it **answers `READ_DESCRIPTOR`** — `SUCCESS`
> with the configuration index and the descriptor, `NO_SUCH_DESCRIPTOR` on a
> locate miss, `BAD_ARGUMENTS` on a bad configuration index — and returns a
> conformant `NOT_IMPLEMENTED` echo to every other AECP command. It is not
> silent, and it is not an implementation of anything else.
>
> For this page that means: every assertion built on `GET_COUNTERS` (all of
> §1's replacement set) and every one built on `GET_STREAM_FORMAT` /
> `SET_STREAM_FORMAT` (§2's companions, and the two CONFORMANT-REFUSALs in §3)
> now gets a well-formed `NOT_IMPLEMENTED` instead of the status they were
> written against. A runner must grade that as **not implemented**, never as a
> refusal and never as coverage. Descriptor reads are the one thing that came
> back, and only in the narrow sense §2 spells out. Persistence did not come
> back at all.

## Contents

- **[1. FAIL 1 — GPTP_GM_CHANGED: the assertion was wrong](#1-fail-1--gptp_gm_changed-the-assertion-was-wrong)** — the assertion encoded a follower bench but the AX is the domain GM (priority1 238, verified), so the conformant delta is exactly zero; four replacement assertions, with LINK_UP demoted to INFO because the inline tap masks link events.
- **[2. FAIL 2 — the format did not persist: the clause is real, the verdict was not](#2-fail-2--the-format-did-not-persist-the-clause-is-real-the-verdict-was-not)** — Milan 5.3.8.1's unconditional shall is a real open gap: `/proc/mtd` is empty so nothing on this build can persist; the probe-decided KNOWN-PENDING verdict scheme and two companion records replace the bare FAIL.
- **[3. What the run could not see, and why](#3-what-the-run-could-not-see-and-why)** — the 45 SKIPs decomposed: the listener-index-8 bind failure and its licence cascade (32+12 records), plus the 25 s-vs-60 s ssh timeout constant that silently nulled every board reading.

## 1. FAIL 1 — `GPTP_GM_CHANGED`: the assertion was wrong

**What was filed.** `phys.switch-cycle.gm-partition` /
`counters.avb_interface.gptp-gm-changed-advances`, detail
`{"post": 2, "pre": 2, "why": "GPTP_GM_CHANGED never advanced across a
partition and re-join — the device slept through two real elections"}`.

**The clause.** IEEE 1722.1-2021 Table 7-153, `AVB_INTERFACE` counters
block, offset 20:

> `GPTP_GM_CHANGED` — gPTP grandmaster change count.

Milan v1.2 says the same in its `AVB_INTERFACE` counter table:

> `GPTP_GM_CHANGED` — Number of gPTP GM changes, since boot.

It counts **changes of the grandmaster**, not link events, not partitions,
not elections that re-confirm the incumbent.

**The topology, verified rather than assumed.**

| fact | evidence |
|---|---|
| the AX holds `priority1` 238 | live read of the deployed `/etc/gptp.cfg` on the board: `priority1  238` |
| the bridge advertises `priority1` 246 | BENCH_TOPOLOGY §1 (tap-read: `246/cc248/acc0x20`) |
| the AX **is** the grandmaster | both entities' ADPDU `gptp_grandmaster_id` = `020000fffe000001` = the AX's own entity id, in *both* pre-snapshots and after both cycles |
| everything hangs off the one switch | the pre-cycle probe went `dark: true` the moment OUT4 was cut — the controller host, the AX and the peer are all inside the partition |
| the AX did **not** restart | it was re-reachable **22.3 s** after power returned to the switch; a genuine cold boot on this board took **108.2 s** in the same run |

So the AX was GM before the cut, GM of its island of one during it (lower
`priority1` wins, and it is alone anyway), and GM again on the re-join. **Its
own `grandmasterIdentity` never changed, so the conformant delta is exactly
zero.** The gateware implemented precisely the clause —
`KL_aecp_response_builder.sv`: `if (gptp_gm_id_i != gm_prev_r) cnt_gmchg_r <=
cnt_gmchg_r + 32'd1`. That module is deleted, and `GET_COUNTERS` was not
reimplemented, so the counter has neither a source nor a way out: the argument
above is still the right reading of the clause, but it can no longer be
*measured* over AECP on this build.

**Verdict: the assertion was misapplied.** It encoded a bench where the DUT
is a follower, and the bench is the opposite.

**A second observation that survives the triage.** `LINK_UP` read 1 before and
1 after the switch cycle, with the reboot ruled out above. That is *also* not
a defect: **tap1 is an inline regenerating tap on the AX↔switch link**
(BENCH_TOPOLOGY §0), and such a tap holds the board-side PHY up while the
switch side is dark. The DUT could not have seen a link event to count.
Asserting "the DUT noticed the link event" would have been the same mistake
one layer down, so `LINK_UP`/`LINK_DOWN` are now recorded as an **INFO
datum**, never a verdict.

**The fix (both repos).**

| assertion | grading |
|---|---|
| `counters.avb_interface.gptp-gm-continuity` *(new, SHALL)* | applies when the DUT **was** the domain GM: PASS iff the ADPDU `gptp_grandmaster_id` is unchanged **and** the delta is 0. A counter that moves with an unchanged id is the torn-latch / partial-id-re-read class; a changed id with `priority1` untouched means it lost an election it held |
| `counters.avb_interface.gptp-gm-changed-advances` *(narrowed)* | applies only when the DUT **was following a remote GM**: it really did lose its grandmaster, so a small bounded advance is owed and a frozen counter is the original FAIL, correctly aimed |
| `counters.avb_interface.peer-gptp-gm-changed-advances` *(new, SHALL)* | the other end station is the side that *does* lose its GM when a permanent-GM DUT is cut off, so that is where the election is observable. Attempted every run; a reference device that does not answer `GET_COUNTERS` SKIPs naming that, never a verdict about the DUT |
| `counters.avb_interface.link-event-observed` *(new, INFO)* | `LINK_UP`/`LINK_DOWN` deltas as context for the above — the inline tap makes a zero delta a cabling fact |

Whichever branch does not apply SKIPs **naming why**, so the step still
accounts for its whole contract and neither direction can quietly vanish.

---

## 2. FAIL 2 — the format did not persist: the clause is real, the verdict was not

**What was filed.** `phys.dut-cycle.power-cycle` /
`state.restored-after-power-cycle`, detail `differs: ["stream_input[7]"]`,
pre `0205022001006000`, post `0205022002006000` — AAF
`channels_per_frame` 4 before the cycle, **8** (the elaborated default) after
it.

**The clause.** Milan v1.2 **5.3.8.1 STREAM_INPUT dynamic state / Format**,
verbatim and complete:

> A Stream Input shall always be using a format that is one of the supported
> formats described by the formats list. […]
> **The current format shall be saved in a non-volatile memory and restored
> after a power cycle.**

It is an unconditional **shall**, and it is not alone: 5.3.7.1 says it for a
Stream Output's format, 5.3.8.2 for the bound state, 5.3.8.3 for the binding
parameters, 5.3.10.1/5.3.9.1 for the input/output channel mappings, 5.3.7.6
for the presentation time offset, plus the sampling rate, the clock source and
the user-name list. **Milan does require it. This is a real open defect.**

There is no conflict with the standing *shape-is-static-from-elaboration*
directive: that directive governs stream **counts** and audio ports. The
per-stream **current format** is dynamic state that 5.3.8 explicitly makes
settable and 5.3.8.1 explicitly makes persistent.

**Why it cannot pass today, measured not assumed.** On the DUT:

```
# cat /proc/mtd
dev:    size   erasesize  name
# mount
rootfs on / type rootfs (rw)
```

`/proc/mtd` lists a header and **nothing else** — the DTB carries no
journal/user MTD partition (task #57) and the rootfs is a RAM initramfs.
**Nothing on this build can persist anything.** The fabric side is further
along than the board side: `KL_persist_journal` exists and the 0x7B8
journal-ingest group is wired for the bound state, but it has no store behind
it.

**What must persist, and where it would have to live** (this is the
task-worthy note):

- **What:** per `STREAM_INPUT`/`STREAM_OUTPUT` the current format
  (5.3.8.1/5.3.7.1); the bound state and binding parameters
  (5.3.8.2/5.3.8.3); the input and output channel mappings
  (5.3.10.1/5.3.9.1); the presentation time offset (5.3.7.6); the sampling
  rate; the clock source; the user-name list.
- **Where:** a writable MTD partition declared in the DUT's DTB (the 16 MB
  N25Q128 has the room — the "full" manifest map already carves a 4 MiB
  bitstream slot), plus a restore-on-boot step that replays it into the AEM
  dynamic state before the entity starts advertising. Neither exists today, and
  since 2026-08-13 the target of that replay does not exist either: there is no
  AEM dynamic state to write into. `KL_persist_journal` is deleted, the setters
  that would have moved the state (`SET_STREAM_FORMAT`, the audio-map commands,
  `SET_MAX_TRANSIT_TIME`, `SET_CLOCK_SOURCE`) are unimplemented, and the model
  a controller reads is a static descriptor image in DRAM that nothing writes
  at runtime. The gap got deeper, not shallower.

**The fix.** The assertion is **never deleted** — the clause is a SHALL. What
changes is the verdict it may return, decided by a **probe, not a guess**
(`/proc/mtd` over `--board-cmd`, overridable with the new `--nvm
present|absent`):

| situation | verdict |
|---|---|
| nothing differs | `PASS` — a device that keeps it, passes, whatever the probe says |
| differs, store **present** | `FAIL` — the clause is violated by something that could have held it |
| differs, store **absent** | `KNOWN-PENDING` — naming the clause, what must persist and where it would live. It does not fail the run (a red that can never go green trains the reader to skip past it), and it goes live as a `FAIL` untouched the day the store lands |
| differs, store **unknown** | `SKIP` naming `--nvm` |

Two records now sit beside it so the cycle is never left with no verdict on
its own state:

- `state.self-consistent-after-power-cycle` *(new, SHALL — gradable with no
  store at all)*: every descriptor that answered `GET_STREAM_FORMAT` before
  the cycle answers again after it, with a well-formed 8-octet format. That
  is the half of 5.3.8.1 ("shall always be using a format…", + 1722.1-2021
  7.4.10) a no-store build still owes. **Not gradable as written since
  2026-08-13**: `GET_STREAM_FORMAT` returns a `NOT_IMPLEMENTED` echo. And do
  not substitute `READ_DESCRIPTOR` for it — the STREAM_INPUT descriptor's
  `current_format` comes from a static image in DRAM that no runtime writer
  touches, so it reads identically before and after a power cycle by
  construction. Agreement there proves the image is loaded, nothing about
  dynamic state.
- `state.format-after-power-cycle` *(new, INFO)*: what each descriptor
  actually read back, pre vs post — the datum that makes the gap measurable
  before it is fixed.

Membership against the entity's *supported* formats list is deliberately
**not** asserted: the runner's `Device.formats` is the set the campaign uses,
not the entity's declared list, and grading against it would be the same kind
of over-claim this triage removed from the GM story.

---

## 3. What the run could not see, and why

45 of the 88 records were SKIPs, and they concentrate in two causes.

| # | what skipped | why | structural or fixable |
|---|---|---|---|
| 32 | the two proof pairs' whole post-bind contract (16 each: `acmp.status`, `adp.alive`, four counter-mask/invariant checks, the six `stream_input` growth checks, `wire.matches-declared-format`, `xside.errors-static-all-sides`, `instrument.test-machine-lossless`, `counters.stream_input.reset-on-not-bound-to-bound`) | **`acmp.status`: "no ACMP response"** from the peer at listener index 8 — everything after it SKIPs "the bind did not succeed, so the post-bind assertions have no subject" | **fixable, and the highest-value one.** The proof pair picks `lis[-1]` = 8, the last of the primaries `(0, 2, 4, 6, 8)`. Index 8 is the one primary the peer did not answer on; the earlier campaigns' working binds used lower indices. Either index 8 is not actually served (probe it and shrink `listener_index_set`) or it needs the lazy-TA arming the 07-29 session hit |
| 12 | the two `start-if-needed` steps' licence-conditional set (`stream.starts-on-bind-alone`, `frames-tx/rx-advances`, and the three `xside` corroborations, ×2) | `LWSRP_STATUS` bit 8 (stream gate) SHUT → Milan 5.3.7.3's licence is a conjunction and was never completed, because there was no bind to complete it | consequence of the same bind failure — **fixable with it** |
| 1 | `boot.shield-posture-restored` | the SKIP said *"no board path (`--board-cmd`)"* — **and the launcher supplied `--board-cmd`** | **fixable, and now fixed.** `Runner._board` bounded its ssh at **25 s** while `Csr.read` had already been raised to **60 s** for exactly this bench (ssh-via-pw0 into a loaded single-hart softcore). Every board reading of the run silently came back `None`: the `uptime` snapshots were `null`, so `entity.survived-without-reboot` fell from uptime evidence to the far weaker counter-monotonicity fallback on the one step whose job is to prove the DUT did not restart. A constant that disagreed with its twin — the standing *derive, never mirror* rule. `_board` is now 60 s, and a failed read says *"`--board-cmd` is configured but reading X returned nothing"* instead of blaming a flag that is already there |

Nothing in the run SKIPped for a **structural** reason (no CSR path, no tap
host, no runner op): the CSR path was live all run — the licence word, the
`VERSION` word (`0x10021`, unchanged across the cold boot) and `CLKV_STAT`
(tu = 0 after both cycles) all read cleanly.

Also worth keeping: the two `CONFORMANT-REFUSAL`s are the talker refusing
`SET_STREAM_FORMAT` with status 7, which is the documented correct behaviour
per FR-STR-03 — not a defect, and correctly not graded as one. On the current
gateware the same probe gets a different answer: `SET_STREAM_FORMAT` is
unimplemented, so the µCPU replies `NOT_IMPLEMENTED`. That is still a
well-formed response and still not a defect, but it is a **different verdict
class** — a command with no implementation behind it, not a talker exercising
a documented refusal. Do not let the two collapse into one row.
