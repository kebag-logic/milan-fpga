[A583] REVIEW READY — Round 19 continuation

Head: `97e713168470bfae2685521fa557dc462b782b32` (local only; not pushed).
Base merge retained: `95ca54cb`, with dev `d5858bbee328cf8d2c39a99ec14203f5d0ddd123` as its second parent.

The scope extension in comment 6137497435 is implemented. `test_ctrl_memory.py --build-only` is a fifth mandatory compiler capture; the unchanged probe/link helper is shared with the full suite. Each of the three programs has a load-bearing unclassified-copy control. Dropping the fifth capture refuses it by name, and a private stack-header include in the reset entry is caught through that capture. The baseline reset compile reads no forbidden source.

Classification scope is explicit: `ctrl_memory.py` compiles nothing. `milan_soc.py` is OUTSIDE relative to this control firmware: it loads a prelinked control ELF; its separate BIOS/milan_baremetal path builds other firmware and compiles no control-stack source. The reason does not claim that the entire program compiles nothing.

Local evidence, final required commands all rc 0:
- 65/65 linked ELFs equal dev by direct bytes, size and SHA-256; both manifests hash to `96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584`. The tsn-c-stack pin remains `405dc68310a18f669049ffc10cc23eef7300dcff`; no production firmware or image input changed in the continuation.
- Firmware boundary: 2824 sources / 3052 invocations; 110 boundary, 106 pin and four figure controls, no findings or misbehavior. Verilator boundary: 829 / 926; six boundary, 106 pin and four figure controls, no findings or misbehavior.
- All 915 firmware verdicts pass: 60 arms, 506 control, 76 AECP, 198/73 SRP and two lwSRP pin controls. Store execution: 435 tests across five shapes. Memory suite: 44/44 mutants caught.
- Coverage: 30 files at 100% lines/branches after unchanged exclusions; candidate and dev tables match under the same compiler; 29/29 reader controls pass.
- Entry points: 252/252 named refusals. Pin matrix, hook rule-removal, configuration variants and the earlier unchanged review probes retain their expected outcomes on both Git versions and both Python versions.
- CI contract: 2169 checks and 3064 self-test arms; 16 additional workflow plants caught. All 54 documentation/source-list/evidence commands pass. Disposable runner self-test: 446 arms pass.
- Boundary phases plus measured dependency installation total 836.57 s locally, 46.5% of the unchanged 30-minute timeout. This is a sum of bounded foreground commands, not new hosted timing. The four prior firmware jobs and their hosted budget evidence remain unchanged.

The handoff and prepared PR body contain the changed file:line table, full image/coverage/mutation tables, pin diff/proof, commands, receipts and limitations. R584-16-RES-1/RES-2 and the corresponding R585-17 residue remain applied. The newer native environment changes one mutant's failed-check count from 32 to 35, while its caught verdict is unchanged; the coverage comparison with dev is exact under that environment.

Supplementary store `--self-test` attempts reached the 570-second command limit and are not counted as passes; no complete 109-mutant store claim is made. Round 18's required store command omits that option and passes all 435 tests. The separate BIOS classification scope is stated above for review.

The tree and both submodule checkouts are clean. This head needs independent review and protected hosted contexts after publication; prior positive reviews cover `27ee16b5`. No push, PR edit, merge or hardware operation was performed.
