[R762] NEGATIVE - exact head cfb799229d3c5c695468cc1a7cad08403e57f265

# R762-3: external review of issue #829 / PR #831, round 3

Tree `ee5e690bf5af14052ef5d00bff34cecbdc8624ce`. Delta `2d534bec..cfb79922`: 2 commits, 3 files, no file under `hdl/`. Source base and live `dev` are `1f29f189279f9fc0132f4918e47342b87d22f33a`.

**One MINOR keeps this NEGATIVE, and its reach today is narrow.** Gate 1h now reads comments and dead arms correctly, passes on the pinned front end locally and hosted, and refuses when the front end is missing. But it reads the datapath alone, and the build reads 118 sources in order. A binding that is dead only because of a macro from an earlier source therefore passes the gate. The shipped wiring is correct, and nothing is wrong on either board.

## Findings

### R762-3-F1: MINOR: gate 1h misses a dead arm decided by a macro from an earlier source

- **Lenses:** Tests, Docs
- **Path:** `sw/builder/test_builder.py:18331-18338` (the front-end call names one file), `:18317-18319` (the docstring's claim), and PR #831 body, "The fix": "The gate now reads what the build's front end reads ... Comments and dead arms are gone before the gate looks".
- **Authority and evidence:** AGENTS section 6, `Tests`: each new test can fail for the defect it claims to detect. AGENTS section 6, `Docs`: changed contracts are reflected. R761-2 F1's required outcome: "A dead preprocessor arm is either refused or named as a limit in the gate's own comment." This arm is neither.

  `syn/yosys/run.sh --emit milan_datapath` lists 118 sources with the datapath last, and sv2v carries a `define` from one source into the next. The gate passes only the datapath, so it cannot see that state.

  | Plant, on `hdl/milan/milan_datapath.sv` | Gate 1h | Conversion with the emitted flags and source order |
  |---|---|---|
  | Shipped text | accepted | `sv2v --top` rc 0; plane binds `ETH_TICK_NS_P` and `ETH_CYC_PER_OCTET_P` |
  | Octet binding inside `` `ifndef ETHERNET_PACKET_PKG_SV `` | **accepted** | rc 0; **plane binds only `ETH_TICK_NS_P`, so `ETH_CYC_PER_OCTET_P` keeps its GMII default** |
  | Tick binding, same guard | **accepted** | Not converted; same mechanism |
  | Either default, old value under that guard and the MII value in its `else` | **accepted** | Not converted; same mechanism |

  Receipts: `receipts/plants-sv2v-012.log`, `plants-sv2v-013.log` (the four `BAD` rows), `probe-earlier-macro.log`, `earlier-macro-build-shipped.log`, `earlier-macro-build-planted.log`.
- **Reach today:** earlier sources define exactly one macro, the package guard `ETHERNET_PACKET_PKG_SV`, so the escape takes a deliberately odd guard today. Any file-scope macro later added to an earlier source would widen it. `milan_datapath.sv` has no preprocessor conditional at all.
- **Why it is not RESIDUE or a SUGGESTION:** it concerns what a test can detect, and this is the defect class round 3 set out to close. Naming it as a limit would be a wording fix, but closing it is a code change, so I am not certain it is wording only. The owner rule makes that MINOR.
- **Impact:** with the octet binding dead this way, the sv2v conversion leaves the plane on its GMII default. On MII the plane then expects 45 clocks against the observer's 90, and every frame is lost unmeasured, behind a green gate. Vivado's read of the same plant was not run.
- **Required outcome:** one of these two.
  1. The gate reads the datapath in the build's source context and refuses these plants, with at least one such plant as a committed control.
  2. The gate's comment and the PR's limit paragraph name this case as outside the gate, and "reads what the build's front end reads" and "dead arms are gone" are narrowed to match.

  Option 1 was tried on a disposable copy: pass the record's other sources before the planted copy, and read the output from `module milan_datapath` on. The gate stays at 37/37 and 6/6, all 66 refuse rows are refused and all 15 accept rows accepted, and the gate alone takes 120 s against 36 s. Receipts: `receipts/whole-list-fix-gate.log`, `plants-whole-list-fix.log`.
- **Verification:** run `scripts/plant_gate1h_r3.py <clone> 16` with the pinned front end first on `PATH`. For option 1 it must report `not as wanted: 0`. For option 2, re-file the four rows as `limit` and read the comment.

## Residue, wording only

| ID | Lens | Path | Defect | Exact fix |
|---|---|---|---|---|
| R762-3-R1 | Docs | `README.md:281`, `README.md:252`, `README.md:223` | `sw/builder/test_builder.py` now needs sv2v. Row 281 still says `python3 + pyyaml`, line 252 calls the step "pure Python" with only the lint gate needing more, and sv2v is listed as tier 2 only. With no sv2v the run stops at gate 1h, inventory index 17, leaving 89 gates unrun; the next gate alone passes without it (`receipts/no-sv2v-next-gate.log`). The refusal itself is right. At `2d534bec` the suite and the scripts it names call no sv2v, by static trace | Row 281: `python3 + pyyaml + sv2v`. Line 252: `# 4 · run the repo gates — pure Python, seconds (the lint one wants verilator, the builder one sv2v)`. Line 223 note: add "; `sw/builder/test_builder.py` gate 1h also reads the datapath through it" |

## Suggestions

- **R762-3-S1, Tests:** the default's read uses `[^=\n]*` before the name, so a shadow with `=` earlier on its line escapes, and a genvar loop's header does not end in `;`. Both need the plane moved into a new generate block. Yosys confirms the first shape gives 40 in a small module (`receipts/probe-shadow.sv`, `probe-shadow-yosys.log`). Replacing the read with `re.findall(rf"^\s*(.*\b{param}\s*=(?!=).*)$", code, re.MULTILINE)`, compared against `[f"parameter int unsigned {param} = {default};"]`, refuses all four probes and keeps 37/37 and 6/6 (`receipts/suggested-fix-gate.log`, `plants-suggested-fix.log`).
- **R762-3-S2, Docs:** the comment at `.github/ci-templates/docs.yml:164-166` gives the builder's dp_srcs self-test as why the job installs sv2v. Gate 1h is now the reason that holds at this head; the comment is older than this delta.
- **Retained, for their own Issues:** R761-2 S1 and R762-2-S1 (gate 1g has the same comment gap), R762-2-S2 (an elaboration of the plane's effective parameters), R761-2 S2 (a route of `dev`), R761 S4, R761 S5, R762-S1, R762-S3.

## The four requested checks

**1. Gate 1h reads through the front end, and missing sv2v is a refusal: yes, except for F1.**

- The call uses `sv2v --pass-through` with the record's defines and include directories (`test_builder.py:18324-18338`). The clean clone's record states `define=SYNTHESIS` and seven include directories.
- My own script ran 90 plants on v0.0.12 and on v0.0.13, with identical answers. Of 66 that must be refused, 62 were; the other four are F1. All 15 equal spellings were accepted.
- The refused plants include line, block and multi-line comments; dead and `ifndef SYNTHESIS` arms; a tie under `SYNTHESIS` with the binding in the `else`; macro ties and a macro that discards its argument; shadows beside and around the plane; a second instance in the plane's own statement; a missing include; and a syntax error.
- The script exits 1 at this head because of those four rows.
- Missing sv2v: rc 1, `gate 1h: sv2v is not on PATH`. A failing shim, an empty-output shim and a shim that echoes its input each give rc 1 by name.
- Six mutants of the gate each fail the test: no defines, containment reads of the binding and the default, no plane count, no instance name, and raw text (`receipts/gate1h-mutants.log`).

**2. The shipped wiring passes in the hosted job: yes, executed at this exact head.**

- `docs-gates-2` runs leg 1, and it installs the checksum-pinned sv2v before the builder step, with no `if` on either.
- Its log shows `sv2v v0.0.12` and `[gate 1h mutation] 37/37 cuts rejected, 6/6 equal spellings accepted`, and the job concluded success (`receipts/hosted-docs-gates-2-gate1h.log`, `hosted-docs-gates-2-steps.json`).
- That log ends `ALL GATES PASS EXCEPT 17 NOT RUN`; the author's local leg 1 had 16. The extra row is gate 38, "no Verilator on this runner", which does not concern gate 1h.
- All four builder jobs install sv2v before the builder step, by parsing the workflows.
- A clean clone with only the job's three submodules, and no yosys or verilator on `PATH`, passes on the pinned binary (checksum verified). It also passes under a bare and a POSIX locale, though the datapath has 69 non-ASCII lines.

**3. The stated limit is acceptable: yes, as far as it goes.**

- A `defparam` and a never-elaborating arm are both accepted by the gate, as the comment and PR say.
- No `defparam` appears in `hdl/`, `tb/` or `sw/litex/`, or in the SystemVerilog and Verilog of `protocol-processor`, `gptp-processor` and `third_party/verilog-axis`. The only hit under `syn/` is a comment.
- A `defparam` is a deliberate override rather than a cut made by editing. Parsing without elaborating is an honest boundary, and the elaboration that would close the class stays R762-2-S2.
- The plane does sit in a real arm, `if (GPTP_PLANE_EN_P)`, which is why the stated limit matters. The elaboration job names `test_gptp_plane_reaches_the_instance` for that enable; I read its name in the requirement list, not its body.
- The limit does not cover F1, which is a preprocessor case. A plane in a never-instantiated module is also accepted, and "parses and does not elaborate" does cover that.

**4. Residue applied and the program unchanged: yes.** `milan_soc.py`'s parsed program is identical between `2d534bec` and `cfb79922` (`receipts/soc-ast.log`). The per-item results are in the prior-findings table below.

**Comment rule:** no lane label, round, reviewer ID or comment ID in the delta's added lines (`receipts/comment-rule-grep.txt`). Both commits are one line with no trailers.

## Clean lenses

```text
[R762] PASS Conformance — sw/builder/test_builder.py:18303-18307 against hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:281 and KL_gptp_shadow.sv:1036; receipts/soc-ast.log — no protocol behaviour moves in the delta; the comment's 45 against 90 clocks and (90+2+2-1) x (40-8) = 2976 ns both hold; #829 acceptance keeps its R762-2 result
[R762] PASS RTL — git diff --stat 2d534bec cfb79922 -- hdl (empty) and receipts/soc-ast.log — no RTL changes and milan_soc.py's parsed program is identical, so the R762-2 result stands
[R762] PASS Robustness — receipts/gate1h-no-sv2v.log, gate1h-shim-empty.log, gate1h-shim-fail.log, gate1h-shim-cat.log, gate1h-bare-locale.log, gate1h-posix-locale.log — the gate fails closed on a missing, failing, empty or echoing front end and on an unterminated comment, missing include or syntax error, and holds under a bare locale
```

## Ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta comment figures against `KL_gptp_txret.sv:281`, `KL_gptp_shadow.sv:1036`; `receipts/soc-ast.log` | R762-3 for the delta; R762-2 for code the delta does not touch | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| RTL | CLEAN | Empty `hdl/` diff; `receipts/soc-ast.log`; `milan_datapath.sv:92-93,8880-8889` read | R762-3 for the delta; R762-2 for code the delta does not touch | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| Robustness | CLEAN | Fail-closed shims, missing tool, locales, broken input rows in `receipts/plants-sv2v-012.log` | R762-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| Tests | UNCLEAN (F1) | `test_builder.py:18303-18460`; `receipts/plants-sv2v-012.log`, `plants-sv2v-013.log`, `gate1h-mutants.log`, `earlier-macro-build-*.log` | R762-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |
| Docs | UNCLEAN (F1) | Gate docstring; PR body "Round 3"; `tb/verilator/gptp_txts/README.md:75-80`; `milan_soc.py:2091-2096`; `README.md:223,252,281`; author-r3 `HANDOFF.md` | R762-3 | `cfb799229d3c5c695468cc1a7cad08403e57f265` |

`receipts/independent-pass-before-prior-findings.md` is my provisional note, written before I read any prior finding. It says POSITIVE because I had not yet run the earlier-source probe that produced F1. This report's verdict replaces it.

## Prior public findings

| Finding | At this head | Evidence |
|---|---|---|
| R762-F9, R761-2 F1: comment and dead-arm cuts accepted | **Closed for every plant those reports named. The dead-arm clause stays open only for F1's case** | All named plants refused by name in `receipts/plants-sv2v-012.log`; author-r3 `plants/` logs show 17 of 17 and 14 of 14 refused |
| R761-2 RES1, R762-2-R1: `eth_rst` sentence | **Closed** | `milan_soc.py:2094-2096`; parsed program identical |
| R761-2 RES2: the two cuts' effects | **Closed** | `test_builder.py:18304-18307`; 2976 ns recomputed |
| R761-2 RES3: lifecycle bullet | **Closed** | PR body reads "See #833." |
| R761-2 RES4: README wrap | **Closed** | `tb/verilator/gptp_txts/README.md:78-80` |
| R762-2-R2: citation | **Closed** | Clause is at `KL_gptp_gmii_launch.sv:101`; author-r3 `HANDOFF.md` corrects it; published round 2 packet not regenerated, as disclosed |
| R761-2 S1, S2; R762-2-S1, S2; R761 S4, S5; R762-S1, S3 | Retained as suggestions | Not taken; the delta does not change them |
| R762-S2 and R761 S1 (#832); R762-S4 and R761 S2 (#833) | Tracked, not findings here | Both Issues open |
| Round 1 and round 2 findings already closed | **Remain closed** | No RTL, harness or document they depend on changed, apart from the re-wrap and the comment order above |

## Author evidence

- Commit `80e3b4ea` is **unsigned**: GitHub reports `verified: false, reason: unsigned`. I could not verify a signature, so integrity below rests on digests only.
- All 165 `author-r3` rows in `MANIFEST.json` match their published bytes.
- Of the 162 rows in `receipts/INDEX.md`, 95 match the published bytes and 67 match the manifest's original digest of a path-redacted file. None match neither (`receipts/author-r3-index-reconcile.log`).
- The author's receipts do not state which sv2v version ran. The pinned version is established by my runs and the hosted log instead.

## Real limits

- I did not run the full builder bank, so the statement that the suite did not need sv2v at `2d534bec` is a static trace of the suite and the scripts it names.
- The build-path evidence for F1 is a one-shot `sv2v --top` with the emitted flags and source order, plus one added include directory for the moved copy. It is not a Yosys or Vivado run.
- At my last snapshot (`receipts/hosted-final-snapshot.txt`) no hosted job had failed, but `docs-gates-0`, `elaborate-gates-1`, `publication-census` and all of `rtl-full` were unfinished. I make no claim for those contexts. I did not run Docker or `act`.
- No manager source bank exists at this head, and I infer none. Physical calibration was NOT RUN, and field skips are not hardware proof.
- I did not read R761-3. All probes ran in a disposable clone; this review clone was only read and still matches the head.

## Pending manager duties

- Carry R762-3-R1 to the residue checklist and return F1 to the author.
- Own hosted and local-replica acceptance, the current-dev merge candidate and post-merge containment.
- Physical calibration and the tap-out check stay owed through #583.

R762-3 FINISHED
