<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Milan v1.2 — the road to full compliance

**Status 2026-08-16, VERSION `0x0002_004F`.** This is the ordered, clause-cited
plan from where the device is to a device that passes the Milan
end-station validation test plan. It supersedes the AECP sections of
[historical `MILAN_COMPLIANCE_GAPS.md`](MILAN_COMPLIANCE_GAPS.md), whose 2026-08-13 status
banner ("every AECP command except READ_DESCRIPTOR draws a NOT_IMPLEMENTED
echo") expired three days after it was written.

Authoritative sources, all read for this document rather than recalled:

| Source | Used for |
|---|---|
| `Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf` | every SHALL / SHOULD / MAY below |
| `1722.1-2021.pdf` | response PDU layouts, status codes, the base rules Milan defers to |
| `milanendstationvalidationtestplanv1.9.pdf` | the `es-N.M` test items each gap blocks |

Two reading rules this document keeps, because the repo grades by them:
**RECOMMENDED is not SHALL** — a `rec` row is tracked separately and is never
counted as a compliance gap. And **an echo is not an implementation** — a
conformant `NOT_IMPLEMENTED` answer is correct protocol behaviour and still
leaves the clause open.

---

## Contents

- **[0. Where the device actually is](#0-where-the-device-actually-is)** -- Implemented command surface, measured cost, and the state-store constraint.
- **[1. The remaining SHALL set](#1-the-remaining-shall-set)** -- Ordered command and dynamic-state work required by the profile.
- **[2. The non-command SHALLs](#2-the-non-command-shalls)** -- Persistence, notification, and controller-departure duties.
- **[3. Tracked, but NOT compliance gaps](#3-tracked-but-not-compliance-gaps)** -- Recommended or optional work kept outside the mandatory count.
- **[4. Two traps to carry into every round](#4-two-traps-to-carry-into-every-round)** -- Design constraints that repeatedly affect implementation choices.
- **[5. Recorded order and remaining follow-ups](#5-recorded-order-and-remaining-follow-ups)** -- Completed state-store work and the ordered consumer, command, notification, and persistence follow-ups.
- **[6. How each row gets proved](#6-how-each-row-gets-proved)** -- Required verification and acceptance evidence.

## 0. Where the device actually is

### 0.1 Served for real, today

**Twenty-three** AEM opcodes plus one MVU command. The authority is
`protocol-processor/hdl/aecp/KL_aecp_engine.sv`'s `OP_*_C` constants, and
`tests/steps/aecp_engine_steps.py`'s `SERVED` table is gated against that list
by a behave step that parses the RTL — so this section cannot silently rot
again.

**"Served" here means the command's own request/response contract.** It does
**not** include the unsolicited notification that Milan §5.4.5.2 and IEEE
§7.4.7 require after a successful `SET_*`: no microprogram enqueues one, the
only `NOTIFY_ENQ` in `gen_ucode.py` sits in an exemplar program, and
`pp_pkg.sv` defines notification kinds for the deregistration, `LOCK_ENTITY`,
and GET families only, with none for any `SET_*`. Every `SET_*` row below
therefore carries an open half tracked as #69 rather than a per-row caveat,
because it is the same missing mechanism in all of them. One more caveat worth
naming here rather than burying: `0x0016`'s stored
clock source reaches `milan_datapath` and is read by nothing (audit B3).

`0x0006` used to carry a second caveat — it stored an index that
`READ_DESCRIPTOR(ENTITY)` did not reflect, so §7.4.8.2's equivalence broke on a
multi-configuration image. That is closed: `E_RDESCENT` overlays the ENTITY
descriptor's last field with the same dynamic value `GET_CONFIGURATION` reads,
and `protocol-processor/tb/pp_top` W18c3/W18h grade the two commands **against
each other** rather than each against a literal, which is how the divergence hid
in the first place. What remains is narrower and worth stating: the shipping
one-configuration image cannot exercise a real active-configuration switch, so
the command stores and reports an index without any descriptor set changing
underneath it.

| Opcode | Command | Milan clause | Landed |
|---|---|---|---|
| `0x0000` | ACQUIRE_ENTITY (refused `NOT_SUPPORTED`) | 5.4.2.1 | 0x0044 |
| `0x0001` | LOCK_ENTITY | 5.4.2.2 | 0x0046 |
| `0x0002` | ENTITY_AVAILABLE | 5.4.2.3 | **0x004B** |
| `0x0004` | READ_DESCRIPTOR | 5.4.2.4 | 0x0040 |
| `0x0006` | SET_CONFIGURATION | 5.4.2.5 | **0x004D** |
| `0x0007` | GET_CONFIGURATION | 5.4.2.6 | **0x004B** |
| `0x0009` | GET_STREAM_FORMAT | 5.4.2.8 | **0x004B** |
| `0x000F` | GET_STREAM_INFO (Milan 80-byte form) | 5.4.2.10 | 0x0047 |
| `0x0014` | SET_SAMPLING_RATE | 5.4.2.13 | **0x004C** |
| `0x0015` | GET_SAMPLING_RATE | 5.4.2.14 | **0x004B** |
| `0x0016` | SET_CLOCK_SOURCE | 5.4.2.15 | **0x004C** |
| `0x0017` | GET_CLOCK_SOURCE | 5.4.2.16 | **0x004B** |
| `0x0018` | SET_CONTROL (IDENTIFY) | 5.4.2.17 | **0x004C** |
| `0x0019` | GET_CONTROL (IDENTIFY) | 5.4.2.18 | **0x004C** |
| `0x0022` | START_STREAMING | 5.4.2.19 | 0x004F |
| `0x0023` | STOP_STREAMING | 5.4.2.20 | 0x004F |
| `0x0024` | REGISTER_UNSOLICITED_NOTIFICATION | 5.4.2.21 | 0x0045 |
| `0x0025` | DEREGISTER_UNSOLICITED_NOTIFICATION | 5.4.2.22 | 0x0045 |
| `0x0026` | IDENTIFY_NOTIFICATION as a command → `BAD_ARGUMENTS` | IEEE 7.4.39.2 | 0x0042 |
| `0x0027` | GET_AVB_INFO | 5.4.2.23 | 0x0048 |
| `0x0028` | GET_AS_PATH | 5.4.2.24 | 0x0048 |
| `0x0029` | GET_COUNTERS | 5.4.2.25 | 0x0049 |
| `0x002B` | GET_AUDIO_MAP (both port directions) | 5.4.2.26 | 0x0048 |
| MVU `0x0000` | GET_MILAN_INFO | 5.4.4.1 | 0x0043 |

### 0.1b What the read-side set cost, measured

`KL_aecp_engine` out of context, yosys 0.66 `synth_xilinx -family xc7 -flatten`,
`HEAD~1` vs `HEAD` of the protocol-processor submodule:

| | 0x004A | 0x004B | delta |
|---|---|---|---|
| LUT (1..6 summed) | 3,242 | 3,277 | **+35** |
| FDRE + FDSE | 1,990 | 1,996 | **+6** |
| RAMB36E1 | 5 | 5 | **0** |
| CARRY4 | 194 | 194 | 0 |
| MUXF7 + MUXF8 | 210 | 241 | +31 |

**Five commands for about thirty-five LUTs and no block RAM.** Two reasons, and
both are reusable:

1. **The microprograms are free.** The µcode ROM is instantiated at its full
   2,048-word depth whatever is in it; the five programs plus two shared
   refusal stubs took 62 words of the 1,050-word free run, so the cost is ROM
   *contents*, not ROM. This is the whole point of the microcoded architecture
   and it will hold for the SET family too.
2. **The dispatch terms were shared, not grown.** Rather than adding five
   one-hot discriminators to the four OR chains that already listed seven, the
   round introduced `tix_w` (the `{descriptor_type @24, descriptor_index @26}`
   command shape) and `rgy_any_w` (the registry face's clients) and rewrote the
   chains through them. The operand muxes, the two payload-walk capture guards
   and both gather-face selects each went from a spelled-out OR to one name.

Read the LUT delta as *"of order tens"*, not as 35: the same
`-flatten` method rebalances decode between LUTs and F7/F8 muxes run to run
(visible above — LUT6 fell 117 while LUT3 rose 116 and the muxes rose 31). The
**flop count is exact and attributable**: +6.

### 0.2 The structural fact that shaped everything below — now built

Until VERSION `0x004C` **there was no dynamic-state store**, and that single
absence was why the whole `SET_*` family answered the `NOT_IMPLEMENTED` echo:
every value the device served came from the read-only descriptor image or a
live fabric face, and neither can hold a *setting*.

`KL_aecp_dyn_state.sv` is that store, and it is landed, tested and load-bearing
— `SET_SAMPLING_RATE`, `SET_CLOCK_SOURCE`, `SET_CONTROL` and
`SET_CONFIGURATION` all write it, and their getters read it in preference to
the image. `START`/`STOP_STREAMING` also wrote it and were pulled back out, and issue #78
has now settled where they belong: started/stopped lives in the **ACMP binding
record** and nowhere else. Milan §5.3.8.7 calls the state "undefined when the
Stream Input is not bound", so it is a property of the binding, and only that
record has the lifecycle — it is cleared on unbind, and it is captured by the
NVM shadow and restored through the boot preload. **The persistence PLUMBING is
complete; the persistence SHALL is not.** §5.3.8.7's third sentence ("shall be
saved in a non-volatile memory and restored after a power cycle") still waits on
a real flash backend: `KL_pp_shadow` sets `NVM_BACKED_C = 1'b0` and answers a
blank-flash stub, so nothing survives a power cycle on any shipping build. That
gap is issue #70's, and it is named here so "captured and restored" is not read
as "persisted". Selector 6 of the dynamic store is
**retired, not reused**, and the two commands reach the record through a
write-only request region that stores nothing, so a second copy cannot come
back by accident. The design and the two constraints that forced it are
kept in §P2.1 below, because they still govern every command that has not
landed yet.

**What it does not yet do is reach its consumers.** The dynamic store holds
seven fields (selector 6, started/stopped, is retired - see below). The fields served through AECP and those published to the fabric
are different sets:

| field | a microprogram reads or writes it | it has an output port |
|---|---|---|
| `current_configuration` | yes | yes |
| `clock_source_index` | yes | yes |
| IDENTIFY | yes | yes |
| `current_sampling_rate` | yes | **no** |
| presentation-time offset | **no** | yes |
| `current_format`, Stream Inputs | **no** | **no** |
| `current_format`, Stream Outputs | **no** | **no** |

Four fields have an output, and all four are read by nothing downstream. (A
fifth, started/stopped, USED to sit here with an output nothing read. It is
no longer in this store: issue #78 retired selector 6 and moved the state to
the ACMP binding record, where `milan_datapath` gates the listener accept
pulse on it - so that one is now both sourced and consumed.) The
media clock still uses its compile-time select, so `SET_CLOCK_SOURCE` stores a
value the servo does not act on. `current_sampling_rate` is the one field a
controller can move that the fabric cannot see. Aligning the audio grid to it
is #74's work. The two `current_format` rows are storage allocated ahead of
`SET_STREAM_FORMAT`, and neither side can reach them today. This deliberate
sequencing keeps the AECP side independently provable, but a green suite is
**not** a claim that the device behaves differently on the bench.

---

## 1. The remaining SHALL set

**Nine** AEM commands, in the order they should land. "Blocks" names the test
items from the validation test plan that cannot pass until the row does.

Five rows in the tables below carry a **LANDED** mark: they have shipped since
this section was written, and they stay in place because their clause notes and
"Blocks" lists are the record of what shipping them bought. Section 0.1 is the
authority on what is served; a row here without a LANDED mark is open.

### P2.1 — the dynamic-state store — **LANDED at `0x004C`**

Kept in full because the two constraints it is built around still govern every
command below. Not a command. A small register file, reachable as a new µISA state-port
region, holding exactly the fields Milan v1.2 declares settable — with one
field taken back out, because "settable" is not the same as "stored here":

| Field | Owner descriptor | Count here | Clause |
|---|---|---|---|
| current_configuration | ENTITY | 1 | 5.4.2.5 |
| current_sampling_rate | AUDIO_UNIT | 1 | 5.3.5.1 |
| current_format | STREAM_INPUT / STREAM_OUTPUT | 3 | 5.3.7.1 / 5.3.8.1 |
| presentation-time offset | STREAM_OUTPUT | 1 | 5.3.7.6 |
| ~~started/stopped~~ **RETIRED (#78)** | STREAM_INPUT | 0 — it lives in the ACMP binding record | 5.3.8.7 |
| clock_source_index | CLOCK_DOMAIN | 1 | 5.3.11.1 |
| IDENTIFY value | CONTROL | 1 | 5.3.12 |

Ten to twelve entries on the shipping shape. **LUTRAM, not flops** — the die is
LUT-bound and the standing area directive is explicit about it.

#### The design, validated against the µISA on 2026-08-16

The obvious shape — "one lane per {field, descriptor index}, addressed by the
µprogram" — **does not work**, and it is worth writing down why so nobody
spends a day rediscovering it. `READ_ST` and `WRITE_ST` compute
`st_addr_o = desc_base_r + uop_e_r.imm[19:0]` (`KL_aecp_ucpu.sv:311`) and
`desc_base_r` is invariantly 0 in this system, so **the state-port address is
an immediate and nothing else**. There is no register-indexed addressing, so a
µprogram cannot say "the lane for the descriptor this command names".

The shape that does work follows the gather faces, which solved the same
problem already:

- **The address selects the FIELD.** `st_addr[15:3]` is a field selector —
  0 = sampling rate, 1 = clock source index, 2 = current format, and so on —
  so each µprogram names its own field with a constant, which is all an
  immediate can express.
- **The descriptor index comes from the engine**, registered, exactly the way
  `ctr_desc_index_o`, `gsi_desc_index_o` and `amap_desc_index_o` already do
  (`KL_aecp_engine.sv:966-1007`). The store module takes `desc_type_i` and
  `desc_index_i` alongside its state port and picks the row itself.
- **Put it in its own module**, `KL_aecp_dyn_state.sv`, muxed onto the state
  port by region code at the engine — regions `0x1` (value) and `0x2` (valid
  flag) are free; only `0x0`, `0xC`, `0xD`, `0xE` and `0xF` are taken. A
  separate module leaves `KL_aecp_desc_store`'s 501 checks untouched, which
  matters more than saving the file.
- **Valid-bit with image fallback, not seed-at-boot.** A GET reads the valid
  flag, branches, and takes either the overlay or the image — about five extra
  µwords per command. This is the variant that **composes with P3.1**: a
  persistence restore just writes values and sets valid bits, whereas a
  seed-from-image design would have to be taught not to overwrite what NVM
  restored. Pick the one that does not fight the next item.

*Acceptance*: a new `protocol-processor/tb/dyn_state` suite proving
overlay-beats-image per field and per descriptor index; the five 0x004B GETs
re-graded in `protocol-processor/tb/pp_top` §W through both arms (unwritten → image, written →
overlay); and reset behaviour — the volatile fields (lock, registry, IDENTIFY)
clear, the persisted ones do not (see P3.1).

### P2.2 — the GET half that P2.1 unblocks

| Opcode | Command | Clause | Response | Blocks |
|---|---|---|---|---|
| `0x0011` | GET_NAME | 5.4.2.12 | cdl 84: type, index, name_index, configuration_index, 64-byte name | es-4.7, es-4.18, es-5.1, es-6.1, es-6.2 |
| `0x0019` | GET_CONTROL **— LANDED** | 5.4.2.18 | cdl 17: type, index, one `CONTROL_LINEAR_UINT8` value (0 or 255) | es-4.10 |

Both of these look like one-afternoon reads and are not. Measured 2026-08-16
while scoping this round:

**`GET_NAME` has no name table to read.** The store's name-table overlay
exists and is writable, but `avdecc/gen_aemi_image.py:239-241` deliberately
emits **no** name table — *"Names are left to the descriptors' own inline
`object_name` fields, so no name table is emitted (`name_index` unset means
'unnamed' to the packer)."* So every descriptor's `nbase` reads `0xFFFF` and
the names live inline at descriptor offset 4. Two consequences:

1. **Offset 4 is not lane-aligned**, and the µISA has no shift. `COPY_BUF`
   starts at the 8-byte lane the address falls in, so it cannot lift a 64-byte
   field that begins 4 bytes into lane 0. Serving names from the inline field
   needs either a byte-offset `COPY_BUF` (a µCPU change) or the name table.
2. **The name table has to grow.** `KL_aecp_desc_store.sv:153`
   `NAME_ENTRIES_P = 16`, and the store *refuses an image* whose `n_names`
   exceeds it (`:460`). Milan §5.3.13's settable-name list on the 1x1 shipping
   shape comes to about 29 entries — ENTITY contributes two
   (`entity_name` index 0, `group_name` index 1, IEEE §7.4.18.1) and the 16
   AUDIO_CLUSTERs contribute 16. Sixteen entries is 1 KB of on-chip RAM;
   thirty-two is 2 KB, **on a die already at 67 % BRAM**.

So P2.2's real first question is a sizing decision, not a microprogram:
inline-with-a-µISA-change, or name-table-with-more-BRAM. Take it to the area
budget before writing either.

**`GET_CONTROL` cannot honestly read the image.** The IDENTIFY value is
dynamic state: Milan §5.3.12 makes it 0 or 255 with 0 the reset default, and
`SET_CONTROL` is its writer. The image's copy sits at CONTROL offset 108
(`avdecc/gen_aem_store.py:1351`), which is lane byte 4 — mid-lane, so the same
extraction limit applies — and it would in any case go stale the moment
`SET_CONTROL` lands. `o_identify` is tied 0 in the fabric today. This command
belongs with `SET_CONTROL` and the P2.1 store, not before them.

> **The cross-cutting constraint both of these hit:** a field is servable from
> the descriptor image only if it **ends its 8-byte lane** (readable
> right-justified by `READ_ST` + `BUILD_FLD`) or **begins one** (liftable by
> `COPY_BUF`). Everything else needs a shift the µISA does not have. The five
> commands that landed at 0x004B were chosen because their fields satisfy
> exactly that: `current_configuration` @310 and `clock_source_index` @70 end
> their lanes; `current_sampling_rate` @136 begins one. Check the offset before
> promising the command.

### P2.3 — the SET half

Every row is lock-protected: Milan repeats the same sentence in each clause —
*"If the PAAD-AE is locked by a controller, it shall not accept a `<CMD>`
command from a different controller, and it shall also not change `<the state>`
by non-ATDECC means."* The µISA already has `CHECK_LOCK` for exactly this.

| Opcode | Command | Clause | The Milan-specific refusal | Blocks |
|---|---|---|---|---|
| `0x0006` | SET_CONFIGURATION **— LANDED** | 5.4.2.5 | `STREAM_IS_RUNNING` (12) if **any** Stream Input is bound or **any** Stream Output is streaming | es-4.3, es-5.1, es-12.1, es-12.2 |
| `0x0008` | SET_STREAM_FORMAT | 5.4.2.7 | `STREAM_IS_RUNNING` on a **bound** input or streaming output; `BAD_ARGUMENTS` if any existing mapping references a channel absent from the new format | es-4.4, es-5.1, es-9.x, es-10.x, es-12.1, es-12.2 |
| `0x000E` | SET_STREAM_INFO | 5.4.2.9 | `NOT_SUPPORTED` on **any** Stream Input; `MSRP_ACC_LAT_VALID` sets the presentation offset, range `0x0`–`0x7FFFFFFF` ns, outside → `BAD_ARGUMENTS`; any unsupported sub-flag → refuse the **whole** command `NOT_SUPPORTED` | es-4.5, es-5.1, es-10.2, es-12.1 |
| `0x0010` | SET_NAME | 5.4.2.11 | must accept names of **non-active** configurations too (es-4.7) | es-4.7, es-4.18, es-5.1, es-6.1, es-6.2 |
| `0x0014` | SET_SAMPLING_RATE **— LANDED** | 5.4.2.13 | the rate/mapping-mismatch refusal is a **MAY**, not a SHALL | es-4.16, es-5.1 |
| `0x0016` | SET_CLOCK_SOURCE **— LANDED** | 5.4.2.15 | — | es-4.9, es-5.1, es-10.1 |
| `0x0018` | SET_CONTROL **— LANDED** | 5.4.2.17 | IDENTIFY only; values 0 and 255 | es-4.10 |
| `0x0022` | START_STREAMING **— LANDED** | 5.4.2.19 | `NOT_SUPPORTED` on a Stream **Output** (and on every other type); on a bound+stopped input → started. **Residue:** the IEEE 7.5.2 unsolicited *response* for this opcode is not sent — the Table 5.22 GET_STREAM_INFO push on the state change is (issue #69) | es-4.11, es-12.7 |
| `0x0023` | STOP_STREAMING **— LANDED** | 5.4.2.20 | mirror of the above, same residue | es-4.11, es-12.7 |

> **`SET_CLOCK_SOURCE` is worth more than one row.** Its dynamic-state store
> and wrapper output have landed. The selected index now reaches the root, but
> no media-plane consumer reads it. Replacing the INTERNAL selection constant
> with that validated value is still required before `KL_mmcm_drp_servo` and
> the `KL_media_nco` packet-grid servo can become live.

### P2.4 — dynamic audio mappings

| Opcode | Command | Clause | Blocks |
|---|---|---|---|
| `0x002C` | ADD_AUDIO_MAPPINGS | 5.4.2.27 | es-4.16, es-5.1, es-9.2, es-11.6, es-12.11 |
| `0x002D` | REMOVE_AUDIO_MAPPINGS | 5.4.2.28 | as above |

All-or-nothing `BAD_ARGUMENTS` (*"no mapping shall be added"*), the two
same-channel conflict rules, REMOVE ignoring duplicates, and the
running-output gate keyed on `TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING`. The µISA
already carries `MAP_VALID` for the validation and `E_MAPV`/`E_MAPVF` as
exemplar programs; the read side (`GET_AUDIO_MAP`) is already live off the
integrator's map store, so the write path is the gap.

### P2.5 — the packed getter

| Opcode | Command | Clause | Blocks |
|---|---|---|---|
| `0x004B` | GET_DYNAMIC_INFO | 5.4.2.29 | *nothing in test plan v1.9* |

A SHALL that the v1.9 test plan never sends. It is therefore last: real
compliance debt, zero risk to a compliance run. Note IEEE §7.4.76's hard rule — if
any packed sub-command could ever return `IN_PROGRESS`, the entity **shall not
support GET_DYNAMIC_INFO at all**; this engine's policy is never to answer
`IN_PROGRESS`, so the rule is satisfiable. The µISA has `ITER_OPEN` /
`ITER_NEXT` / `APPEND` and `E_OVF`'s skip-on-overflow for it already.

---

## 2. The non-command SHALLs

### P3.1 — persistence (Milan 5.3.5.1, 5.3.7.1/.6, 5.3.8.1/.2/.3/.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13)

Eight items the device **shall** save and restore across a power cycle:
current configuration; sampling rate per Audio Unit; format per Stream
Input/Output; presentation offset per Stream Output; channel mappings both
directions; clock source per Clock Domain; the bound state and binding
parameters; every user name.

**Nothing in this device persists anything.** The processor's NVM face is a
blank-flash responder: reads `0xFF`, accepts and discards writes, completes
erase. A restore walk always finds blank flash and completes with zero records.

Blocks **es-5.1 entirely**, and es-5.1 has **no "if the DUT does not implement
persistence" escape clause** — this is a hard compliance gate, not a
nice-to-have. It also blocks Milan 5.5.1.4 / 5.5.2.6 saved-state fast-connect.

Volatile by rule, and must **not** be persisted: the lock state, the registered-
controller list (both *"cleared by a power cycle"*), and the IDENTIFY value
(0 after reset).

### P3.2 — unsolicited notification triggers (Milan 5.4.5.2 + Table 5.22)

The registry, the fan-out and the sequence-per-controller are landed. What is
open is the **trigger set**: every successful state-changing command must push
to every registered controller *except the requester* (es-6.2 is an inverted
gate — notifying the requester **fails**), plus the asynchronous triggers of
Table 5.22: GET_STREAM_INFO field changes, GET_AVB_INFO changes, GET_AS_PATH
changes, GET_COUNTERS (rate-limited to **≤1 per descriptor per second**), the
LOCK auto-unlock, and auto-DEREGISTER.

Most of P2.3 lands its own trigger, so this is best done command-by-command
rather than as one round. Blocks es-4.4, es-4.7, es-4.16, es-4.18, es-6.1,
es-6.2, es-12.4, es-12.5, es-12.6, es-12.7.

### P3.3 — departing-controller detection (Milan 5.4.5.3)

Per registered controller: a **random 30–60 s** monitor timer, reset by any
valid AECP command from that controller; on expiry a `CONTROLLER_AVAILABLE`
(`0x0003`) command with **one** retry per IEEE §9.3.6; any reply at all — *"no
matter the value of the status code"* — re-arms; silence removes the entry and
sends a targeted unsolicited `DEREGISTER_UNSOLICITED_NOTIFICATION`.

This is the only place the device must **originate** an AECP command. The
processor has `KL_pp_originator` (already used for the ACMP retry path) and a
timer service, so the machinery exists. Blocks es-6.4, which measures the first
probe at **27–66 s** and the retry within **250 ms**.

---

## 3. Tracked, but NOT compliance gaps

Do not schedule these as SHALLs and do not let a grader count them.

| Item | Clause | Level |
|---|---|---|
| MVU `0x0001`/`0x0002` SET/GET_SYSTEM_UNIQUE_ID | 5.4.4.2/.3 | **RECOMMENDED** — *"Support for this feature is a recommendation … will become a requirement in a future revision"* |
| MVU `0x0003`/`0x0004` SET/GET_MEDIA_CLOCK_REFERENCE_INFO | 5.4.4.4/.5 | **RECOMMENDED**, same construction |
| IDENTIFY_NOTIFICATION as a transmitted unsolicited response | 5.4.5.4 | **SHOULD** — *"it should implement the Identification Notification"* |
| `ACQUIRE_ENTITY` answering specifically `NOT_SUPPORTED` | 5.4.2.1 | the SHALL is only *"shall not reply SUCCESS"*; the code choice is a SHOULD (we do answer `NOT_SUPPORTED`) |
| Redundancy (§8, R-PAAD) | 8.x | out of scope: this is a single-AVB_INTERFACE PAAD, so es-11.x is Not Applicable |

---

## 4. Two traps to carry into every round

**The STREAM_OUTPUT counter bits are Milan's, not IEEE's.** Milan Table 5.17
drops `STREAM_INTERRUPTED`, `TIMESTAMP_VALID` and `TIMESTAMP_NOT_VALID` from
the IEEE Table 7-158 set and **compacts the survivors upward**: `MEDIA_RESET`
sits at `counters_block` offset 8 under Milan and offset 12 under IEEE
1722.1-2021. Milan flags this itself (*"Note: Some of the STREAM_OUTPUT counter
definitions below are not in line with the definitions in the ATDECC
specification"*). A reference peer built from 1722.1 alone will decode our
talker counters wrong. `STREAM_INPUT`, `AVB_INTERFACE` and `CLOCK_DOMAIN` do
**not** diverge.

**Only `NOT_IMPLEMENTED` may answer at command length.** IEEE §9.3.5.3.3 wants
"a correctly sized response", and the reference stack reads that as the
reflected command *for `NOT_IMPLEMENTED` only* — la_avdecc's
`checkResponsePayload` sizes every other status against the **response** form.
So a `NOT_SUPPORTED` refusal must carry the full response body. This cost the
0x0049→0x004A round a silicon-visible "Incorrect payload size" complaint; the
0x004B commands each carry a full-body refusal for the same reason.

---

## 5. Recorded order and remaining follow-ups

1. **P2.1** dynamic-state store: landed and serving the implemented setters.
2. **P2.3 consumer follow-up**: validate and consume the exported clock-source
   and sampling-rate state in the media plane. The clock-source command alone
   does not light up the media-clock servo.
3. **P2.2** `GET_NAME` + **P2.3** `SET_NAME` — one pair, one storage question
   (`name_index` fan-out), and five test items.
4. **P2.3** `SET_STREAM_FORMAT` and `SET_STREAM_INFO`: these still need the
   bound/streaming interlocks. The already-landed `SET_CONFIGURATION` path now
   applies its running reduction at dispatch, and `START`/`STOP_STREAMING`
   landed with issue #78 — their interlock turned out to be the binding
   record's own (§5.3.8.7's "undefined when not bound"), not a reduction over
   every stream.
5. **P3.2** notification triggers, folded into each command above as it lands.
6. **P2.2/P2.3** `GET`/`SET_CONTROL` with the IDENTIFY indicator wired.
7. **P2.4** ADD/REMOVE_AUDIO_MAPPINGS.
8. **P3.3** departing-controller monitor.
9. **P3.1** persistence — largest, and the only one that needs a real flash
   backend rather than the blank-flash stub.
10. **P2.5** GET_DYNAMIC_INFO.

---

## 6. How each row gets proved

The ladder, cheapest first. A row is not done until it has all four.

| Layer | Where | What it proves |
|---|---|---|
| microprogram | `protocol-processor/tb/ucpu` | the program runs, branches and sets status |
| wire truth | `protocol-processor/tb/pp_top` §W and siblings | the response is byte-exact against a payload the bench builds from the IEEE figure |
| against the model | `tb/verilator/milan_dp` `sim_nxn.cpp` `[AECP-MODEL]` | the answer matches the **generated entity model**, for every descriptor the generator emitted, with a negative oracle for every absent one |
| the inventory | `tests/features/aecp_response_contract.feature` | the opcode partition, gated against the engine RTL's own `OP_*_C` constants so the suite cannot go stale |

The `[AECP-MODEL]` block is the one that answers "do all the commands respond
correctly to the entity model": it runs `endstation_builder.py` and
`gen_aemi_image.py` live, loads the image into the RTL's DRAM, and grades every
answer against the model's own bytes — never against a literal, and never
against the DUT's own earlier answer. At 0x004B it walks **50 of 50**
descriptors and probes six absent ones.

What none of these layers can prove is timing, PHY behaviour or switch
interop. Those stay on-silicon, and a green sweep is never a hardware claim.
