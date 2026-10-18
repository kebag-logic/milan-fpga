[A649]

# Publish thisClock and {thisClock} from reset release and whenever no live peer is elected

Refs #82

## Problem

Until a first gPTP peer appeared, the engine published grandmaster 0 and an empty path, and
GET_AVB_INFO and GET_AS_PATH served the same zeros. IEEE 802.1AS-2020 10.3.13.2.4 b) makes an
instance with no port vector its own grandmaster, and i) then sets pathTrace to {thisClock}.

## Change

- thisClock is ROM data. The generator writes its high and low halves at the two fixed words
  1022 and 1023. The engine reads them from the same `UCODE_HEX_P` image at configuration.
- Reset loads the self tuple into the publication bank: grandmaster thisClock, count 1, zero
  tail. Parent identity keeps its reset value. The engine commits it once, on the first clock
  edge after release, before any handler can run. Cold start and warm reset behave alike. The
  init leg installs S_CID from the engine's copy, so the ROM holds thisClock once.
- A reset leaves no port vector (10.3.12, BEGIN). The retained best record gets reset-backed
  validity: until written it reads as the worst vector, so only a newly received Announce
  competes after a reset. Reset also clears the raw selected path.
- A port that stops being asCapable stops contributing its vector (10.3.12, DISABLED). Any
  flags write that clears asCapable expires the Announce receipt watch at once. Its leg drops an
  elected peer and publishes thisClock and {thisClock}, without touching PHC control, so the
  slew level and rate still hold across capability loss. Announce silence on a capable port
  still makes this plane master after 3 s. Both paths end in one shared self publication.
- gmPresent (flags bit 0) follows 10.3.13.2.4 g): it is TRUE when gmPriority's priority1 is below
  255. gmPriority is never worse than thisClock's own vector, so a plane whose priority1 is below
  255 always publishes gmPresent: at reset, after either departure and as master. Bit 32 of ROM
  word 1022 marks that capability, and the engine ORs it into published bit 0. The microcode's
  own bit 0 keeps one meaning, "a peer is elected", so mastership no longer sets it. With
  priority1 255, every self publication carries gmPresent FALSE.
- The ROM uses 1,013 of 1,024 words (was 1,016); the image digest changes.

## Interface

Parameter and port declarations are identical to the parent's current pin once comments are
stripped; only the `pub_path_count_o` comment changed. The commit is still a single-cycle pulse
over stable outputs. What a consumer sees differently:

- From release, GM is thisClock, the path {thisClock}, and the flags word is `0x1` (gmPresent).
  The boot commit is a GM edge from 0, so the parent's shadow pulses its discontinuity output
  and advances its path generation once.
- After asCapable falls under an elected peer, a commit within about 1 ms names thisClock with
  {thisClock}. Its flags word is `0x1`: sync-ok, mastership and asCapable are clear.
- The parent reads flags bits 3 and 2 only; their behaviour is unchanged.
- The ROM image now carries thisClock and its capability mark; an image from an older generator
  would not.

## Tests

Engine suite: 1,642 checks per image (round 2: 1,634), three images. A fourth pass runs the
boot, mastership and capability-loss phases from a priority1-255 image: 46 checks.

| scenario | checks |
|---|---|
| cold release to the first timer beat | every cycle names thisClock with {thisClock} and gmPresent; one commit, on the first edge after release, carrying them with no other flag |
| a peer wins | its commit names its grandmaster and its three-entry path |
| warm reset while that peer is elected | one commit in 2 ms, on the first edge, naming thisClock with a zero tail and gmPresent alone |
| after that reset | a peer worse than this plane leaves thisClock; a live peer worse than the absent winner wins with its own path |
| Announce silence, Pdelay answering | the mastership commit names thisClock with {thisClock} and gmPresent |
| Pdelay loss, Announces and Syncs continuing | sync-ok is set at the fall; thisClock with {thisClock} within 2 ms, flags gmPresent alone; incapable-port Announces elect nothing |
| capability returns, no Announce | mastership within one receipt interval, naming thisClock with {thisClock} and gmPresent; then a live peer worse than the dropped one wins |
| the whole run | every commit naming thisClock carries {thisClock} |
| priority1 255 | the same boot, mastership and capability-loss checks with gmPresent clear in every self publication |

Twenty-five planted controls cover #82; each fails every check it names, and the arm is 58/58
(round 2: 52/52). A check of the priority1-255 pass can only be satisfied by that pass. Against the
round-2 head the new harness fails exactly the four new gmPresent checks, plus two in the
priority1-255 pass; against the base engine, 20 and 13.

Repository gates are rc 0 at base and head: contract, lint, docs, microCPU 768, parser 337 +
9/9, engine as above, gaskets 81 + 5/5, field-input suite 288 + 4/4, bench tag.

## Parent consumer gates (dev `e9cbb676`)

The head column uses a local, never-pushed parent branch on dev with two commits: the gitlink at
this head with the eight gPTP docs re-pointed and the new ROM-ledger row, and the milan_dp test
update below.

- Elaboration, ratcheted lint, port contracts, wire accountability, gPTP docs, ROM ledger and
  the builder clock contract pass.
