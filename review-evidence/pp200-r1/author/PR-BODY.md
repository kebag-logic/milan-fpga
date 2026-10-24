[A668]

Closes #200

GET_AVB_INFO with a descriptor_type other than AVB_INTERFACE now answers NOT_SUPPORTED (IEEE 1722.1-2021 Table 7-141 status 11) with the command echoed at its own length. Since #182 (#177) it answered NOT_IMPLEMENTED (status 1). An AVB_INTERFACE index that does not exist still answers NO_SUCH_DESCRIPTOR, a command shorter than cdl 16 still answers BAD_ARGUMENTS, and AVB_INTERFACE still answers SUCCESS. The order is unchanged: length, then type, then existence. So a wrong type answers NOT_SUPPORTED whether or not that descriptor exists.

Clauses, as in the issue:

- Table 7-141: NOT_IMPLEMENTED (1) is "The ATDECC Entity does not support the command type". NOT_SUPPORTED (11) is "The command is implemented but the target of the command is not supported".
- Milan v1.2 5.4.2.23 requires the PAAD-AE to implement GET_AVB_INFO. The command type is implemented, and only the target (a descriptor_type other than AVB_INTERFACE, IEEE 7.4.40.1) is unsupported.
- IEEE 9.3.5.3.3's NOT_IMPLEMENTED covers command types the entity does not implement, not an implemented command aimed at the wrong descriptor type.
- Milan v1.2 uses NOT_SUPPORTED the same way in 5.4.2.2 (LOCK_ENTITY on a descriptor other than ENTITY) and 5.4.2.9 (SET_STREAM_INFO on a Stream Input).

## Change

- Engine: the GET_AVB_INFO arm of the A_PLD-exit re-dispatch sends a wrong type to `UPC_NSUPPE_C` instead of `UPC_NOTIMPL_C`, with `echo_r` still set. This is the existing command-sized NOT_SUPPORTED echo that GET_STREAM_INFO's wrong-type arm uses. That one constant is the only synthesised change. The comment that bounds the `UPC_NOTIMPL_C` sites is back to two sites, as before #182.
- Command model: the GET_AVB_INFO status set and entries return to `NOT_SUPPORTED` and `NSUPPE`. F06.14 is regenerated with `python3 -B scripts/check_aecp_commands.py --write`, and its row matches its pre-#182 text.
- `tb/aecp_cmds/decode.json` is re-recorded with `make -C tb/aecp_cmds record`. Only AEM 0x0027's wrong-type program moved: `NOTIMPL {1: echo}` became `NSUPPE {11: echo}`, cdl 16-100, floor 16. The engine digest changed with it.
- The compliance review's section 8 GET_AVB_INFO entry carries the ruling and the clauses above. In the table that entry is row 14; row 12 is the SET_CONFIGURATION notification decision (#178). 06 sections 6.10 and 8.1 and 09 follow.
- The microcode ROM is byte-identical: `ucode.hex` has the same sha256 at base and head, and the parent's ROM digest ledger records the same ucode and latency-ROM digests at this head as at main.

## Tests (`tb/pp_top` section V, main build and `make aecp-dispatch`)

- V5: the 13 rows now expect a byte-exact NOT_SUPPORTED echo. They cover ENTITY, CONFIGURATION, AUDIO_UNIT, both STREAM types, the types either side of AVB_INTERFACE, CLOCK_DOMAIN, an absent CLOCK_DOMAIN index, 0x0109, 0x8009 and 0xFFFF at cdl 16, and a CLOCK_DOMAIN padded to cdl 20.
- V1, V1b, V3 (NO_SUCH_DESCRIPTOR) and V4 (BAD_ARGUMENTS) are unchanged.
- M9 keeps its real AVB_INTERFACE 0 body, so an unguarded `gavb_w` runs E_GAVB.

Planted mutants, each killed by name at this head (failing checks in brackets):

