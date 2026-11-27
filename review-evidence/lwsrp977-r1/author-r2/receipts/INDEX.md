# Receipts: kebag-logic/lwSRP PR #22, round 2 (head 50a2106483141fcd7d1b20654bcf0803e7c3020a)

Every gate ran on its own clean clone of the head (`scripts/gate.sh`, reruns `scripts/gate-r2.sh`). Paths inside the
logs are this host's scratch paths; they are local receipts, not for publication.

| Receipt | What it shows |
| --- | --- |
| `gates/suites-OFF.log`, `gates/suites-ON.log` | host build, ctest, unit_tests (27,348 / 27,336), behave and its dry run, both profiles |
| `gates/units.log`, `gates/units/` | 18 unit builds (default, scale, end-station with and without scale, each switch alone; both profiles), all rc 0 |
| `gates/codec.log` | the isolated codec command, 1,690 passes |
| `gates/diff-OFF-r2.log`, `gates/diff-ON-r2.log`, `*.differential.json` | the differential, both profiles, with MemorySanitizer: 22 builds, 39 of 39 plants (38 + the sanitizer's), 0 problems |
| `gates/rev-OFF-r2.log`, `gates/rev-ON-r2.log` | reversal default runs: 118 listed, 110 selected/run/killed, 8 skipped |
| `gates/rev-key-*.log`, `gates/rev-es-*.log`, `gates/rev-es-noscale-*.log`, `*.summary.json` | reversal runs with --scale ON, --scale ON --end-station ON, --end-station ON; both profiles |
| `gates/eq-OFF.log`, `gates/eq-ON.log` | equivalence, both profiles |
| `gates/eqc-OFF-r2.log`, `gates/eqc-ON-r2.log` | equivalence controls, 5 of 5 each |
| `gates/baremetal.log` | check_embedded; check_freestanding with five switch sets |
| `gates/objects.log` | 8 sources x 8 flag sets against main: 64 of 64 byte-identical |
| `gates/inventory-r2.log` | no Python cache tracked; 74 tracked files, all text, none generated |
| `gates/docs-r2.log` | sentence, reference (and self-test), link and graph checks |
| `gates/summary-reruns.txt` | rc of the six reruns |
| `named-failures.txt` | the named tests each end-station reversal fails, both profiles |
| `added-lines-scan.txt` | 0 labels or private paths in the added lines; commit subjects, no bodies |
| `probes/sparse-word-probe.log` | the scan-ending defect: SURVIVED with 73007b48's driver, KILLED at seed 3 with the new one (lean-tx and end-station, both profiles) |
| `probes/reversal-count-plant.log` | a planted silent skip fails the reversal runner (rc 1, `selected but reported no result`) |
| `probes/objects-with-debug-info.txt` | with -g, 24 of 24 objects identical after `objcopy --strip-debug` |
| `superseded/` | the 73007b48-era object comparison (61/64 before the fix, 64/64 after 7ca4a6f) and the gate logs broken by harness faults, with the first batch's summary |
| `scripts/` | every script used: gate.sh, gate-r2.sh, units.sh, objects_identical.sh, sparse_probe.py, repoint_anchors.py, log_diff_rm.py |

## sha256

~~~
f3a07ca02371cbacd7bd513bd1dfb6fb77caff3347207f193613b109f7ad7897  ./added-lines-scan.txt
e42d21e3b10708c292ea78dc869e98ea88bfc8cd4784a0bc1d82202a9a4b3dee  ./gates/baremetal.log
dd43d7a8541639b48c7dd837c2eaa00b62c99935d395d482a53a51e73335a69e  ./gates/codec.log
74d0a3c7082bcb8f8f55208d14d4720cfd2ed42c5e4cb66635cf16a39c71d63a  ./gates/diff-OFF-r2.differential.json
71247682c1017ed35565ce0c1d28ae189f63548cf355f982842cb10d9c5f6040  ./gates/diff-OFF-r2.log
bccbc5cd6e0cd9c762fd9acd3f20ee6d2a89cb332e0daadb9382c03997c6e1ba  ./gates/diff-ON-r2.differential.json
80c9273babbcbb9e19668219811b6b1f7e41d5bce68d6ec03d12c54b641c1d48  ./gates/diff-ON-r2.log
1c45df790f4173a184fe45b9c0fb4f1723f7e271dbe7d258c805e8176b6f4e79  ./gates/docs-r2.log
444fbba26b210a7a4fa3efc5f9ccde408187bb3ed0c426530eb94e04f87b1a95  ./gates/eq-OFF.log
49835304a58c8b0ed7a7a956a03aca053e8756fc0e729d8939d4e3c98fd0b108  ./gates/eq-ON.log
cd2ce409b87d78e019681a3c260b59e895c91598a8907c12d48dfbe1b18c9a79  ./gates/eqc-OFF-r2.log
fe9cf9c5d45e18f8a4cc7b43905bca73753e6f3764c88064ce7fefb8f4961ea3  ./gates/eqc-ON-r2.log
5337840c12a57dab3a4b8e738c317e9cc88b6db9614de96688545487724820ed  ./gates/inventory-r2.log
2b3f71d0021532a9e841a993459a06e04e2857ebd864eac1369ef708b05bd72e  ./gates/objects.log
abe5f66eed558ca97615446cf892e59ff06804183e71ba751375cf5c9c68e8b6  ./gates/rev-OFF-r2.log
42d326a9a3db053d30535d3a96337e17bfd817c44837587b335deb67c8f248dc  ./gates/rev-OFF-r2.summary.json
b4d464563534feb6164abb417db2ec6093c5832f37aa60cc29b0e6774845f156  ./gates/rev-ON-r2.log
3546b1f9dc38fd21d0996d984f73293dd17f51c22d2002a729c79c4955dd3924  ./gates/rev-ON-r2.summary.json
5c6c5bb67f7dd60a6fa0d52969ac996baf9d30f9363c289bdb92dc14ac407782  ./gates/rev-es-OFF.log
dbdd2cc7c0e91140d72bcbe6b40fcb26fd9ffa3c66c1f3833938ae739b4d7107  ./gates/rev-es-OFF.summary.json
79dc918aee9220efcd0e6fea6012bc36cef311890600e5641fbb43298b6e7018  ./gates/rev-es-ON.log
89d03f7d37f2499b934bec2336721320ce4afb5b65708718f5ed1099e7c079cc  ./gates/rev-es-ON.summary.json
bde5d7e8395d6071c9d719a1e4331f3bba9251c1350852cceb05857c8dd0e9c4  ./gates/rev-es-noscale-OFF.log
54d2804eeb0f1e967dd6e1dbb6f9ce69a52b51ce564d45186665c356c1b662d6  ./gates/rev-es-noscale-OFF.summary.json
2a3ef172da92de54129d432511927838ac92cdea2754d3c8a65252792bbaeeec  ./gates/rev-es-noscale-ON.log
e14befcb9ebe9da0a926a4648b1db36ca56ab65a12c7a8db7d26c8f0d086259f  ./gates/rev-es-noscale-ON.summary.json
9cc1ef76a3690309aa847b76ee2abaf1f9f2bcb25be450f34754101bd526f7f7  ./gates/rev-key-OFF.log
9ac0dc3757e368507cb5c1af1c4e33b3cfe9638cf2765b218658430423e74f22  ./gates/rev-key-OFF.summary.json
9fb7cd49b768e37ddd11a0896eaa7de77c8c8bbf408cefefbf19b17484c04294  ./gates/rev-key-ON.log
2f102f0c7234cabda890de36776606e97c600c14ba949989671477cc29e51578  ./gates/rev-key-ON.summary.json
27d03b9552c81f25eb62b4a154665c07c23c18fbb5d702be8db7f4ae42a91fb5  ./gates/suites-OFF.log
5b4cf979a2f179d20cef987ec93d74ff3e566c845c3aad0251bdd9e4c43fafc5  ./gates/suites-ON.log
66427ef050edacf1562daeac13ff15da07134f69bec9b9cb562c9cfbcadc33ad  ./gates/summary-reruns.txt
c98df2832fec70578214143d2ab25cdf6641c6c3e6e0da562761e2c152c94ca2  ./gates/units/default-milanOFF.unit.log
76dcceed9479c68f9b229005c74e94eb7dfe869a36ce42612607f961d345d7d1  ./gates/units/default-milanON.unit.log
4e1f2af8394a32d86319bb5194a35113740d328953d53570b0dfdaeebe82b465  ./gates/units/end-station-milanOFF.unit.log
c4dc89267865ac8e47e2964ecf3d7828b92a8b3bc289f3aa2f6ce1b3e01e0e2e  ./gates/units/end-station-milanON.unit.log
9b29b14f2226ade00b0013773abc264a8693646101531103c897d8deb8383365  ./gates/units/end-station-no-scale-milanOFF.unit.log
81fc0878132d5894377c1248721811587ca31725013d95f70ab82c6c4c6033dd  ./gates/units/end-station-no-scale-milanON.unit.log
c80873219d0bbe8f5646bf317437c22e24e0a1d2b6bbbe5e4cc220f8cd93aa59  ./gates/units/lean-copy-milanOFF.unit.log
f9e1ee4128b9aebaa4f0f81eaddc87362b63085551fab3fa79c78ab145f3bfa8  ./gates/units/lean-copy-milanON.unit.log
5c9c448a63a6930598d4adb0170d18bc28178bdce82fa3a6836783d54fbae662  ./gates/units/lean-tx-milanOFF.unit.log
aaefe83ef5370b7c29f0afb753152d56b21142c8090657a555c3aa44906d486d  ./gates/units/lean-tx-milanON.unit.log
62434d21d57699f4b807f227d4ca489e31ba064de6843344895eb2095100c154  ./gates/units/lean-validate-milanOFF.unit.log
8326ef903cb0097113cff0fe0e10d0d1a33c86c418c0b87d6bdf65a4d01168e4  ./gates/units/lean-validate-milanON.unit.log
7b37537ded3c7f89b3da052058e8141cbbcf82340097a120125e5d893221abde  ./gates/units/one-port-milanOFF.unit.log
521fb3fe32ad0e8c42af6a2dad66679ba838600033a2d8ebd4a90f7f43acfdac  ./gates/units/one-port-milanON.unit.log
f677c0cd1df18cf0505605c5185458208c930b706b2cf10b75c68d0be4e3a8e4  ./gates/units/rapid-replace-milanOFF.unit.log
a44500965364cdab5240aff139d4b7be20db61f122b4c56d3e6c9e46f90f24ed  ./gates/units/rapid-replace-milanON.unit.log
d7db3824ef2c3119ee0292a55363c9cda6e3e32b4e88b92d58a92e6cd555cb7a  ./gates/units/scale-milanOFF.unit.log
45243a39bde31b19403b11eddc087ac446982ffde6269bf2227b16ec10954fda  ./gates/units/scale-milanON.unit.log
8775056603efeec795d071c2c75a194c89ab83fa5c56eefe5474c40ca0d70adb  ./gates/units.log
e09665366fc3470638dc34f27153a132eb82a9e112db44ecdd15de2b5f08e66b  ./named-failures.txt
18ea5591c9b7dc56cfd5e3aa445d1490011e18dcd627a66be9796db1bd8ce030  ./probes/objects-with-debug-info.txt
d2d7a94f8aac7883198a46fd9cf03eae5038e475cbe72288f985d70a655941ab  ./probes/reversal-count-plant.log
e34c145a406e3beb818fb81487c7ef47b716e218f3985232b4b6ed4aea5d6120  ./probes/sparse-word-probe.log
42c3738ea01a4a07370468729275409e8a6c157471a34f438709d7e3c5229d36  ./scripts/gate-r2.sh
42c3738ea01a4a07370468729275409e8a6c157471a34f438709d7e3c5229d36  ./scripts/gate.sh
5de6763358e75c457cd5140fb793e0b64b2a674e6f306f47b0a92865a2fd122f  ./scripts/log_diff_rm.py
954bcac575d43a90d2c7a6a32bd155ff5d3d0499dcb314b2bf2195d9d3bfecf4  ./scripts/objects_identical.sh
f2918ed7d6c8396f683bcea99ef2175ac50dba1a76e6e0f743edfacdbd9ba587  ./scripts/repoint_anchors.py
d5eddbefff4103c149ce052a08e589a493e0e7d47d3d7dc6795d2077d75e0455  ./scripts/sparse_probe.py
b6c821ea63e506523f014471e90055bc53940e34fb98abb7a85074f4f6da7e69  ./scripts/units.sh
5c8790637f11c8bcdbeafcdecdd326a1f0813974f2ff0da3953a443146d096cf  ./superseded/gate-diff-OFF.log
bab160d380a9c4b94f4b55b49d87fc981230108dd0707bdeb00bc9118b2e8d48  ./superseded/gate-diff-ON.log
9672c707c7adb853a010ec2e5c6e67750f0b4c411d3913fa11f6f436be410c3f  ./superseded/gate-docs.log
4430451929dd2d898d0c5b6dc257160d73ff22a9a976639650529e7b08cbc47e  ./superseded/gate-eqc-OFF.log
e6b67b77ec15d15829e9a4ec2ce35842f772186e2a6f1340fa095254c0269be9  ./superseded/gate-eqc-ON.log
e0c3902e18f9dbbd92ecc969d572f6a47af1ecb184efd0020a02bbedf6271162  ./superseded/gate-inventory.log
6ef0def459195fc25b816fd3888e53d979538c913ace09951940af90448a5f3f  ./superseded/gate-rev-OFF.log
14b8389b8d1350b415a0d67e84ac1a78ff5a852e556d3e8d9639574479a422e3  ./superseded/gate-rev-ON.log
b05dac9a1ec3f4dd34f482ca1506f54261a53cd926a8c8b83fe05960b0411092  ./superseded/gate-summary-batch1.txt
9d1505d70ed821b883ef0150588d9c9080bb2dc68b8c753b5b82f9e08e5e447d  ./superseded/objects-identical-at-73007b48.txt
6a26dff05edc2a658307efb7d24ec8ac0af0588954a847d591cbd63c03e5bd8c  ./superseded/objects-identical-at-7ca4a6f.txt
~~~

Manager note (publication): line 4 of `added-lines-scan.txt`, the scanner's literal pattern list, was replaced before publication because it named tool tokens the public evidence rule refuses. The text now reads "pattern: review and lane labels, comment IDs, host paths and tool names (case-insensitive); the literal list is kept privately". The gate's results in the rest of the file are unchanged. The author's original hash was `f152030f313134a22871be707affa711c79c7221ff50859a2c5020be452c3839`; the line above gives the published file's hash.