- The C++ and Python idiom ratchets and the builder suite pass (round 4, below).
- `gptp_shadow` 309, lifecycle, and its mutant arm (controls 9, failures 0) pass.
- `gptp_tables` 36 and its mutant arm (controls 26, failures 0) pass.
- `gptp_txts` 85 + 6/6, `gptp_plane` 29 + 62 + 8, the field campaign 677/0, and `gmstep` 190 pass.
- The plane-on `milan_dp` legs `gptp` and `gptp-lat` fail 3 of 182 as dev has them. Those checks
  assert the boot state this PR removes: GM zero before any peer, and a compatibility mask that
  includes the discontinuity holdover the boot GM edge arms. Expecting thisClock and masking
  that bit, both legs are 182/182 at head; the updated check fails at base. The gmPresent change
  adds no failure there. The parent's pin bump needs this change beside its docs and ledger edits.
- Not run: the nightly physical gPTP job (about 46 minutes of simulation). By reading, its
  check that a mid-run reset clears the public GM needs the same update. Also not run: the full
  `milan_dp` sweep, whose other cases elaborate without the plane, and the media-clock suites.

## Known limits

- Unchanged by this PR: 10.3.13.2.4 a) also ages a vector on sync receipt timeout when
  gmPresent; that timeout still only clears sync-ok.
- Unchanged by this PR: the parent identity is 0 after reset and thisClock after mastership or
  a drop.
- With priority1 255 (not the default), an elected peer whose own priority1 is 255 still
  publishes gmPresent, as at base: adoption sets bit 0 for any elected peer.

## Round 2

Both round-1 reviews were negative. Each finding and its resolution:

- R651-1-F1, R650-1-F1, cold start: the 1.2 s zero window is gone. thisClock comes from the
  image at configuration, reset loads the self tuple, and the first edge commits it. The cold
  interval is graded cycle by cycle, with planted controls.
- R651-1-F2, capability loss: an asCapable fall now drops an elected peer at once, with no PHC
  transition. Both departures are tested, each with planted controls.
- R651-1-F3, R650-1-F2, warm reset: the retained best record and raw path no longer survive a
  reset; the reviewers' worse-live-peer scenario is graded. The phase-35 comment is rewritten.
- R650-1-F3: one commit per reset and the warm-reset zero tail are graded, including the
  reviewer's never-retiring commit control.
- R651-1-F4: both parent mutant arms run to completion against a locally committed gitlink.
- R650-1-F4: round-2 receipts are published with an index that matches the files exactly.
- R650-1-R1: the interface wording above.
- R650-1-S1 and S2: the boot-commit guards and the zero-GM sentinel are gone.

## Round 3

- R650-2-F1: the capability fall is now taken while sync-ok is set, and the drop commit's whole
  flags word is graded. A port that regains asCapable with no further Announces must commit
  mastership with thisClock and {thisClock} within one receipt interval; it does so 1.0 s after
  the rise. The reviewer's two controls, keeping the flags word at the drop and not re-arming the
  receipt watch, are planted with their exact text and each fails its named checks.
- R650-2-F2: made conformant rather than reworded. Every self publication sets gmPresent, at
  reset, after the asCapable drop and after the Announce-silence departure, and each is graded
  with planted controls in both the default and the priority1-255 images. The "Known limits"
  sentence and the integration guide are corrected.
- R650-2-R1: the RTL comment carries the exact text.
- R651-2-S1: the ROM-layout receipt helper now completes for the base generator.
- Not taken, as suggestions outside this assignment: R650-2-S1, R650-2-S2 and R651-2-S2.

## Round 4

Both round-3 reviews were positive. The parent consumer list failed two of its code-quality
ratchets, which also count this repository's sources. All three counts came from this PR's test
sources, and no ratchet is raised:

- `tb/verilator/engine/sim_main.cpp`: `run_suite` had grown to 102 lines with the priority1-255
  pass. It now picks `run_the_self_publication_phases` (the fourth pass) or `run_every_phase`
  (every phase, in file order) and prints the tally line once.
- `tb/verilator/engine/mutants.py`: `main` was 104 lines, and its nested `failing` had no
  docstring.
  - `run_mutant` now plants and grades one control.
  - `named_verdict` holds the #75 and #82 named-check narrowing.
  - `_named_failure` replaces `failing` and has a docstring.
  - `main` keeps the positive control and the tally.
- At this head the C++ gate reads long function 0 of 0. The Python gate reads long function 9 of 9
  and undocumented public function 0 of 0.

Behaviour is unchanged:

- The engine suite's output matches the round-3 head's except for one build-timing line: 1,642
  checks in each of three images and 46 in the fourth pass, all passing.
- The mutation arm's 18 shard logs are byte-identical: 58 of 58 caught, with the same 71 named
  failure lines.
- One meta-run drives every branch of the moved verdict code: a pattern that no longer matches, a
  refused image, a failed build, a survivor, a missed name in each narrowing, and both kinds of
  catch. It prints the same output at both heads.
- Inverting the new dispatch fails 54 checks in the priority1-255 pass. Dropping one phase call is
  not caught by the suite itself, but the check count then drops from 1,642 to 1,629. That count is
  the comparison above.

The full parent consumer list passes on a committed local parent snapshot of dev `e9cbb676` with
this head as the gitlink. That list is all 11 commands of the round-4 template, including both
idiom gates and the builder suite. The builder suite reports one arm not run, as it did at the
round-3 head: its calibration gate needs a board build tree.

R650-3-R1: `docs/INTEGRATION.md` now reads "Flags carry gmPresent alone, or nothing with
priority1 255." R650-3-S1 to S5 are suggestions outside this assignment and are not taken.

Why "Refs" and not "Closes": the plane-on parent checks above assert the old boot zeros and
must change with the parent's pin bump before #82's last done condition holds.
