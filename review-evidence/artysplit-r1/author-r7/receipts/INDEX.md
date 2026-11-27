# Round 7 receipt index

Head `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1`. Image and census at `74f942be516b84915f7d982fe1e3c65b497c227a`; the two commits after it change `docs/` and the receipt regrader only.
Prepared locally; nothing has been posted or pushed.

Every receipt is UTF-8 text below 190,000 bytes. A manifest records each numbered part and the
SHA256 and byte count of the whole before and after redaction of private paths and host headers.
[FILES.manifest.json](FILES.manifest.json) and its numbered `FILES.tsv` parts list all 22866 other files with bytes and SHA256.

## Reproduce

From a checkout of the head: `python3 tb/verilator/ctrl_service_budget/receipt_regrade.py <this directory>`.
It checks every part and whole hash, reproduces all 147 case grades from the extracts, reapplies the cross-case
checks, held-egress ledger and owner model, and regrades every timing corner. Allow about 4 GB of TMPDIR.
Its own log for this packet is [validation/receipt-regrade.log](validation/receipt-regrade.log).
Before its fix it refused the five lines #977 owes ([validation/receipt-regrade-before-fix.log](validation/receipt-regrade-before-fix.log)); a control packet without `srp-bound` is refused by name ([validation/receipt-regrade-control.log](validation/receipt-regrade-control.log)).

## Source

- [source/round7-commits.patch](source/round7-commits.patch): the four commits of this round.

## Primary timing reports

