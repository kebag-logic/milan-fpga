# Receipts, Arty 4x4/1if round 3 (100 MHz)

Local only. Census trace archives stay in `$VALIDATION_STORAGE/arty4x4-a863` (`c1`-`c4-*.tar.zst`).

| File | Bytes | SHA256 | What |
|---|---:|---|---|
| `basis-model.json` | 28478 | `02c1c1ae134167671faeef562f45d28c0fdd74566b1a4ad27607a6ec46d05cc3` | Census-2 basis: round 1's cycles restated at 100 MHz, derived |
| `census1-at100.json` | 15124 | `3f40ef428222fd12256790a2a0e195bd68052a86d1ad1d2f284f40da4d7f5a93` | Round 1's 80 MHz census cycles restated at 100 MHz (basis input) |
| `census2-969.json` | 16734 | `15ffa6d7f145d9d3fabbde98c5a209f822f07e73786f1999eb042da26073aa15` | Costs by the rule, census 2 (instant egress), #969 disposition |
| `census2-no969.json` | 15381 | `f46c11b26b67023eabf32ab785525f3f1237f8c0949cec2188e3053a2e885064` | The same without the disposition |
| `census3-969.json` | 16734 | `b622b7c268c8743bb3f48192a9800fc0fd6194a6b720702b876ca8ea91428be9` | Costs by the rule, census 3 (instant egress) |
| `census4-969.json` | 16735 | `7b3eacb55490c1f4899728cdeae207ab5cb323fb5de4e3fe1f73031c49e563dc` | Costs by the rule, census 4 (link rate) |
| `census4-completed.json` | 68604 | `b1115cea314c65fbbe15528f6ab39a6af13e840b94062051c796e75c1f08602f` | Census 4 (100 MHz, link-rate egress): every case, trace hash and finding |
| `census4-manifest.json` | 5544 | `b2d7dba6ab3c6c2728ec1ad41f961ee8de159f6cc92d402815e3f1c884a55df6` | Census 4: groups per variant, native executable hashes |
| `census4-no969.json` | 15382 | `d9ef7e10f3d7a60b9e435b053cbb54074de121bd698b81a1c6a385cb723a8a61` | Census 4 without the disposition (#1022 control) |
| `census4-rebuild-identity.txt` | 484 | `0937cea94ce764576636759d594f1691caad094aec29e2db4e797792f4143adc` | The eight census images rebuilt at 00f1fcd9d: native executables byte-identical to census 4's |
| `census4-traces-archive.sha256` | 130 | `1a25510fe09509ddbe0636a9a350a932a5318d361e7e8e5b6cadfecbe45907ca` | sha256 of the census-4 trace archive kept in scratch (c4-census4-linkrate-traces.tar.zst) |
| `derive-census4-969.json` | 29140 | `c2a6913ba9ffde419bf4b84b37ef44a7a9057f8f7719224a04215abd013e3b18` | The derivation from census 4 alone: same choice |
| `derive-merged234-969.json` | 29288 | `4e6ac71464e94efda5d4bae4762f491a016cf44f4b03be60cb23bc5459923f66` | The rule's derivation from the merge: CANDIDATE MODEL 125/5/1250 (installed) |
| `derive2-969.json` | 28479 | `4f1576bae0cf628b9281570646989f0fd8db0b6da3092f5be343a9bc71aec5c0` | Derivation from census 2 |
| `derive23-969.json` | 28479 | `4f1576bae0cf628b9281570646989f0fd8db0b6da3092f5be343a9bc71aec5c0` | Derivation from censuses 2+3 (instant) |
| `egress-fixed-80-100.txt` | 1000 | `17009a3ebf83524cfa15d56993661d73a2c8bf621670e2d7bee2cc3235a71b37` | egress_fixed.py: fixed path 312.5 ns at 80 MHz (gate PASS), 300.0 ns at 100 MHz |
| `egress_mii-census4.log.gz` | 2831 | `742d11ff889319ed60a2a1d263e5c7274aa7181db16b35bbacd5369c4920e2ac` | egress_mii.py over census 4: (a) by construction, (b) 527.04 us of 1000 us, RESULT PASS |
| `gate-boot-1x1.log.gz` | 2593 | `15a6852df83c67144cc3277dff2cf638bba9c2540d35c92ae9ce3a8e655a08fe` | Gate log |
| `gate-boot-4x4.log.gz` | 2587 | `1ed045e7b3c5e8f0b9946720315f20ca17ef9766130132b898cd3caf195a4bbd` | Gate log |
| `gate-boot-native-controls-4x4.log.gz` | 461 | `99cd06f755f86fbe071951a0666f364a9a7fe1a85c638a3c574916fd67832319` | Gate log |
| `gate-ctrl-memory.log.gz` | 8353 | `011a27bb65ad0bcf3b9f940b2d7cb322d5f11a04c81a6353fcfaed92764c11e5` | Gate log |
| `gate-firmware-0.log.gz` | 8954 | `dcf844a75733d94c7e6d8fc322408a8b7df1c378b32587a7a4bcb61380f07bf5` | Gate log |
| `gate-firmware-1.log.gz` | 35656 | `99f6008e3c4e0adcaf16a063b2acd7366efbdd0d4d76760db128c49368f866dc` | Gate log |
| `gate-firmware-2.log.gz` | 12483 | `b2a3f7f761f81ce191c64749a88d91360cf072e1485d085e314955f277ad4916` | Gate log |
| `gate-firmware-3.log.gz` | 24435 | `65fb22403b2772001abcb399ebc4922030a09102bb2af35a257146163757b3fa` | Gate log |
| `gate-host-arms.log.gz` | 1111 | `b01531e9bffe7ea5ab533e1dce308754bc53af8782ba5035211ba06e386066b2` | Gate log |
| `gate-region-4x4.log.gz` | 1782 | `ac4c7d554439ed3fb11a21b7ddcf0990a2944b4447b0f393a6bf2dfb69077e0c` | Gate log |
| `gates-results.json` | 4117 | `40ec0cbc09f24e36830b3de8ce5a0d37c3500d55c65a977df6797cd8b82ab7c9` | Firmware shards, 4x4 boot/controls/region, 1x1 boot, ctrl-memory, host arms at 00f1fcd9d: all PASS |
| `identity-base-digests.json` | 10102 | `170ed8a27a8075d97ae93947cc778aa25e1e24313872218e750dc9af7aef83ee` | Base aa53840d9: builder outputs and product ELFs of the existing configs |
| `identity-head-digests.json` | 10102 | `f58dc618d13e6e40d3f22e09b25acc9ce4e73ad8115797fc29a6e294e4bd6f5a` | Head e7bc55f8a: the same, byte-identical but size.json |
| `merged23-969.json` | 18606 | `53fdef2e3692dcc060d2422988afd383102fc6218fcf9cd8561d2b4a26a2fa73` | Largest of censuses 2 and 3 |
| `merged234-969.json` | 19731 | `6ca2c87b4e845629ef979e65ba453954f8c2be07921d70d0db2208aa4b7fc164` | Largest of censuses 2, 3 and 4: the installed row's costs |
| `product-4x4-100MHz-size.json` | 1805 | `f4fcbe0a0583c652dee4bc1c44ea292a244ff87e8306cebe8fcf6cfa10110a86` | Final product ELF sections and banks: 49.5 of 56 RAMB36 |
| `qualification-commands.json` | 5507 | `5a5fbc70501a713f8a7d2f4f96931b6fbbda50326b05bf5bdec0a17df1517928` | The qualification's commands and their log hashes |
| `qualification.json` | 11205 | `1dd94eb1e3c0c5727d5add0f5b68ee2bfdcadc03fe78e42c904bb0885015cde9` | Qualification of the link-rate census at the installed row: PASS (159 cases, 8 regrades, record classes, statements = measured rule) |
| `route100-first-AltSpreadLogic_high-Fast_0C.rpt.gz` | 61305 | `628e22628d87f039d81bb65efcf38a495041636d74193274c2c6d6b38c99b1f2` | Signoff timing or utilization report |
| `route100-first-AltSpreadLogic_high-Fast_85C.rpt.gz` | 61306 | `f3fa2513fa612d54df0b5dda10d2fdce323ccacd11e2f02a33d0733ddfa32d0d` | Signoff timing or utilization report |
| `route100-first-AltSpreadLogic_high-Slow_0C.rpt.gz` | 64048 | `be7cbd1591c50d54612ead1c11e451fa1f898762e74450255feb619c45050597` | Signoff timing or utilization report |
| `route100-first-AltSpreadLogic_high-Slow_85C.rpt.gz` | 64049 | `29c663cac3d63e385dfb826340aff706805064f923c76a432d3075917bed02f3` | Signoff timing or utilization report |
| `route100-first-AltSpreadLogic_high-utilization.rpt.gz` | 2481 | `f03cc71edfe7d456213255ba17dbf26ac596bdd86d8df45ab1f811b0b31922a6` | Signoff timing or utilization report |
| `route100-first-ExtraPostPlacementOpt-Fast_0C.rpt.gz` | 60560 | `36871cdf82f00041f7f2f8e8378d1f18607f057054d277923edd08494b5ad8ce` | Signoff timing or utilization report |
| `route100-first-ExtraPostPlacementOpt-Fast_85C.rpt.gz` | 60561 | `dbf7130d9bfeb294691a28a890d3724d360bad0ea48ccf5744abf001d3f72254` | Signoff timing or utilization report |
| `route100-first-ExtraPostPlacementOpt-Slow_0C.rpt.gz` | 61480 | `f65fef4f21196378678d5754863cde05a55082e9a0b439a9019a847225707b36` | Signoff timing or utilization report |
| `route100-first-ExtraPostPlacementOpt-Slow_85C.rpt.gz` | 61482 | `5de40554a2a7d601cf8329382b4712504ba21699c936a83175ce6eaef173cf31` | Signoff timing or utilization report |
| `route100-first-ExtraPostPlacementOpt-utilization.rpt.gz` | 2486 | `bf7544edcf1e16f66819141e47169eb12b239462007ed923e479d7ee32c3e873` | Signoff timing or utilization report |
| `route100-first-ExtraTimingOpt-Fast_0C.rpt.gz` | 62577 | `8a23bd192bee2876908c5c4cefaa7a7d4bb6b8ab34ed40050854a74dfe090e5f` | Signoff timing or utilization report |
| `route100-first-ExtraTimingOpt-Fast_85C.rpt.gz` | 62578 | `f7b9572e84a7d038d45805418b514f1e74b275fc290b0158fb795d4d6664f724` | Signoff timing or utilization report |
| `route100-first-ExtraTimingOpt-Slow_0C.rpt.gz` | 63200 | `0dfe175f7ddfb4bca2851e828638ac5e4d19219d7758b418a03539dc98136fec` | Signoff timing or utilization report |
| `route100-first-ExtraTimingOpt-Slow_85C.rpt.gz` | 63203 | `1c72f6fa1d924e74eadd14b0c67829c2977956d59220a10b3c07438c98a6078c` | Signoff timing or utilization report |
| `route100-first-ExtraTimingOpt-utilization.rpt.gz` | 2484 | `c334cf77efd6b299c785c07ed88f8043d714c24b3d872b8b2c75328eda95c042` | Signoff timing or utilization report |
| `route100-first-graded-images.json` | 21381 | `07e44ffe8de86417e4cc9701ea39a0ce20f1b100be39fc827ad24064e9da0ece` | First 100 MHz route (ELF 51334a4b, pre-row) |
| `route100-first-inputs.json` | 1396 | `ef8935443315a563a0e1035a29606649999ddebadbc6e160a0d1386c251f82be` | First route inputs |
| `routefinal-AltSpreadLogic_high-Fast_0C.rpt.gz` | 61304 | `b8e9565aa36e90e72bb7b8645b88b67f53b27d688058cf19b8370fb268142b37` | Signoff timing or utilization report |
| `routefinal-AltSpreadLogic_high-Fast_85C.rpt.gz` | 61306 | `35f99fc869c061d4c5e1a95e1b5612feb39253f39dd98ed2f9f2ddc558b58daa` | Signoff timing or utilization report |
| `routefinal-AltSpreadLogic_high-Slow_0C.rpt.gz` | 64046 | `d4fbd1d5633ada6c89e10af6c50f760c04feee8d3fa093fdc848a5411838f1ea` | Signoff timing or utilization report |
| `routefinal-AltSpreadLogic_high-Slow_85C.rpt.gz` | 64049 | `09db8ed0502013fe8556a6d74e5f3591ac835c9ea82882ccb73c9654dcc4181e` | Signoff timing or utilization report |
| `routefinal-AltSpreadLogic_high-utilization.rpt.gz` | 2481 | `5f053ffa1b960dbeae52364437c9c2d72d1f27768202e628482f978f6d6d91d9` | Signoff timing or utilization report |
| `routefinal-ExtraPostPlacementOpt-Fast_0C.rpt.gz` | 60559 | `370785f54876926de67501e4b89a2f457cbbec056063313f0efbf61e18dbc927` | Signoff timing or utilization report |
| `routefinal-ExtraPostPlacementOpt-Fast_85C.rpt.gz` | 60561 | `e94b1293e187cc837549b36e2cbabcb8dea93f68b38ba64a1b3a1d67e60f13d2` | Signoff timing or utilization report |
| `routefinal-ExtraPostPlacementOpt-Slow_0C.rpt.gz` | 61480 | `ca7b11d17d5afbb76ebe56118334005dd104941330fb7e50a70db78f51c3cfe9` | Signoff timing or utilization report |
| `routefinal-ExtraPostPlacementOpt-Slow_85C.rpt.gz` | 61481 | `48209094abfc09cbb464d29b0f8f4883fbd18264d8e441a7b635f9bb3947f70e` | Signoff timing or utilization report |
| `routefinal-ExtraPostPlacementOpt-utilization.rpt.gz` | 2487 | `43a9238170f66714eb877ddfb692c4045fed261c4dc2fa9509d2e4eb6b0cb53f` | Signoff timing or utilization report |
| `routefinal-ExtraTimingOpt-Fast_0C.rpt.gz` | 62577 | `3442ab4846c21d96bd8fddc0bb2c7eba874d948801b355245dac2400b28d47da` | Signoff timing or utilization report |
| `routefinal-ExtraTimingOpt-Fast_85C.rpt.gz` | 62579 | `296b82805ec2622c6ed36b02d017ffbe06c89b3fab9be013889f431f8dbeb1a3` | Signoff timing or utilization report |
| `routefinal-ExtraTimingOpt-Slow_0C.rpt.gz` | 63200 | `a3f8bab75561a2cc0e707d6721d45a39e4d729f2493efb6a350ac59bf7a37cbb` | Signoff timing or utilization report |
| `routefinal-ExtraTimingOpt-Slow_85C.rpt.gz` | 63203 | `418478cb943fc87417485364627f23d3c56ba96c3620caba7cac7fb75f215f0a` | Signoff timing or utilization report |
| `routefinal-ExtraTimingOpt-utilization.rpt.gz` | 2485 | `84d662cb5d916b9682539215fcf59234e7ef0dc8c63c446ff1fcb1b9be551813` | Signoff timing or utilization report |
| `routefinal-graded-images.json` | 21481 | `22ec83d77158ed9a6ea7b486d00865e9a16d4b78b3fa622d7201a6d3d8a0d8be` | Final 100 MHz route of ELF 1b8066e4: three directives, four corners, identity and offline pair |
| `routefinal-inputs.json` | 167 | `9bc83e81c3c57a1a04bac948d7ea86f8f39b636b9e7266b9ac431ea1c044cecf` | Final route head, config diff and firmware hash |
| `service-selftest-0.log.gz` | 21252 | `e640b7c2b7e431142b0f63a79ee681c1d8cdff61788e3618357f74cf567f70c7` | Service self-test partition log |
| `service-selftest-1.log.gz` | 21193 | `fba09295b84af166420179bab9e192e4b108badcfdd4f2de3e798194395648db` | Service self-test partition log |
| `service-selftest-2.log.gz` | 21496 | `6fec9e0585a527a9fefbe12de1037f2bc47d7b9b7700fd29e4f317c2673db0b3` | Service self-test partition log |
| `service-selftest-3.log.gz` | 21168 | `2187304d15289b825063ae0f82fb9849bb68f7f233473726fea49af7d9f2ab53` | Service self-test partition log |
| `service-selftest-4.log.gz` | 21539 | `d98c634d0fdbfef349d0b8f6b954b37c84bd46542800d3d8e21aa4f56fe0b71d` | Service self-test partition log |
| `service-selftest-5.log.gz` | 21287 | `4210d6be7ccc2a9e61fc69d58447f0ed2a05a4e2480813616be62f768e883443` | Service self-test partition log |
| `service-selftest-6.log.gz` | 21140 | `7a6d31abc119b94923c6ae757882d409e9eb25a8b9cb317a4e6e7ae9b92b548a` | Service self-test partition log |
| `service-selftest-7.log.gz` | 20821 | `fd004644d9ff6b6edcba945793b031025a0fe9227d3cc6afc684db362fc63a98` | Service self-test partition log |
| `service-selftest.json` | 331 | `3a7ce61e8963d32a7bdbe4468bcf0ca15a68bbc8e20375887cf33217858faeef` | Service self-test partitions at d0f402ee5: all rc 0 (323 mutants) |
| `standalone-arty_grade.log` | 662 | `16b5cb1e2bf9928d06dafcfd98dbb4f18bc3679310f492f2ffb753ffda3d1dd5` | Standalone self-test log |
| `standalone-egress_ledger.log` | 20602 | `5f1f95f6e9a355544b33c2af6e9592b6351cc89ab0abc99e6ca2a7ca60eb1d81` | Standalone self-test log |
| `standalone-egress_mii.log` | 1177 | `2741822d9e8671991dca97d02feaa21e0defd8adff96f7da1642ad9139e09dc8` | Standalone self-test log |
| `standalone-kept_grade.log` | 3393 | `564a045967cf769939089bdec6db087ea170b38289e565dd2d1c163f614195f4` | Standalone self-test log |
| `standalone-load_grade.log` | 45 | `43d9de9746dd458086aeaa66b99633bf052569ae5356268600f4950e60519d71` | Standalone self-test log |
| `standalone-record_classes.log` | 138 | `f493ee9e4703ef5d1d8e5fd86035ca96559174ce38bae1f5d0a52d6aab3c64c4` | Standalone self-test log |
| `standalone-rows_tiers.log` | 50 | `83ca997dc47de52454b3574a6f71c705c8d0906a1cf96432602c9ea6893a9463` | Standalone self-test log |
| `standalone-shape_costs.log` | 55 | `694e4c140b5223abef4e326f0702e6cefa52aef4645b3ab265569157c48f9a3e` | Standalone self-test log |
| `test_builder.log.gz` | 39988 | `34a69a658423e209c1aa4a7b3fd7874f9ab4c0bdcc2320ef621113c9bc95fbd2` | Builder suite at d0f402ee5: all gates pass but gate 11 (not run) |
| `tools/build-variant.py` | 635 | `351b307243af192dbef08b6153837630abb23418155d1c6f1ad65003b693f91f` | Lane tool (copy) |
| `tools/builder-suite3.sh` | 255 | `2fd2c49c0cdcaae6bd4486186a87f4fe179879ec0a844cef3139ff6b6dc65e65` | Lane tool (copy) |
| `tools/census-run.py` | 6657 | `24252ed52cd6198c39a72f1507024a01e362a7e5c673bd5c259baea77d5723af` | Lane tool (copy) |
| `tools/census4.py` | 6194 | `31b1dd2860b50a5e032e4faedf0e47cf7a7d95d87a18b8c3a6114c024a5b4f53` | Lane tool (copy) |
| `tools/derive4.py` | 4785 | `6a5c11dff5eb368687ed92f192be2efbdfc146f4d73f918d0abf9b5baae8f749` | Lane tool (copy) |
| `tools/egress_replay.py` | 19906 | `f03d2c1701458cd713718fb609ddee61c53990f97e633ece3d0c08a06759ed75` | Lane tool (copy) |
| `tools/gates3.py` | 2993 | `59e693cf8039410c7a1e175371499dff67f5b8c86f0dcd2c041795c7a0333eb5` | Lane tool (copy) |
| `tools/grade-images.py` | 5671 | `a7eec9445ed4e4564e2ebeda423365a67ee41967e1414f4a070633b0223d6122` | Lane tool (copy) |
| `tools/host-tests.py` | 1553 | `99844057d6a8ebefede86368140c6c424e83b592ad3033f963cbc4cf9a9725a6` | Lane tool (copy) |
| `tools/identity.py` | 1940 | `4cf73853c96973b6a5823c767286442c7fa980900223e7b2804fa2f7ad0204f9` | Lane tool (copy) |
| `tools/install4.py` | 4363 | `b387adfba8a5bcc3c1dc257f06733bb622ac6e2f0c10263257a44a7752ed981c` | Lane tool (copy) |
| `tools/merge4.py` | 1452 | `5523fc1a671d8f6238e8db78adb8bcb63b49058a7f4c34ef67c78fc36904135f` | Lane tool (copy) |
| `tools/product.py` | 1155 | `4a4d934ca0151b0389bc96ece200319ea510517f1ea108db60a875c562fca9a8` | Lane tool (copy) |
| `tools/qualify4.py` | 6497 | `7831aa83dcc5b3607f198103b1609778e32fa815dcf731682b7a196986a0030b` | Lane tool (copy) |
| `tools/rebuild4.sh` | 947 | `d7ada0cc23612197f9a700145e8ba7003a919277cac75bbd09994cb802c06ec0` | Lane tool (copy) |
| `tools/route100.py` | 3810 | `91f3178d943cf34821969fb2ab3d8ad43dc7afeae9d45afde1e9f309604d536b` | Lane tool (copy) |
| `tools/run-env.sh` | 351 | `ec11ed24f3f8a1dd451db2cae6d67497584997a01d413348236ed289452d62e7` | Lane tool (copy) |
| `tools/service-selftest3.py` | 892 | `1bda1ab479bee270a730443635a5da2439e6fac6e743f98b1ba33264ab6d9dbd` | Lane tool (copy) |
| `tools/whatif.py` | 9649 | `dded91170c983d703b0d166f16ecbb670b5c76f2b52b9f2131ef030424aa2bad` | Lane tool (copy) |
