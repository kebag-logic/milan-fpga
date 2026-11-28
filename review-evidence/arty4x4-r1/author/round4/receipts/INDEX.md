# Round 4 receipts

Head `12ab4b189f54439cd126f677b906a19835d7f32a`. Gate logs from `$VALIDATION_STORAGE/arty4x4-a863/gates4`; round 3's receipts (route, censuses, qualification, egress) stand and are not repeated.

- `harness4.rc.txt`, `ledger-*`, `arty-grade-*`, `fw-coverage-*`: the harness gates (`tools/harness4.sh`).
- `service-selftest*`: the service self-test, 8 partitions (`tools/service-selftest4.py`).
- `docs/`: the docs workflow's runner-free checks (`tools/docs-gates4.py`, `tools/docs-cmds.txt`), and their re-runs in the LiteX and Markdown venvs (`venv-docs.rc.txt`, `venv2-docs.rc.txt`, `em-dash.log`).
- `identity-*-digests.json`, `product-4x4*`: byte identity at head against the base `aa53840d9`.
- `test_builder.*`: the builder suite.
- `gates-results.json`, `gates.log`, `gate-*`: firmware, boot, region, memory and host gates (`tools/gates4.py`).

| File | Bytes | sha256 |
|---|---:|---|
| `arty-grade-1x1.log.gz` | 487 | `1e47c44bb6a8b52bb20e05e50ef55da3a2a37e2509b7e9ebc40e63fc2a7fe74f` |
| `arty-grade-4x4.log.gz` | 486 | `e0d1d4678e79fdd0dbdb3924d66f10f16def27ed6a0d4e549245c6a2eec7495c` |
| `arty-grade-selftest.log.gz` | 293 | `a22e91de7b14a8b38bdce137f384b3ada012ad23fe5555861f0cf80df4f9f7fb` |
| `docs/docs-logs.tar.gz` | 109752 | `b93100a99514f8b62d8b5f2fb50ff72e4b4877f926b3206e5ddb8505d24982fe` |
| `docs/docs-results.json` | 11229 | `a037c859d376c40faaf4f0b234bece0dcd3038792bb41a90bdbecde1ba69e057` |
| `docs/em-dash.log` | 142 | `8cd95322f212df57440a4fca4796114825342b9bb44043c236d2e1357b4596b3` |
| `docs/venv-docs-0.log.gz` | 110 | `267bcf6873299ef4ebac599bb302e951ddb3448bde69d4cbc705ee3ffffaf3b3` |
| `docs/venv-docs-1.log.gz` | 94 | `ed3bc4ce842aa81aa9848348b33008364323c1bb46bc09b50e90df8952066690` |
| `docs/venv-docs-2.log.gz` | 90 | `ee1c8f70e3d0f88199c0a39f206d21fa3a4b36818e3827963a3de134e3b40aed` |
| `docs/venv-docs-3.log.gz` | 88 | `53f7232a7430883d83e3527049d317ecd7bef70118d43ce68ce7b7e78c77fd3b` |
| `docs/venv-docs-4.log.gz` | 273 | `07540b0bce28a2931aa76dab9d20cf94efe86c6a621e72c220f749edc74eb143` |
| `docs/venv-docs-5.log.gz` | 313 | `2ec3650069a011793479618e1feb90fd933e6e7c87e317670cb488880c906356` |
| `docs/venv-docs.rc.txt` | 486 | `5fc4b1804d3a252e1b10668b8780dc8c5f3ccefa43bd44eb9a63c02b8ce9b34a` |
| `docs/venv2-0-md.log.gz` | 70 | `c2f42993191921543fd8932078d5439039345670b6ac9ff46aa72b204d131f61` |
| `docs/venv2-1-md.log.gz` | 97 | `263533e01a61bdffe416075b5cbff0ab30e3530ce99cf974907bef01d7e7d768` |
| `docs/venv2-2-md.log.gz` | 124 | `0840fe212a905ce391938c25bab7a5a602563095a00c54579120a22faed68bf0` |
| `docs/venv2-3-litex.log.gz` | 95 | `026ea568617bf595a38f89631ac04be5962f2927c8f482f4fcf46e54759277b3` |
| `docs/venv2-3-md.log.gz` | 134 | `4eaf4fa12548b8082a94a5a5fae5f9ed47e9cbfac6f5a588e1f766db4f4c6e12` |
| `docs/venv2-4-litex.log.gz` | 1115 | `435b1f75fb4d3edd75beb94df6836226f0fd3a96de4c4b92205c5b0cafac417c` |
| `docs/venv2-4-md.log.gz` | 1243 | `a9e023a8ddacc30670603245b6cb440ef917f8655a9772026bb277dab86bfbde` |
| `docs/venv2-docs.rc.txt` | 308 | `d617b634f93a873f5394c55d718a2aae476b3ac36650addb918902f11277ec2d` |
| `fw-coverage-check.log.gz` | 1287 | `2f247eae4149bddce53158d54ffbdd4094cb74c3ffbcdbb453980c073b746cc8` |
| `fw-coverage-selftest.log.gz` | 1082 | `d653ae840ed6c45193098713638b5741a3daaea87dfb61103c87721759965c18` |
| `gate-boot-1x1.log.gz` | 2593 | `2fd77605232e03c633a879f069efe4cb624837a6599c95053779ddee816632bf` |
| `gate-boot-4x4.log.gz` | 2586 | `401e2a75294d0495b6a695cd228892b043344647f56d5c0328b67437aa127218` |
| `gate-boot-native-controls-4x4.log.gz` | 461 | `df42a7a2f99350953500719b00466b588ff599820af0d5ba73d5ecb30fbf19f3` |
| `gate-ctrl-memory.log.gz` | 8354 | `5bb87d8091eb480c5e0e8d86f1c3a91e3b48a37667f492b580361579376cdc19` |
| `gate-firmware-0.log.gz` | 8954 | `3979b9a58b55dc119bd7a6c838cda86c3ef83514b2dee820a6fe0d31914a5e26` |
| `gate-firmware-1.log.gz` | 35656 | `d048c729b66ea1a960336e1eaf03d879a30320ccc23103e05f67839bce1041b8` |
| `gate-firmware-2.log.gz` | 12483 | `602acfc40992bca6fecadce41285ecda4c945837ed28dd77faaca1fce8dcaad4` |
| `gate-firmware-3.log.gz` | 24435 | `06db47ced1c58743844b953441520ac958b9872281c47122b2370926c64dc189` |
| `gate-host-arms.log.gz` | 1111 | `6631fea3ac13061c10bc545b9ea8d7e6a83e24d36fb707e9016608182c789318` |
| `gate-region-4x4.log.gz` | 1783 | `240b1678bd3084b21e9d550ecdac5de51f91fe03dd43294c46586b8e8aafff3e` |
| `gates-results.json` | 4117 | `972481cb2d205e3c4a625cc923f5dd6409a06afbc84f9f66689be5009ac04d71` |
| `gates.log` | 603 | `9880bdc0ed5453b8843d026080b36c0da31e21b55a99879174837dd0d879c822` |
| `harness4.rc.txt` | 218 | `6815d42b0dd7facc6a3119e93a5ac598187210dff7af487449eefaa7846a86e3` |
| `identity-base-digests.json` | 10102 | `170ed8a27a8075d97ae93947cc778aa25e1e24313872218e750dc9af7aef83ee` |
| `identity-head-digests.json` | 10102 | `722fd287de9c4883e3cf03992eed0c3515cbddadaac7f7d43c13ed76ca32cd42` |
| `ledger-census4.log.gz` | 404 | `7becf55b0fbe2f49cf2d5bd97f545fdaed5d7b5376edc470883fabd7ebcdfe6f` |
| `ledger-selftest.log.gz` | 2544 | `4cabb19b2a6f14badf12b995439e716d1323fa1fd19a49926e8d41ef53a01589` |
| `product-4x4-size.json` | 1805 | `e56e0d35b72c87cac71019d200f264657a038ca8a4a53ec2c7c8fc3035fc64de` |
| `product-4x4.log` | 4956 | `998289160457a31fbdbc9fb4ec8527b510acfa41e01c7b30a2a21d1cc367a9c4` |
| `service-selftest-0.log.gz` | 21252 | `743f25be358444c32755b5cd29f07117cd02e9670717a412fd8ef502c7f5d89e` |
| `service-selftest-1.log.gz` | 21193 | `c3498552f2d8a803068bacf05fdcefb15b8830a7c4079fb469918104b65c9dd7` |
| `service-selftest-2.log.gz` | 21495 | `81ac21348d2f00d33d488e562601d72cb56cd2aece33b8292ea2c7b1030348c0` |
| `service-selftest-3.log.gz` | 21168 | `ae553db8624163021f670fd91e50ffdec620f626cf33bf35b0b837fa1c080722` |
| `service-selftest-4.log.gz` | 21539 | `b50cebfa11a1ba4f73596e94f9a73cb9430a616bee785cf230a45c8512882fd6` |
| `service-selftest-5.log.gz` | 21287 | `75f6fb70df2f8f6f325515008e83168bca9572c55934b351d2ff0b14745854bc` |
| `service-selftest-6.log.gz` | 21140 | `8d3532ad4d122ebc0384390ac4f1fcfd60b4a4247460c31bde2a4b4aab109fe0` |
| `service-selftest-7.log.gz` | 20821 | `8f3de5663dc37c2e9cb75652aa7ba4bd217b49f0c6e48984bf134cf8c4dcc716` |
| `service-selftest.json` | 331 | `3a7ce61e8963d32a7bdbe4468bcf0ca15a68bbc8e20375887cf33217858faeef` |
| `test_builder.head.txt` | 41 | `595008182b5bd04ba22fd5bb401883962de105f98f3fb075cc9a2ce30fb06782` |
| `test_builder.log.gz` | 39982 | `f8cdb44bdafb9ee0ef0c71e623c1604d5fac89487d751acd7a1fe8d7cefe47b2` |
| `test_builder.rc.txt` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `tools/builder-suite4.sh` | 255 | `e9aec7b95e27c98112e09dc220ea1c62fc69b76f952b61e78bbd8e3013dcde75` |
| `tools/docs-cmds.txt` | 5860 | `e713e679d00f6dcc39ed72f5761fa720162208070a41e1f272c620eefc9acf6e` |
| `tools/docs-gates4.py` | 1349 | `519e25868b718ef48e73802f12206ac21ed8694a280c16c8fa6fc63025afb568` |
| `tools/gates4.py` | 2993 | `7f3dc6f8fef51a62b08ff12bc685a55b2dec04b14b25561ec97f83a6acb30108` |
| `tools/harness4.sh` | 1181 | `2d14f69383be746b5e8ba4ef7d26feccc14b5d0a5900c04a09b57d0e90ca9887` |
| `tools/identity.py` | 1940 | `4cf73853c96973b6a5823c767286442c7fa980900223e7b2804fa2f7ad0204f9` |
| `tools/product.py` | 1155 | `4a4d934ca0151b0389bc96ece200319ea510517f1ea108db60a875c562fca9a8` |
| `tools/receipts4.sh` | 3189 | `2d4e8c25c39efb4d464c4156ee357f8096bbab781046b3655cb8fd3ef192628b` |
| `tools/run-env.sh` | 351 | `ec11ed24f3f8a1dd451db2cae6d67497584997a01d413348236ed289452d62e7` |
| `tools/service-selftest4.py` | 892 | `719836b48f9f1de0ccce63902733feed603b621a31a53c5396cc05413e8cbf74` |
