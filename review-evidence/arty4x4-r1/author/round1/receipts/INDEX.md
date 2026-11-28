# Receipts, Arty 4x4/1if round 1

Local only. Paths are relative to this directory; scratch copies stay in `$VALIDATION_STORAGE/arty4x4-a863`.

| File | Bytes | SHA256 | What |
|---|---:|---|---|
| `arty_grade-1x1.log` | 1021 | `9bd33a43c579374886db2e67573d7dfe2a727c3c629266133f0b5dde11966926` | Gate or self-test log |
| `arty_grade-4x4.log` | 1862 | `7b22f3fe7ab1a1cf1c4e24601c3ad393e62a433b82b7a3c029f349a498fbe63c` | Gate or self-test log |
| `boot-1x1.log` | 11554 | `f9944a3ba21419674f3c7eaf412ad89dded4f6e5c23884a0a1927d5b07ee81c9` | Gate or self-test log |
| `boot-4x4.log` | 11586 | `a0bfafce4667c85480217a151db6b83bc837c174ef5acce4a38ef90a6adf7857` | Gate or self-test log |
| `boot-native-controls-4x4.log` | 1758 | `526018ad8a8209da4d8bce9e7b3791cdc665b31d3c9bed3423713a42c2498905` | Gate or self-test log |
| `census1-969.json` | 16784 | `14cf3160a6de583c9e56d21e6cccff7812abf8828aab72078a6ab55536d79a3e` | Costs by the rule from census 1, #969 disposition applied (owed lines listed) |
| `census1-completed.json.gz` | 12661 | `fe2767596936cfeadf974cda08aa4669d41ce3cf877593ba0d7bc8dab5991fc7` | Census 1: all 159 cases, native status, trace hashes, findings at the 1x1 statements |
| `census1-manifest.json` | 5544 | `841d47d585eebb5f0c6e82df462c87863e2ad25ab89f0dc794e134be526d2e11` | Census 1: groups per variant, native executable hashes |
| `census1-no969.json` | 15295 | `1b177b71d341f14d056b4bf7985afea82f3ca2b0a123a3aacaed77d399bae101` | Costs by the rule, every owed line counted (#1022 control) |
| `census1-runner.log` | 19761 | `088b55c4e7fbe236e432fd613d0c587ff87fb7b08d75a81cf4244f56025eb365` | Census 1 runner log (START/DONE per case) |
| `ctrl-memory.log` | 60556 | `55190cd68b984a0ef1510dae8ca40aea8d24518c841bf4172ccb551deb32437c` | Gate or self-test log |
| `derive1-969.json` | 34243 | `f7ec2f4094ec24b7e250e47706323e07e0da70186dfdc2183d6335269553ed99` | Rule derivation: all 52 candidates, rows, owner findings: NO QUALIFIED MODEL |
| `derive1-no969.json` | 36539 | `cfbb463a5ea783178ffcc3c16d281381f541926177f541d1d0dac1b442672501` | The same without the disposition: NO QUALIFIED MODEL, load 1.03 |
| `egress-replay-all.json.gz` | 4410 | `7aa88c2159587769c2b24a69d3489002cb08e01fe80e1a8328ab52761f5f4d54` | Egress replay at 100 Mb/s over the 159 traces: (a) and (b) per trace |
| `envelope.json` | 2583 | `ff031eceedfb1c27629c90ff4f5c798363dc3501e55ae204e3c16cac236ee355` | The 100 Mb/s envelope by Milan Table 4.4 (tools/envelope.py) |
| `final-4x4-gates.rc` | 56 | `7c723e422aee33e53ed793efc85fa7dd8466261db71c46423f4b4e234468f004` | The three 4x4 gates again at 11f903bd4 |
| `final-boot-4x4.log.gz` | 2597 | `881aea6d36b94f91ff2892790bfc9efa9a78ee8de7ad19e82436f5399f19e7ee` | 4x4 gate log at 11f903bd4 |
| `final-boot-native-controls-4x4.log.gz` | 461 | `c0be65059fa653e6e942fd9639510db31cca0ab1dd9d37017282a6a4fdc9020e` | 4x4 gate log at 11f903bd4 |
| `final-region-4x4.log.gz` | 1787 | `62d106fe427a4afdcfbb24017e65bd68a36608228f301f4e3accb07a0d93437c` | 4x4 gate log at 11f903bd4 |
| `firmware-0.log.gz` | 8954 | `ab0447a864e7c3a9a0ae10b76a2224cd2c37bcb0aeb8227685bce146d2453712` | Firmware shard log |
| `firmware-1.log.gz` | 35653 | `b3e3fda30358adfc6c43b0d93779945cedfecd9ac2e1b8e0f9ca1ce15714e540` | Firmware shard log |
| `firmware-2.log.gz` | 12433 | `0b55e51d8a95afc2fceaae1faec7df0e233c60baf50c329ebe0bd8fdc2663df2` | Firmware shard log |
| `firmware-3.log.gz` | 24414 | `c7d0a21bb97987f6e1e93e509764ca6ae0d92376afd5ba88bfe00712d9a5c20b` | Firmware shard log |
| `floor-search.json` | 22612 | `cab06be17367af34354d35b47ade8f027c42ac8af31071b88b9f54f24e287bbb` | Indicator: the same search at the 1x1 costs with the 4x4 counts (no row) |
| `gates-results.json` | 4109 | `cafdbc150fc8fbf8ec853064a2eb130aaf89e854a65caa869184eeef320100c1` | Firmware shards, boot, controls, region, ctrl-memory, host arms at 1c158ec15 |
| `host-arms.log` | 6496 | `34b9afbb5bcddb18f9e8c1d055a47cc89b154fc6f05bd336fd83e1ff75bc1e7d` | Gate or self-test log |
| `identity-base-digests.json` | 10102 | `170ed8a27a8075d97ae93947cc778aa25e1e24313872218e750dc9af7aef83ee` | Base aa53840d9: builder outputs and product ELFs of existing configs |
| `identity-head-digests.json` | 10102 | `5c774106de0b918edbb5554590aa0997f5f6ed804dc2544600dc485fbddaec8c` | Head: the same; equal but for size.json (archive mtimes, map paths) |
| `product-4x4-census1-size.json` | 1805 | `8db1c6de54f1e30d18471c7de8b8e362ed531c28b185741346d731bd2917f31a` | Census-1 product ELF size and banks |
| `product-4x4-size.json` | 1805 | `50a3f181e49b723e1baf033e4868af74a4788258008d07029e810b5704f96504` | Final product ELF (48 kHz AUDIO_UNIT) size and banks: 49.5 of 56 |
| `region-4x4.log` | 15134 | `48e15cb8d4db32318f1264b1ad86214f412729b775ec122e74313ce2b20af4c1` | Gate or self-test log |
| `route-AltSpreadLogic_high-Fast_0C.rpt.gz` | 63167 | `2a2986c9759f6976adfb4da22ef114f22802093d24abb4fb40a4c1379c5fa09b` | Signoff timing or utilization report |
| `route-AltSpreadLogic_high-Fast_85C.rpt.gz` | 63169 | `d45b40034ce2536c411a757d2338f48134e958685983ba5aa8cd38496685b560` | Signoff timing or utilization report |
| `route-AltSpreadLogic_high-Slow_0C.rpt.gz` | 61765 | `fc0687a1f8eba3b6b9ad9d436d488d05c30464b911d539588e38afb6447d75f3` | Signoff timing or utilization report |
| `route-AltSpreadLogic_high-Slow_85C.rpt.gz` | 61767 | `e67c86ff6293f5b37efa8194f017d65032b503a4fdfa77ef40d1b478f9c718b9` | Signoff timing or utilization report |
| `route-AltSpreadLogic_high-utilization.rpt.gz` | 2477 | `6467f7ba14b7952fe5c148efb2bcdc6e4ad0c2b433d584662fbd78ae14fbc8cf` | Signoff timing or utilization report |
| `route-ExtraPostPlacementOpt-Fast_0C.rpt.gz` | 62516 | `420fd0f5c0c60be212a74140f1fbc0bf4b82ab68339fdb4e921ef244940b6eb0` | Signoff timing or utilization report |
| `route-ExtraPostPlacementOpt-Fast_85C.rpt.gz` | 62519 | `06774e429334f557e389342a56a070ae19f2a273ffbaad07fccf567b4590e3e1` | Signoff timing or utilization report |
| `route-ExtraPostPlacementOpt-Slow_0C.rpt.gz` | 62515 | `8932bfadbd1a4644c192e32ffe13d2fa99065355b10287b972656dd378c11d6d` | Signoff timing or utilization report |
| `route-ExtraPostPlacementOpt-Slow_85C.rpt.gz` | 62517 | `b4ff8b8e2cdd64760f9a644c53ab8e48ba20c46a0195121e61c052428a5d83ee` | Signoff timing or utilization report |
| `route-ExtraPostPlacementOpt-utilization.rpt.gz` | 2488 | `a287b1e2a7b28090cb26944f75a2b6768b237359921c2cd22af971a8438a667d` | Signoff timing or utilization report |
| `route-ExtraTimingOpt-Fast_0C.rpt.gz` | 61772 | `6bd819b932139add6e9282390a2522a831a5897712a4daa9b93871bcd331db07` | Signoff timing or utilization report |
| `route-ExtraTimingOpt-Fast_85C.rpt.gz` | 61774 | `f69caeb36db963a60445b7bd4fcbfc37d6076aac9da04bdbcd6ea18b7a077826` | Signoff timing or utilization report |
| `route-ExtraTimingOpt-Slow_0C.rpt.gz` | 61262 | `365521ddedd46f84d6865eff145e046b664057e6e545fa5f548f57bd65786d1d` | Signoff timing or utilization report |
| `route-ExtraTimingOpt-Slow_85C.rpt.gz` | 61264 | `4259043e72851999b11a5462b9734a71f8e42b17fa3e6077256c65e4153cf97a` | Signoff timing or utilization report |
| `route-ExtraTimingOpt-utilization.rpt.gz` | 2477 | `8f766ee574e90a1353b612f3277b80029b962bdfec7235b17bd73ed26ec98ec1` | Signoff timing or utilization report |
| `route-graded-images.json` | 20591 | `8391f2a8fcb36075212475b8e62e7c36bb596722eac60c385ef80a89be09041d` | Three routed directives graded at all four corners; identity and offline pair checks |
| `route-inputs.json` | 146 | `f388a056221cc5d6f9a60f434e32eeb78446d3a7a896d3f1740aef567772c28a` | Route head and firmware hash |
| `service-selftest-0.log.gz` | 21228 | `24c74c84356bfff3ebf439bd8a77f1f81fd094a88cd85a7187d768ac95db2f3f` | Service self-test partition log |
| `service-selftest-1.log.gz` | 21168 | `e025602c945be6cc6560e1450a9b953a8800c99bdf5d6209414c23286a1e4145` | Service self-test partition log |
| `service-selftest-2.log.gz` | 21481 | `d5ac02b25165915cdc430cc5078a45625edc39a9339a22c1e83c22cf04704a10` | Service self-test partition log |
| `service-selftest-3.log.gz` | 21153 | `3ebfa314db690e3a0b91d0a665d3613466a7907d0f24fc8cf838a3ad96e07667` | Service self-test partition log |
| `service-selftest-4.log.gz` | 21523 | `b462e35794033b1f2fc053a9e212e5668120854296f2fe8ff0a7e7f5a40be5a9` | Service self-test partition log |
| `service-selftest-5.log.gz` | 21272 | `a68f3131189a56eefd4ef92bb4ed5088a71a40b100dba45f22d047c290a749dc` | Service self-test partition log |
| `service-selftest-6.log.gz` | 21125 | `daa3d7712d3c144a427a1268b273c70d3c9d53f8ba14e890444318ac937a9092` | Service self-test partition log |
| `service-selftest-7.log.gz` | 20805 | `9ed4c334544476d2a54a945146ee53e7170ff485c334f3de57e27d477591a6e5` | Service self-test partition log |
| `service-selftest.json` | 331 | `3a7ce61e8963d32a7bdbe4468bcf0ca15a68bbc8e20375887cf33217858faeef` | Service self-test partitions: all rc 0 |
| `standalone-arty_grade.log` | 662 | `16b5cb1e2bf9928d06dafcfd98dbb4f18bc3679310f492f2ffb753ffda3d1dd5` | Gate or self-test log |
| `standalone-egress_ledger.log` | 20602 | `5f1f95f6e9a355544b33c2af6e9592b6351cc89ab0abc99e6ca2a7ca60eb1d81` | Gate or self-test log |
| `standalone-load_grade.log` | 75 | `a8b83c333d3b0e8949ff874640b09b4ab1ee9e1309b50ce857dbbae94de705ba` | Gate or self-test log |
| `standalone-record_classes.log` | 138 | `f493ee9e4703ef5d1d8e5fd86035ca96559174ce38bae1f5d0a52d6aab3c64c4` | Gate or self-test log |
| `standalone-rows_tiers.log` | 50 | `83ca997dc47de52454b3574a6f71c705c8d0906a1cf96432602c9ea6893a9463` | Gate or self-test log |
| `standalone-shape_costs.log` | 55 | `694e4c140b5223abef4e326f0702e6cefa52aef4645b3ab265569157c48f9a3e` | Gate or self-test log |
| `test_builder.log.gz` | 39988 | `ecb85932e38deb0891db0c04fce08cf863fcd813d6d233963ab518ae7617edc2` | Builder suite at 11f903bd4: all gates pass but gate 11 not run |
| `tools/build-variant.py` | 635 | `351b307243af192dbef08b6153837630abb23418155d1c6f1ad65003b693f91f` | Lane tool (copy) |
| `tools/census-run.py` | 6624 | `646a3d355716a0887071af7a582d6e03a61f9062dd01b67357b85585daf3a3d0` | Lane tool (copy) |
| `tools/census4.py` | 6067 | `27722f03a4706e7538da3d74fc5a49fc4ea514117a31dc0b826437d3c6ee3011` | Lane tool (copy) |
| `tools/derive4.py` | 4781 | `249944160565c9f2ee3f1a8dbe3b9f057a6eb49948558c4fe5e8dc16f18b57c8` | Lane tool (copy) |
| `tools/egress_replay.py` | 19627 | `7990d205dddc6058a6785902560a65013d541a10654b482c44c710cbab7c18e2` | Lane tool (copy) |
| `tools/envelope.py` | 1444 | `27cc7a151a4f95ccf557a95831c98e313c8a3145bbc369f7b1514318b058cbb6` | Lane tool (copy) |
| `tools/eventcost.py` | 3474 | `e25a7bfbd68d02f8ca988d789351b39fd7f2b10212def3461eaa20243e0264fc` | Lane tool (copy) |
| `tools/gates.py` | 2992 | `cf2e0ea80e05b7acf89e8877e605f29c654e724c5333ee4b55ed48367e0fa1cc` | Lane tool (copy) |
| `tools/grade-images.py` | 5671 | `a7eec9445ed4e4564e2ebeda423365a67ee41967e1414f4a070633b0223d6122` | Lane tool (copy) |
| `tools/host-tests.py` | 1552 | `a76260ea97ffbebb32ff571c6c6d0222c7ed783a100436c18279203d5aae133e` | Lane tool (copy) |
| `tools/identity.py` | 1940 | `4cf73853c96973b6a5823c767286442c7fa980900223e7b2804fa2f7ad0204f9` | Lane tool (copy) |
| `tools/parts.py` | 8729 | `f25460cb3c1388f22250f36aa6b02d26f893403f2665cdc05f15e023f53b267b` | Lane tool (copy) |
| `tools/product.py` | 1155 | `4a4d934ca0151b0389bc96ece200319ea510517f1ea108db60a875c562fca9a8` | Lane tool (copy) |
| `tools/route.py` | 3469 | `aea2f8f9ad431f86eccb75a19a073b2200c3c4a4b82e18dbece816b8e755ae0c` | Lane tool (copy) |
| `tools/run-env.sh` | 351 | `ec11ed24f3f8a1dd451db2cae6d67497584997a01d413348236ed289452d62e7` | Lane tool (copy) |
| `tools/search-floor.py` | 1869 | `4a529ce648c0ce4a3f6d96282b9bd1ab94f7b80dce630f97ed4e2cfd7b99622f` | Lane tool (copy) |
| `tools/service-selftest.py` | 891 | `acc5e618ef3a0c3fa80ed39f9ac019dc2548d39de7f2382d7fc0c9b6b82c6cf2` | Lane tool (copy) |
