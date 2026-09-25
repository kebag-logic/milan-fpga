README (490e430) tb/pp_top/README.md:505-522 quotes, scoped to b51bc38: 7,660 total = 7,640 default + 20 fixture; word-560 SUCCESS mutant 197 of 7,640 (M4 10); word-741 features=3 mutant 3 of 7,640 (M1, M2, M5b).
Reviewer's own round-1 receipts at b51bc38 (published with R319-1):
-- pp_top-head-run.log sha256 5a066cad057722fdc948d1b1b926f8213e33afb0e065066bbd046e4a1266cfad
[build fixture, SRP_DOM_DEF_VID_P 0x5a3c] 20 checks, 0 failures
7660 checks: 7660 PASS, 0 FAIL
-- probes/rom-notimpl-success.log sha256 0970f50b97ae0d054f4c0f53d104c57ec112f97969dc7628751fe20aedc3f638
GI latency walks added: 5568 checks, 0 failures
[build default, SRP_DOM_DEF_VID_P 0x0002] 7640 checks, 197 failures
-- probes/rom-features-3.log sha256 098c4abc1c4ecafb7ce728be18a5e248cdabb9b75915503bc83c1e17b121bf51
GI latency walks added: 5568 checks, 0 failures
[build default, SRP_DOM_DEF_VID_P 0x0002] 7640 checks, 3 failures
-- M4 failures in round-1 SUCCESS mutant:
10
0
