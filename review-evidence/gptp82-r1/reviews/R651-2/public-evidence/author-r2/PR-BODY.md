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
  tail. Parent identity and flags keep their reset values. The engine commits it once, on the
  first clock edge after release, before any handler can run. Cold start and warm reset behave
  alike. The init leg installs S_CID from the engine's copy, so the ROM holds thisClock once.
- A reset leaves no port vector (10.3.12, BEGIN). The retained best record gets reset-backed
  validity: until written it reads as the worst vector, so only a newly received Announce
  competes after a reset. Reset also clears the raw selected path.
- A port that stops being asCapable stops contributing its vector (10.3.12, DISABLED). Any
  flags write that clears asCapable expires the Announce receipt watch at once. Its leg drops an
  elected peer and publishes thisClock and {thisClock}, without touching PHC control, so the
  slew level and rate still hold across capability loss. Announce silence on a capable port
  still makes this plane master after 3 s. Both paths end in one shared self publication.
- The ROM uses 1,013 of 1,024 words (was 1,016); the image digest changes.

## Interface

Parameter and port declarations are identical to the parent's current pin once comments are
stripped; only the `pub_path_count_o` comment changed. The commit is still a single-cycle pulse
over stable outputs. What a consumer sees differently:

- From release, GM is thisClock and the path {thisClock}. The boot commit is a GM edge from 0,
  so the parent's shadow pulses its discontinuity output and advances its path generation once.
- After asCapable falls under an elected peer, a commit within about 1 ms names thisClock and
  clears the presence and sync flags.
- The ROM image now carries thisClock; an image from an older generator would not.

## Tests

Engine suite: 1,634 checks per image (round 1: 1,623), three images.

| scenario | checks |
|---|---|
| cold release to the first timer beat | every cycle names thisClock with {thisClock}; one commit, on the first edge after release, carrying both |
| a peer wins | its commit names its grandmaster and its three-entry path |
| warm reset while that peer is elected | one commit in 2 ms, on the first edge, naming thisClock with a zero tail |
| after that reset | a peer worse than this plane leaves thisClock; a live peer worse than the absent winner wins with its own path |
| Announce silence, Pdelay answering | the mastership commit names thisClock with {thisClock} |
| Pdelay loss, Announces continuing | thisClock with {thisClock} within 2 ms of the fall; incapable-port Announces elect nothing; once capable, a live peer worse than the dropped one wins |
| the whole run | every commit naming thisClock carries {thisClock} |

Nineteen planted controls each fail every check they name; the arm is 52/52 (round 1: 39/39).
Against the base engine the new harness fails 17 checks; against the round-1 head, 11: the cold
interval, post-reset selection and capability loss. The reviewers' cold, gone and warm probes,
re-run verbatim, fail at the round-1 head as published and pass at this head.

Repository gates are rc 0 at base and head: contract, lint, docs, microCPU 768, parser 337 +
9/9, engine as above, gaskets 81 + 5/5, field-input suite 288 + 4/4, bench tag.

## Parent consumer gates (dev `e9cbb676`)

The head column uses a local, never-pushed parent commit with the gitlink at this head, the
eight gPTP docs re-pointed and the new ROM-ledger row.

- Elaboration, ratcheted lint, port contracts, wire accountability, gPTP docs, ROM ledger and
  the builder clock contract pass.
- `gptp_shadow` 309, lifecycle, and its mutant arm (controls 9, failures 0) pass.
- `gptp_tables` 36 and its mutant arm (controls 26, failures 0) pass.
- `gptp_txts` 85 + 6/6, `gptp_plane` 29 + 62 + 8, the field campaign 677/0, and `gmstep` 190 pass.
- The plane-on `milan_dp` legs `gptp` and `gptp-lat` fail 3 of 182 as dev has them. Those checks
  assert the boot state this PR removes: GM zero before any peer, and a compatibility mask that
  includes the discontinuity holdover the boot GM edge arms. Expecting thisClock and masking
  that bit, both legs are 182/182 at head; the updated check fails at base. The parent's pin
  bump needs this change beside its docs and ledger edits.
- Not run: the nightly physical gPTP job (about 46 minutes of simulation). By reading, its
  check that a mid-run reset clears the public GM needs the same update. Also not run: the full
  `milan_dp` sweep, whose other cases elaborate without the plane, and the media-clock suites.

## Known limits, unchanged by this PR

- 10.3.13.2.4 a) also ages a vector on sync receipt timeout when gmPresent; that timeout still
  only clears sync-ok.
- gm_present stays 0 at boot and after a dropped peer.
- The parent identity is 0 after reset and thisClock after mastership or a drop.

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

Why "Refs" and not "Closes": the plane-on parent checks above assert the old boot zeros and
must change with the parent's pin bump before #82's last done condition holds.
