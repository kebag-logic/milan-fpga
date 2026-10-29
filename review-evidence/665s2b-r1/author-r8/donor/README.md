# Donor draft for lwSRP: the reclaim walk and the validation pass's clearing (#665 S2b round 8, item 2c)

Not pushed and not a PR. `lwsrp-reclaim-and-parse.patch` is `git format-patch` of two commits on the parent's pin:

- base: lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348` (the parent's gitlink and `ctrl_arms.LWSRP_REV`, "Merge pull request #18");
- `a9db353`: the source change; `fc06e7c0f8f7270d9c76b6f8daa666bc82d448dd`: its tests. Squash them for the review if the repository prefers one commit.
- In a scratch clone; nothing was pushed.

## What it changes

| File | Change | Reason |
|---|---|---|
| `src/core/mrp_mad.c` | `struct mrp_port_state` gains `reclaim_due`. `attr_reclaimable()` states Table 10-3 note 11's condition once (Registrar MT; Applicant VO, AO or QO), and `mrp_reclaim` uses it. `note_states()` sets the mark when an attribute is created, after every event `deliver_event_changed` applies, and after the leave timer's Registrar event. `mrp_reclaim` returns 0 without walking while the mark is clear, and clears it when it walks | Every state assignment (`appl_event`, `reg_event`, creation) passes one of those three points, so a port without the mark holds no reclaimable attribute. `mrp_reclaim` frees the same attributes at the same calls as before. The parent's SRP adapter calls it on every poll after a receive, and each call walked the whole list: 0.76 ms of the worst 8x8 SRP window at round 7, nearly all data-cache refills |
| same | A rollback in `deliver_event_changed` takes no mark | It restores states that were marked when they were reached; no walk can run between |
| `src/core/mrp_pdu.c` | `parse_pass` clears a decoded value only on the delivering pass | The validation pass delivers nothing, and every `decode_attr` writes its output without reading it, so its 64-byte clearing per attribute bought nothing. A delivered value is still zero past its decoded bytes |
| `tests/unit/review_test.c` | `registration_ended_by_the_leave_timer_is_reclaimed_after_an_earlier_walk`; `refused_replacement_leaves_its_new_instance_reclaimable` | The two paths no existing test reached: the leave timer's change after a walk, and a new instance a refused replacement leaves undeclared |
| `tests/unit/receive_test.c` | `delivered_value_is_zero_past_its_decoded_bytes`: a Listener delivered after a longer Talker value in the same PDU is zero from byte 9 on | The clearing the delivering pass keeps |

## Evidence, on this host

lwSRP's suite (`doc/tester.md` "Run the suites": configure, build, `ctest`, `unit_tests`). This host has no cgreen package, so cgreen 1.6.5 was built from its release tag in scratch:

- at the base: 26,658 passes, rc 0 (`receipts/donor/lwsrp-suite-base.log`);
- with the donor: 26,690 passes, rc 0 (`receipts/donor/lwsrp-suite-donor4.log`);
- six planted defects, each caught by the test named (`scripts/lwsrp_plants.py`, `receipts/donor/lwsrp-plants.txt`): the leave timer's mark dropped, the event's mark dropped, the creation's mark dropped, the walk always skipped, a Leaving Observer taken as reclaimable, and the delivering pass left uncleared.

- `SHLAN_LIBRARY=<build>/libshlan.so behave`: 1 feature, 3 scenarios, 10 steps passed, rc 0, at the base and with the donor (`receipts/donor/lwsrp-behave-*.log`).

Not run: the documentation checks CONTRIBUTING names (`doc/tools/README.md`); the donor changes no document.

## The parent's side

The parent's SRP adapter needs no source change for it: its `reclaim` flag still saves the call, and `mrp_reclaim`'s contract is unchanged.
Dropping that flag to call `mrp_reclaim` on every poll would be a simplification, not a saving, and would remove the adapter's own tests and planted defect, so it is not proposed.
Moving the pin is two lines in one commit, after the donor merges upstream (push the submodule before the superproject):

- the gitlink `third_party/lwSRP` (`receipts/variants/parent-with-donors-gitlinks.patch` carries it with the TSN stack's);
- `LWSRP_REV` and its comment in `sw/firmware/ctrl/test/ctrl_arms.py` (`receipts/variants/parent-with-lwsrp-donor-pin.patch`), which the image builder and the firmware self-test read.