- `gavb-other-type-not-implemented`, which plants #182's status: `V5 GET_AVB_INFO on CLOCK_DOMAIN 0: NOT_SUPPORTED` (13).
- `gavb-other-type-full-body` (new), the read-side fixed-body NOT_SUPPORTED in place of the command-sized echo: `V5 GET_AVB_INFO on CLOCK_DOMAIN 0 padded: NOT_SUPPORTED, the command echoed at cdl 20` (13).
- Header-only (13), gate dropped (13), low byte (2), inverted gate `gavb-interface-not-supported` (16), locate miss ignored (1), padding refused (2), floor 14 (1) and the M9 guard (14). These are #182's arms, regenerated against the new source and renamed where the old name named the old status.
- The `tb/aecp_cmds` standing control now plants #182's status and fails with `decode: GET_AVB_INFO: the table's entries name NSUPPE, which the engine never dispatches AEM 0x0027 to`.

## Validation at processor main 93fb0b2d and this head

- Every processor suite passes, 1,030,399 checks at both ends, with every suite line identical. V5 keeps its 13 checks.
- The requirement-tag execution check passes at both ends. Its evidence differs only by −1 line offsets in `tb/pp_top/sim_main.cpp` past V5.
- Lint, `make check`, the portability elaboration and the elaboration guards pass at both ends. `make check` differs only by the one new patch file in its ID scan (663 → 664 files).
- Every campaign that builds a changed file passes at this head:
  - AECP decode controls: 17 of 17.
  - Dispatch: 74 of 74 (4 controls and 70 arms).
  - Deadline and hazard-class: 67.
  - Counters: 18.
  - Milan-info face: 23.
  - Name write: killed.
  - ACMP: 65.
  - Notifications: 137.
  - D3: 110.
  - Elaboration-guard mutants: 160.
  - Name state: 16.
- All of these except notifications and D3 were also run at main and agree with it. The only differences are the GET_AVB_INFO arms and control named above: two renamed, one new, and the V5 wording that moved from NOT_IMPLEMENTED to NOT_SUPPORTED. The notification and D3 campaigns were run at this head only.

## Parent consumer gate

The scratch parent is a local clone of milan-fpga dev a032c6d6 with this head committed as the protocol-processor gitlink. Its ROM digest ledger was re-recorded for the new pin, giving the same digests as main. It was never pushed and needed no other change.

- `make -j8 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2` passes at dev's own pin (this PR's base) and at this head. Every check line is identical: 11,630 `[ok]`, 1,127 `[PASS]`, 0 `[FAIL]`.
- Area, from the parent's out-of-context recipe (`syn/yosys/ooc.sh`):
  - `protocol_processor_top` at its module defaults: 57,221 → 57,168 LUT (−53, −0.09 %). LUTRAM, FF, BRAM, DSP and CARRY4 are unchanged.
  - The parent's wrapper `KL_pp_shadow`: 58,039 → 58,506 LUT (+467, +0.80 %), again with nothing else moving. A re-run gives the same figure.
  - A control built from main plus only the one-constant swap gives the head figure exactly. Pointing the same arm at a third existing program instead gives 57,986.
  - So the in-wrapper LUT count moves by a few hundred with which existing program address that one arm loads. It reflects the mapper's sensitivity to that constant, not new logic or state.

## Note for review

The issue requires the NOT_SUPPORTED answer "echoed at its own length" (cdl 16 for the four-byte command), and this PR does exactly that. 06 section 6.6 records that the reference controller stack accepts a command-length reflection only for NOT_IMPLEMENTED, and sizes every other non-success answer against the response form. GET_AVB_INFO's response form is cdl 32 + 4·N, so that stack may report this echo as an incorrect payload size. GET_STREAM_INFO's existing wrong-type NOT_SUPPORTED echo is in the same position. The read-side set (GET_STREAM_FORMAT and the rest) answers a wrong target with a fixed-body NOT_SUPPORTED instead. Choosing that form for GET_AVB_INFO would be a separate decision; the `gavb-other-type-full-body` arm shows the V5 rows tell the two apart.

Ports, parameters and register maps are unchanged.