| Directive | Report | Original bytes | Original SHA256 | Manifest |
|---|---|---:|---|---|
| ExtraTimingOpt | digilent_arty_signoff_Slow_0C_timing.rpt | 1324232 | `b937e97f861510d94e4d0cd12d97370ce6be2ba073b5c6e740ea25913119681a` | [digilent_arty_signoff_Slow_0C_timing.rpt.manifest.json](timing-r7/ExtraTimingOpt/digilent_arty_signoff_Slow_0C_timing.rpt.manifest.json) |
| ExtraTimingOpt | digilent_arty_signoff_Slow_85C_timing.rpt | 1324235 | `5a83adaffb32afe5546cdf5648a593ec9ef9615e833878acfa5481b2e8ebf3b5` | [digilent_arty_signoff_Slow_85C_timing.rpt.manifest.json](timing-r7/ExtraTimingOpt/digilent_arty_signoff_Slow_85C_timing.rpt.manifest.json) |
| ExtraTimingOpt | digilent_arty_signoff_Fast_0C_timing.rpt | 1319386 | `2ad47ec002403c592df31448b7ca645765788a659453c89cd45b843dd26644fd` | [digilent_arty_signoff_Fast_0C_timing.rpt.manifest.json](timing-r7/ExtraTimingOpt/digilent_arty_signoff_Fast_0C_timing.rpt.manifest.json) |
| ExtraTimingOpt | digilent_arty_signoff_Fast_85C_timing.rpt | 1319389 | `94fe39dadafc53d2aef38da72a30a0dd0f0809b5fb77220b5898d998a06ffc08` | [digilent_arty_signoff_Fast_85C_timing.rpt.manifest.json](timing-r7/ExtraTimingOpt/digilent_arty_signoff_Fast_85C_timing.rpt.manifest.json) |
| AltSpreadLogic_high | digilent_arty_signoff_Slow_0C_timing.rpt | 1324232 | `a40a4aee2404399f2913b7d19379e4fd4d960b915a148d6d5b6a078f90c81b7c` | [digilent_arty_signoff_Slow_0C_timing.rpt.manifest.json](timing-r7/AltSpreadLogic_high/digilent_arty_signoff_Slow_0C_timing.rpt.manifest.json) |
| AltSpreadLogic_high | digilent_arty_signoff_Slow_85C_timing.rpt | 1324235 | `31c61606c8ea99a79763fb7f25f0a1b1921d253e4e3d18028c3b41ae7a9357c4` | [digilent_arty_signoff_Slow_85C_timing.rpt.manifest.json](timing-r7/AltSpreadLogic_high/digilent_arty_signoff_Slow_85C_timing.rpt.manifest.json) |
| AltSpreadLogic_high | digilent_arty_signoff_Fast_0C_timing.rpt | 1319386 | `9d777698229e6f6f381af15f10ef8111f639be0803f9033aa782006ffdc6f713` | [digilent_arty_signoff_Fast_0C_timing.rpt.manifest.json](timing-r7/AltSpreadLogic_high/digilent_arty_signoff_Fast_0C_timing.rpt.manifest.json) |
| AltSpreadLogic_high | digilent_arty_signoff_Fast_85C_timing.rpt | 1319389 | `c8ea729e97cb6f50e9a766536500b907ab5719add57b9078e7b754df9697a390` | [digilent_arty_signoff_Fast_85C_timing.rpt.manifest.json](timing-r7/AltSpreadLogic_high/digilent_arty_signoff_Fast_85C_timing.rpt.manifest.json) |
| ExtraPostPlacementOpt | digilent_arty_signoff_Slow_0C_timing.rpt | 1355948 | `165c83562a72375ae53a9cb78b0ecb542cfeae7421062d304b7f86d4495d470f` | [digilent_arty_signoff_Slow_0C_timing.rpt.manifest.json](timing-r7/ExtraPostPlacementOpt/digilent_arty_signoff_Slow_0C_timing.rpt.manifest.json) |
| ExtraPostPlacementOpt | digilent_arty_signoff_Slow_85C_timing.rpt | 1355951 | `995e94b6c73bc11d81db205dfead5417026bc615bb13a1212267a0c85c9cd009` | [digilent_arty_signoff_Slow_85C_timing.rpt.manifest.json](timing-r7/ExtraPostPlacementOpt/digilent_arty_signoff_Slow_85C_timing.rpt.manifest.json) |
| ExtraPostPlacementOpt | digilent_arty_signoff_Fast_0C_timing.rpt | 1327652 | `b7ed888e71ba529c59fe0b07e31b301b9a6ef8738bd1587afb3b5f23802be0b9` | [digilent_arty_signoff_Fast_0C_timing.rpt.manifest.json](timing-r7/ExtraPostPlacementOpt/digilent_arty_signoff_Fast_0C_timing.rpt.manifest.json) |
| ExtraPostPlacementOpt | digilent_arty_signoff_Fast_85C_timing.rpt | 1327655 | `d8ba60229b3bb77aa71b63f10a48a515082a8fec6d22aaf58dd8bbe0c8d0ebe2` | [digilent_arty_signoff_Fast_85C_timing.rpt.manifest.json](timing-r7/ExtraPostPlacementOpt/digilent_arty_signoff_Fast_85C_timing.rpt.manifest.json) |

The grader verdict is [timing-r7/graded-images.json](timing-r7/graded-images.json); utilization and check_timing reports sit beside each directive's timing reports.

## Validation logs

| Receipt | Original bytes | Original SHA256 | Parts |
|---|---:|---|---:|
| [step1-install.log](validation/step1-install.log) | 1057 | `7f825706f0ee4d529d3b2e5350ee9b8d9dc7f9eccdf564af0e91448fd6a58495` | 1 |
| [step1-arty-grade-installed.log](validation/step1-arty-grade-installed.log) | 998 | `40977db1129f6b8d75c0895fcc6ad6c243bb207e10327bc2674dfde4b9e95dcc` | 1 |
| [step1-arty-grade.log](validation/step1-arty-grade.log) | 998 | `40977db1129f6b8d75c0895fcc6ad6c243bb207e10327bc2674dfde4b9e95dcc` | 1 |
| [step1-standalone.rc](validation/step1-standalone.rc) | 93 | `2b3ad19da2e087e1919e83ae68c9a0d938c0935035c6c32c5dded1257e7803ce` | 1 |
| [step1-census-build.log](validation/step1-census-build.log) | 5965 | `5eef1271d12ca6954985ede57f079616ba643fa9110c0c69d1f2018487cc4855` | 1 |
| [step1-census-w1.log](validation/step1-census-w1.log) | 8204 | `c6fbece15ad10269c4b23d727485c08a2580140ff041bcfbb31023f29d2d8a29` | 1 |
| [step1-census-w2.log](validation/step1-census-w2.log) | 8206 | `c05e6e8d65cb1e18e8ebbb3f30da496f38d378e9fda44324470768ddf6a2eafe` | 1 |
| [step1-census-w3.log](validation/step1-census-w3.log) | 1576 | `388030ffc83ed0d716f7d60f98c0228c9aefe55c46891b594f2d0ce4305c27bf` | 1 |
| [step1-kept-grade.log](validation/step1-kept-grade.log) | 2720 | `95e43484676699775bd68112d85db45d319748ecd3ec09c30da0eba2a2802696` | 1 |
| [step1-qualify.log](validation/step1-qualify.log) | 13613 | `c51bdf8a47cdf29f9edd0b7dc3663be815b95106bdf4b9e7c752f195b4d1d297` | 1 |
| [step1-install-step2.log](validation/step1-install-step2.log) | 1057 | `d3f9a8ff63bac20ff0e3a7f80d3840830648ad575a043b6698fa0ee26e99d2f5` | 1 |
| [step1-arty-grade-step2.log](validation/step1-arty-grade-step2.log) | 998 | `3a7b686b53bea7460a736c97554d2b1a7de4730d9801057936fb19b2e9a00e9c` | 1 |
| [step1-gates.log](validation/step1-gates.log) | 657 | `274d37244d5508cb51e35260872c28890dfcdb0b612aae4bc3e83b2832e5fffe` | 1 |
| [step1-gates-results.json](validation/step1-gates-results.json) | 5542 | `c045e6242d23d3894dfc7f874ad9e8cea98cf1e9023aa6bed2d00905852871b9` | 1 |
| [step1-route-window1.log](validation/step1-route-window1.log) | 135 | `f895ab9356a4e4c9de22a89ddf97c222f25c8bedf67f7fd20eb5d242e3b4f4d0` | 1 |
| [step1-route.log](validation/step1-route.log) | 97 | `8f71e3439aa6cc16dac120297a31ed405008bed7700fd6a4708f890e81e4ba8c` | 1 |
| [step1-grade-images.log](validation/step1-grade-images.log) | 20737 | `34242c5557b4b3f27e42333850701dda063e33e3aacb9cd1e9b2f6824e67c7c7` | 1 |
| [step1-service-selftest.log](validation/step1-service-selftest.log) | 104 | `25624f3bfa4d1b572701c7f513eaa09f61d22e1e7da1ff70fad5d7a360278dc4` | 1 |
| [step1-host-tests.log](validation/step1-host-tests.log) | 6496 | `34b9afbb5bcddb18f9e8c1d055a47cc89b154fc6f05bd336fd83e1ff75bc1e7d` | 1 |
| [step1-product.log](validation/step1-product.log) | 4779 | `1b24d34adadfbede70342676d3affab26e1c0f7a6a62825b3334f5fe8f809b7c` | 1 |
| [arty-grade.log](validation/arty-grade.log) | 998 | `3a7b686b53bea7460a736c97554d2b1a7de4730d9801057936fb19b2e9a00e9c` | 1 |
| [standalone-rows_tiers.log](validation/standalone-rows_tiers.log) | 50 | `83ca997dc47de52454b3574a6f71c705c8d0906a1cf96432602c9ea6893a9463` | 1 |
| [standalone-load_grade.log](validation/standalone-load_grade.log) | 45 | `43d9de9746dd458086aeaa66b99633bf052569ae5356268600f4950e60519d71` | 1 |
| [standalone-egress_ledger.log](validation/standalone-egress_ledger.log) | 20602 | `5f1f95f6e9a355544b33c2af6e9592b6351cc89ab0abc99e6ca2a7ca60eb1d81` | 1 |
| [standalone-record_classes.log](validation/standalone-record_classes.log) | 138 | `f493ee9e4703ef5d1d8e5fd86035ca96559174ce38bae1f5d0a52d6aab3c64c4` | 1 |
| [standalone-arty_grade.log](validation/standalone-arty_grade.log) | 482 | `57281920afb5403673d5b28567f2e456466ddec1fc003de31e60a674ec35d23a` | 1 |
| [standalone-egress_ledger-final.log](validation/standalone-egress_ledger-final.log) | 20602 | `5f1f95f6e9a355544b33c2af6e9592b6351cc89ab0abc99e6ca2a7ca60eb1d81` | 1 |
| [standalone.rc](validation/standalone.rc) | 112 | `beff87f6a956ad9cf7549dad077e73e430327ebcf470e2c8ce4bf57be7184790` | 1 |
| [test-ctrl-memory.log](validation/test-ctrl-memory.log) | 60636 | `247c35cf44e351dfee187dd88302422562dc3c7eae9e5642d5dede6fd69ce667` | 1 |
| [service-selftest.log](validation/service-selftest.log) | 104 | `a86b445e747ba7d7db86ce84cdb4e5df88dfc3187f6ab10e95c3038ac915bc3c` | 1 |
| [service-selftest.json](validation/service-selftest.json) | 331 | `3a7ce61e8963d32a7bdbe4468bcf0ca15a68bbc8e20375887cf33217858faeef` | 1 |
| [service-selftest-0.log](validation/service-selftest-0.log.part0001.txt) | 203943 | `ef141a73b713877103adfc80257f067e5bf030f0f364a1fb7eb6eef000054bdf` | 2 |
| [service-selftest-1.log](validation/service-selftest-1.log.part0001.txt) | 202346 | `c3dbeca603be9eb14e1c3e3a674893e2a38d27854209886b1680159fe610e128` | 2 |
| [service-selftest-2.log](validation/service-selftest-2.log.part0001.txt) | 199840 | `8d2bc7bdc501678a64ad472e5fdd04d0afec851fd72af24034dff3862a564fec` | 2 |
| [service-selftest-3.log](validation/service-selftest-3.log.part0001.txt) | 201747 | `0e79563dd8a3e06e15b1920f188932174be24ba0cc2bf599343914aaa3aef5e4` | 2 |
| [service-selftest-4.log](validation/service-selftest-4.log.part0001.txt) | 197640 | `797f82bafd43e6369e44754454baa319348fd93c507d7448e39594154e0fc63f` | 2 |
| [service-selftest-5.log](validation/service-selftest-5.log.part0001.txt) | 189044 | `f2a1e3fb67584db5d76d6f50c6c49b99855c8d24290fa0a76195fbe43e739479` | 2 |
| [service-selftest-6.log](validation/service-selftest-6.log.part0001.txt) | 201121 | `7f4b26941f6a3b6a78d0cd598d5fff64369c7b864495a17e8dc379dd320f611e` | 2 |
| [service-selftest-7.log](validation/service-selftest-7.log.part0001.txt) | 199148 | `f5348259799165a2f975d3f2b90ae1794eb57eddc63a5b1ebcf8bb1df8a819e9` | 2 |
| [host-tests.log](validation/host-tests.log) | 6496 | `34b9afbb5bcddb18f9e8c1d055a47cc89b154fc6f05bd336fd83e1ff75bc1e7d` | 1 |
| [host-results.json](validation/host-results.json) | 279 | `285903847ec05241df26baad00b49d77bf959a197c6fe8e7f534c79be5833905` | 1 |
| [host-console.log](validation/host-console.log) | 4708 | `c71ac372ec232586471bb2e3c1ea15f93f4579956fd3af9db5f35b872a808788` | 1 |
| [host-mii.log](validation/host-mii.log) | 1700 | `b9b669455ba3e26478edbaf7fd3b5ffbdaebf8da37e5a6c944064be81b9a4d53` | 1 |
| [product.log](validation/product.log) | 4779 | `1b24d34adadfbede70342676d3affab26e1c0f7a6a62825b3334f5fe8f809b7c` | 1 |
| [product-link.log](validation/product-link.log) | 2273 | `f679e40680f03645e1b831401fd6ecbed2524ebf2da132f067f4546c097525d6` | 1 |
| [product-size.json](validation/product-size.json) | 1876 | `cfff85ee02a91de3566606bf0b2190fa101068dd5405f932b2293ce02e130022` | 1 |
| [route.log](validation/route.log) | 159 | `33c293e994a6eed193cb0c7bec2d1c6092e6b51a83e526673b7a20df54948aef` | 1 |
| [grade-images.log](validation/grade-images.log) | 20737 | `769627adb6007d90a431125b850413dfc01b1113d3508861fbe9067b1a38d7e9` | 1 |
| [images-inputs.json](validation/images-inputs.json) | 146 | `70f954fabd8d78c01beffcc8691feca3f74f8e3c6dabca74d26791834fa7b74e` | 1 |
| [census-build.log](validation/census-build.log) | 5965 | `5eef1271d12ca6954985ede57f079616ba643fa9110c0c69d1f2018487cc4855` | 1 |
| [identity-raw.log](validation/identity-raw.log) | 8486 | `b5a150516302f4bcadcc690c3fc68ba4fb67736483c42184b6a0b22d821332d3` | 1 |
| [identity.log](validation/identity.log) | 3749 | `82aee2f3ed66331051950ec52765c0493c155ca89bac95c3daef6a7de2e05eef` | 1 |
| [reuse.log](validation/reuse.log) | 7088 | `e98cc01f57d923c00a03b0fb5f6a12441db39774790f30c227dcf850f246ede2` | 1 |
| [qualify.log](validation/qualify.log) | 13459 | `512739b889dafa69808d24021aef0944f170eacef676b6861c745ef1e350cd42` | 1 |
| [receipt-regrade-before-fix.log](validation/receipt-regrade-before-fix.log) | 14168 | `680c67ce20e06b7887125458fcd4397ba977ffaba884051af80175cf216e3935` | 1 |
| [receipt-regrade.log](validation/receipt-regrade.log) | 14990 | `98a1a7cb91ba9f4b643f7a81b7746c62bfbf64ec0a72e0dfa386b3993027865d` | 1 |
| [receipt-regrade-control.log](validation/receipt-regrade-control.log) | 14186 | `e71901a23f9ad3d6764e0ca5dccced7f6d86076279d7d3966d2bee89858161ea` | 1 |
| [gates-74f942be5.log](validation/gates-74f942be5.log) | 657 | `53f43fafb23375e2fd2b8fcf7293d21a4465eb9fb3bb6bde69e1a18f13a52766` | 1 |
| [gates-2d911d2bf.log](validation/gates-2d911d2bf.log) | 515 | `ee2a74c1b25e87a8cf92525bde3c75ac55a4403d3576bd2958d1413c3d0e010f` | 1 |
| [gates.log](validation/gates.log) | 515 | `4775f7af9034e60ea7949277067df5ea4c7741489006eeaeed7125920d5fc3a7` | 1 |
| [gates-results.json](validation/gates-results.json) | 5542 | `b2ae3ec5b5518a36e422054bee7693d483b9fcc5e67734460b7c849792069657` | 1 |
| [firmware-0.log](validation/firmware-0.log) | 100615 | `9f49ed38016349eb85fad53f4437c160e53fc3e6b9174b7be72320efc8015a88` | 1 |
| [firmware-1.log](validation/firmware-1.log.part0001.txt) | 241311 | `dc431aa4bed490467614c1ab6641649d1d7836d73b216e673b85089d65857255` | 2 |
| [firmware-2.log](validation/firmware-2.log.part0001.txt) | 372411 | `880ae6027e8eddbad955f368809df871779b2f7cafd49172a66f4c29c5a53476` | 2 |
| [firmware-3.log](validation/firmware-3.log.part0001.txt) | 308162 | `04a2ca7e422e288a5e3bf2c130129a7ca6a77996adb4f922ef07e6e9ac3962ba` | 2 |
| [boot.log](validation/boot.log) | 11359 | `365c322ecaeebdeff127a04938afd52238c3d78d623f9b179b2c7afcb702ed37` | 1 |
| [boot-native-controls.log](validation/boot-native-controls.log) | 1758 | `526018ad8a8209da4d8bce9e7b3791cdc665b31d3c9bed3423713a42c2498905` | 1 |
| [region-controls.log](validation/region-controls.log) | 14987 | `4af033c3189e96be36dd7b7c1fdbf1f719ec0a372bf124ba64f7d449681c7e81` | 1 |
| [docs-check.log](validation/docs-check.log) | 128 | `c3243754c3f1a2c5a47df6174a87c0aaa3aa2ebbfb4838871ea1f470261a8f60` | 1 |
| [doc-style.log](validation/doc-style.log) | 47 | `680272641877f342dfde0fc85b7cb5d14558ba6da7b9162d9ff1d23b79f2f311` | 1 |
| [doc-paths.log](validation/doc-paths.log) | 101 | `fe5cda5b78bc69d3badbc4b4fb019ad522bf5c14359196911c94265086e93da6` | 1 |
| [gptp-docs.log](validation/gptp-docs.log) | 41 | `d8a77a32600566f0613626fd361bad845759693a08b1095dd54865c1aa25455d` | 1 |
| [inventory.log](validation/inventory.log) | 78 | `5d6785e7760826a37829426bb12c7fd4d7f81eaf467660978a0d986b1958faa5` | 1 |
| [idiom.log](validation/idiom.log) | 461 | `686570e482e0f581005713ab3e7f7cb8a5f4cac638c882be2f3362197cdcfcc0` | 1 |
| [cpp-idiom.log](validation/cpp-idiom.log) | 316 | `119a4859c80431a111c8f2903c1c16373c97fcbec5f7f3418922023f90f9aff5` | 1 |
| [em-dash.log](validation/em-dash.log) | 141 | `8d7d671cb18e2e95ef1680a21f500fe7988cdea9c158d6bf8543f7c94536c767` | 1 |
| [toc-check.log](validation/toc-check.log) | 94 | `40f80cdafa6ec01e04d1fd374885a9af8dffb83ab79900a6d9841fd7b9c613c8` | 1 |
| [toc-verify-anchors.log](validation/toc-verify-anchors.log) | 64 | `796bae51405022dbb87285d50c307c1aead4d576ab66e3e313da5f0768fb9f95` | 1 |

## Native census

[census.json](census.json) lists all 147 cases at `74f942be516b84915f7d982fe1e3c65b497c227a`. Each case manifest binds the full
local trace's size and SHA256, the observation extract, the scenario, the stimulus and the original grade.
The traces were measured at step 1 (`f7b90e3b7`). Step 2 changed no firmware byte: every native executable, firmware
ELF, flash image and stimulus is identical, and the build inputs differ only in generation dates
([validation/identity.log](validation/identity.log)). So the step-2 census regrades step 1's traces
([validation/reuse.log](validation/reuse.log)).
Qualification command logs and results are under [qualification/](qualification/) ([manifest](qualification/manifest.json));
[published-qualification.json](published-qualification.json) is the qualification the regrader compares against.

## Derivation

The installed model of each step and its inputs (round 6's merged maxima, the round-4 control derivation, step 1's
cost census and qualification) are under [derivation/](derivation/) ([manifest](derivation/manifest.json)).

## Recipes

The orchestration scripts, redacted, are under [recipes/](recipes/).
