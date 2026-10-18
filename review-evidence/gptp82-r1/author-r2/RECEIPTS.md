# Round 2 receipts index

Published copy: the manager redacted host paths (<home>, <data>, <slots>, <host>) and recomputed bytes and sha256 for the files in this directory. Rows outside it (scratch files) keep the author's values.


Every file under this directory except this index, with its size in bytes and sha256.
`receipts/scripts/verify_receipts.py <this directory>` checks that the table and the
directory match exactly.

| file | bytes | sha256 | what it is |
|---|---:|---|---|
| `HANDOFF.md` | 34480 | `d23aedf75d16adb3d1336a3a485fc9be2b41403db90dc037d1a70f01460d996e` | the handoff, rounds 1 and 2 |
| `PR-BODY.md` | 6785 | `5c6b86d86ca917495ee8cabc3d3bad487079f41ae3da3ae7f22680bc674af6ee` | the PR body draft |
| `receipts/controls/control-base-rtl.log` | 2130 | `c544cc1a5e3cd899b3eb852050aaa6f9004ced719786e2c1cb95ebcbf8c0bac1` | head harness against the base and round-1 RTL and ROM |
| `receipts/controls/control-round1-rtl.log` | 1514 | `4e8d2b93d7dabffffadf16c373e287e315d8eb999a3025c8b048ecf4e5d3527d` | head harness against the base and round-1 RTL and ROM |
| `receipts/gates/base/HEAD` | 41 | `c6da7177804de676b3922dc049aaede6c4e2521e4eb375138c89114a43fefb78` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/bench.log` | 4904 | `2f8308a15ebbe22494aafae6ebc82b15496a7bc5fdb544c5ca89bfe75ce2b169` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/clean.log` | 909 | `a5ac355fb574faca6311e099328046648d224f6df64617a0b9f23f408a051db3` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/contract.log` | 62 | `cdc70d96a542ea1a2ebbc4cae75d9ed837c6d247ce06fcf7a4fb5bb4ae03e07e` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/docs.log` | 2527 | `1f0946171cc082ba2ffdfbf0573f487235fb1b1a4f032b77616bfcb389ce5190` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/engine-mutants-s0.log` | 1119 | `72eb5de2da8431dfb46b219c5802e675e0f07c846fcbed6058c3a199a7d374d8` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/engine-mutants-s1.log` | 1263 | `7e7844d7b08af4aa185d19d22d4f105068cc47f3472ef5ecc9a55942aadbfdc7` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/engine-mutants-s2.log` | 1164 | `c59a36dea10e877b0b2127621a8d2ef8a3c51d15a2b27488a3bcd0c6017ee3c8` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/engine-mutants-s3.log` | 984 | `119f5f8b81c56be2b00b42d6d95c77a18ae623600c4d9b6c93deb94754b0dbcd` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/engine-mutants-s4.log` | 1051 | `d9bc47aaffa0bbe8166e012e3209ec485811bbc9e912e9224a88f44b7fdb8727` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/engine-mutants-s5.log` | 988 | `db41b0bb2d6a32dbadb0b7a6d08c5197b53150789940429fbbe30e0584d29b60` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/engine-run.log` | 6743 | `0ad3bc18639f1afbb832377d1063e53f0f5544b9ff8f43b85f7e71218748af99` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/gaskets.log` | 6418 | `82ddb0b6d5196d2c9e4c97550a34d9efdb9c953b229d14cddd3fda157d28d53e` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/lint.log` | 1538 | `6ebb965bba751f6d08dad2479ccf942648096149f9fe6d77889cad470d81f96d` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/parser.log` | 8639 | `45ed4b6c179f513fe67bf018161ba156965f0b1baed236b642a0d82e5484422e` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/tsngen.log` | 1779 | `71bbdb1e504e92f33cb9734107b45b057867ecef504172469410a8fa663e5d84` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/base/ucpu.log` | 5688 | `5c76283a973e1edd880f4f0398db49237d58eef427235d2ac44f3de533b681b9` | repository gates at base b9ade3a6 (HEAD names the commit) |
| `receipts/gates/head/HEAD` | 41 | `5167b833c69607c5314f6a6d04a49f9de2324d27b8f23c7f936d7fc268727fb0` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/bench.log` | 4864 | `3096a5c29a00fa153e64d738e7184dbcd8cf96a726c3b92783e207d559ad2d7d` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/clean.log` | 829 | `6d2cfa71af79666f48cfabb96233b1b508d35dff8768d6ace388e1774be8d608` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/contract.log` | 62 | `cdc70d96a542ea1a2ebbc4cae75d9ed837c6d247ce06fcf7a4fb5bb4ae03e07e` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/docs.log` | 2527 | `895310c46a796611afc5177e76ce29b650dfca557b91f6ae1839214e7b312640` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s0.log` | 1510 | `8c02d44cd1e4f702db5b668bca11c13b94c70355b7aab33f4c62066333da12ca` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s1.log` | 2664 | `f9431ef832dc49473205f578c66ee400d42945d5568caad368248846ec80303d` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s2.log` | 2376 | `11d3fab58dd277c06e1b34f66b75176437a42009a33e4a9f97e779845b5cd060` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s3.log` | 2100 | `7ef28918ce3489c7d47e6d6d82bc8a77c58be74d6809dabecb24bbb9e0d5b304` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s4.log` | 1908 | `c647b4ce0045b82aeebc8380984a48f288742be01f8f5abfde8562240f627461` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s5.log` | 1646 | `db1e0020ad0e491fa1e7093c59ab85cc96b26cac10630484c58e90102bf4f6d9` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s6.log` | 1578 | `b4bb96baece0778452f597d1ee89afa4fab12b75c059a1adbe0c7a136f52d34b` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-mutants-s7.log` | 1756 | `40daeb9b6d9bb52424f75d947e6845a5d7c78a3d2c3d93221eb9a777c3de50ee` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/engine-run.log` | 7205 | `f35d119842aa0acdd96fefa0f4e9d3b3d4ffb565b91211f90399d5279d0a0417` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/gaskets.log` | 1728 | `96494158f6b0cca8f5ee650920a4e67f1abcfbeccbde3b9dbf712dae5cfeb2b4` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/lint.log` | 1518 | `65c10c820f39b78f22046ea335356141869b988c64a634497334b23c3102055a` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/parser.log` | 8550 | `fac2f58d4ce1f5d1d8f82605e2129b97ba8707bb497e9e7ef1efc41dbcaca963` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/tsngen.log` | 6292 | `8546674ad0d77c1d0056f00a1b2cb2b9718c9e62345958b3715414805697d768` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/gates/head/ucpu.log` | 5608 | `93fc281a8b2f92f4aece67a687d4b0c025766df28ecef60d43462a8ef5ee6863` | repository gates at head 8f3c376d (HEAD names the commit) |
| `receipts/iface/ports-85373de0.txt` | 1366 | `ccf818c7862c06610c116859faa8658402e06cff8fae7ecdf2af34a6c8cc3c7a` | parameter and port declarations, comments stripped, at four revisions |
| `receipts/iface/ports-8f3c376d.txt` | 1366 | `ccf818c7862c06610c116859faa8658402e06cff8fae7ecdf2af34a6c8cc3c7a` | parameter and port declarations, comments stripped, at four revisions |
| `receipts/iface/ports-b9ade3a6.txt` | 1366 | `ccf818c7862c06610c116859faa8658402e06cff8fae7ecdf2af34a6c8cc3c7a` | parameter and port declarations, comments stripped, at four revisions |
| `receipts/iface/ports-e4869fd0.txt` | 1366 | `ccf818c7862c06610c116859faa8658402e06cff8fae7ecdf2af34a6c8cc3c7a` | parameter and port declarations, comments stripped, at four revisions |
| `receipts/iface/ports-sha256.txt` | 340 | `05512c22f23d3d0efda505f5df0d3fed6e6db28bf570b6a816e1299a45e017c9` | parameter and port declarations, comments stripped, at four revisions |
| `receipts/parent/docs-pin.diff` | 10447 | `0dc2502e94b3a3815ae529ca4cf97cf5d80c77f1e84c7a73b47463ceefc8b748` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/parent/local-commit-1-stat.txt` | 653 | `cd2eec58746cf5ded187cf91d6f4f2c3babf6982a57c74d0781b75fb7e30e429` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/parent/local-commit-2-stat.txt` | 230 | `987d2a47c0ba5033de5bc87875f758db15734c298f94edd14fe3734159cf2257` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/parent/local-commits.txt` | 360 | `76cf2bad5c58fc4c463c41140b79730f937e7c4ffa942cfee91618d1419892b9` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/parent/milan_dp-test-update.diff` | 2502 | `b62f420a8efe788011fc81913b756752f0ae8d250e58951e81fcda017ad4adfb` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/parent/ooc-record-rom-digests.log` | 198 | `f4c527c1252eb675f2096bd41715496915280c74612fb7b14a89781d68baaf9b` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/parent/remotes.txt` | 92 | `9aba4714491b3f2e18053f01c43d44ff2c3064c9c9494bdb5f8b718fe17ea8c1` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/parent/rom-ledger.diff` | 1228 | `cdff30d4c7ba988567dd694f507c118a89bc8bbb79ca289a80160c84329ab45a` | the two local parent commits: stats, the docs, ledger and test diffs |
| `receipts/pgates/base/GITLINK` | 81 | `b3f1d40a3a73ba6fbcf774265eaeafe8b7a2d72a4fc00c193d6c8430c914cfa3` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/PARENT_HEAD` | 41 | `d1f7f1c43829c9c01f80ffaee5941d3397db4ecc71c1e87b60083de9f312ea6e` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/TEST_RESULTS.generated.md` | 37636 | `226410db75f4387dc17e9601e4653f2c8481b32d4edac14d65d30365983146c9` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/builder-clock-contract.log` | 992 | `e34f004a2939adbbfe2702c78021e574c0660a95c7004027f7b3d4ef68d7a088` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/check_gptp_docs-selftest.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/check_gptp_docs.log` | 41 | `d8a77a32600566f0613626fd361bad845759693a08b1095dd54865c1aa25455d` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_plane-phc-step.log` | 1917 | `505f42312c6128ca469ff4f2e2c8329f2ce06e8a8f0c457ab4134b81dad52d44` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_plane-run.log` | 1620 | `3aa3202fb4c6d8c50d68de8360d8820128807f114f65354ea48cefa73329e247` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_shadow-lifecycle.log` | 11881 | `9a852b81cdc56090cc85791f8bfcb39f13b2f7394949e938ad8fd5a7d1c0edd6` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_shadow-mutants.log` | 3817 | `50dd70c1b995fa4a27851bbe1e8a5968246ac1f50b7ebdf38bb9c0607add1c99` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_shadow-run.log` | 2282 | `522fdbd165b8f3fe655e0455b37ed50d6c0b68dd1aa862c82b8c2891790356c2` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_tables.log` | 5006 | `569450666659b0a02f3d36f17818824de00a82ab6d0d395eae3808cd95002e13` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_txts-mutants.log` | 3132 | `f5c91326e30facc692f717d47f4a4afbd07304cc9074d239a895ad580a119748` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/gptp_txts-run.log` | 8800 | `220230ce343c8ce81537cecec94b56373c1c7a649f1eed5402824bd489aef8d5` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/lint_rtl.log` | 14888 | `7e3aec11012834088a37e5ba3e6b6e51587b8e5f47be2493068b73c669ed7312` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/milan_dp-gmstep.log` | 27308 | `540ce60ff1a9fd6162e39dd67093fa15d9cd7e3b39a2cf481101b12373551e0b` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/milan_dp-gptp-lat.log` | 8279 | `335e5c190b6b5558ba42b16feb545064095c1881bf9b43e12874c55a625c5b57` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/milan_dp-gptp-updated-tests.log` | 9231 | `836b0d9513643c23fd0c2e7b42f5e461a33888495e7075a98b6356dddf91156e` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/milan_dp-gptp.log` | 8076 | `a019c3aef444a58cada2cdd75800f3b23b7309a283d800f3d8b69f5a73890e03` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/ooc-tcam.log` | 299 | `26097a5c7070cd7130d3912b8fd0ed6370fbce76b4464d0e97d54141b32b7a7e` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/port_contracts-selftest.log` | 4619 | `8cbdbe06b994bf0db6efd8d9289a0a237bb965d3a771a9d536aa23e8ae0ae75e` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/port_contracts.log` | 421 | `0f55dc018c984bd32ede859aa34aca3730be44a1b51f58e461cee8258292688f` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/tsn_fuzz-ptp.log` | 3618 | `ef09dee0a776162bc0be0703e43ac0e765c53f39ae80bc7d7426730db01b2a08` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/wire_acc.log` | 4965 | `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/base/yosys-ci3.log` | 369 | `8ad6b2d40b6fb007c3e00bb305d340d3f89069ae15af9b85d20184b9cdeb22c2` | parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0) |
| `receipts/pgates/head/GITLINK` | 81 | `6edefd49a6d8dbc986be36555d3751cdaeb2b6a6e1bfeff0522ec9de42a224e0` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/PARENT_HEAD` | 41 | `4f50e9cbae509f0ae83dafda9aca6bcb8c37766b31748c0bb35aa9bf47a9dcf2` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/PARENT_HEAD_TESTS` | 41 | `2cd508b81d3f727ceb76330a658fb06749f8d2df645ad115aa1a380bafabd869` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/TEST_RESULTS.generated.md` | 37636 | `ad4de4f4c7cb7ad9aa3ad2413c34c6f7797855514b1d5b4281b57c497668e18f` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/builder-clock-contract.log` | 992 | `e34f004a2939adbbfe2702c78021e574c0660a95c7004027f7b3d4ef68d7a088` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/check_gptp_docs-selftest.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/check_gptp_docs.log` | 41 | `d8a77a32600566f0613626fd361bad845759693a08b1095dd54865c1aa25455d` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_plane-phc-step.log` | 1927 | `cbe0723cd8e4644d4b1fa3704acf801c047c2af878b45aa148eb1a08e57404c7` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_plane-run.log` | 11562 | `0315ec605fff7a4b3753d934030520787c83c32a552c59e85dc2bc7d4b55afb2` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_shadow-lifecycle.log` | 11891 | `db00a0f0d8f0de6ed3dadc4eb4d31e80f2e9ee87d503cfa3b3343cb6a5bee3f5` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_shadow-mutants.log` | 3842 | `ddd627a6ef9c39987ff76065013adec698aecd36dfb7946a4e5adcd7d04ebbcf` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_shadow-run.log` | 9083 | `b44723adca283584d3f2d1c2421687e67c82f1b6cf1ad2d7c9a445e73c2d8a9c` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_tables.log` | 9751 | `463ce6bc4370028e3d792ce5f418c2984f719ccaf91ecb3c55fa0d654bd26739` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_txts-mutants.log` | 3157 | `f4d83d24d410578f725226d34e8e153a96e4dc8b3c6abf8677c812e727d1f5ed` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/gptp_txts-run.log` | 9230 | `d2cd4e09727d5d090d59a6d973f43abaa41ccf7211e5e6388144803dfc6231ff` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/lint_rtl.log` | 14888 | `7e3aec11012834088a37e5ba3e6b6e51587b8e5f47be2493068b73c669ed7312` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/milan_dp-build-gptp.log` | 82869 | `2bf9486308edb8fc9d23e87203d7a3b23046ee625f665fce242c6af54887eabf` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/milan_dp-exec-gptp-dev-tests.log` | 1022 | `3ed69775da85c6b350655f6362938d551a61c753d98c4808d9d51032555b7bcd` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/milan_dp-gmstep.log` | 102297 | `1c806366d039d50537a8c6120ae3fbc616431bc59dad0e3b1159372d26d4c80a` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/milan_dp-gptp-lat-dev-tests.log` | 85277 | `bf9c9d92de99a2f5e1dede7d3fc1eaffb591894c385c69c67acc2a0005b3ee9d` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/milan_dp-gptp-lat.log` | 9315 | `5b6a8dbbfc21997f67b601df9789ff55f879616ab8cabae5295e82d6ec84c375` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/milan_dp-gptp.log` | 9051 | `2c0ba67150219670ec74cbf2a9869633ab368c8b69f46175fe661f6fab7df5f6` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/ooc-tcam.log` | 299 | `26097a5c7070cd7130d3912b8fd0ed6370fbce76b4464d0e97d54141b32b7a7e` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/port_contracts-selftest.log` | 4619 | `8cbdbe06b994bf0db6efd8d9289a0a237bb965d3a771a9d536aa23e8ae0ae75e` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/port_contracts.log` | 421 | `0f55dc018c984bd32ede859aa34aca3730be44a1b51f58e461cee8258292688f` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/tsn_fuzz-ptp.log` | 10258 | `679a63e86bf73e1b19ba4ec4bd163121e54d389c65bb5ff5384ca558adf3a3f5` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/wire_acc.log` | 4965 | `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/pgates/head/yosys-ci3.log` | 369 | `b66216c5dd0523bb0a70b202fea693a5452c867b889532e689638a0794391e35` | parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests) |
| `receipts/r651/head/probe-cold.log` | 149 | `cb60b88c3eb41a5dae74a1fb2854d3193893b33bd3744cd231da1cf2099a746b` | R651-1 cold, gone and warm probes re-run at head |
| `receipts/r651/head/probe-cold.log.rc` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | R651-1 cold, gone and warm probes re-run at head |
| `receipts/r651/head/probe-gone.log` | 176 | `56607c2fabc82e19a4f65c36517c2ce95df1d1707658c8c49018d22f085fb145` | R651-1 cold, gone and warm probes re-run at head |
| `receipts/r651/head/probe-gone.log.rc` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | R651-1 cold, gone and warm probes re-run at head |
| `receipts/r651/head/probe-warm.log` | 154 | `a9175dd66c65daf3817739c88c1cbfadb7027765aad71f249799249ab6cc8817` | R651-1 cold, gone and warm probes re-run at head |
| `receipts/r651/head/probe-warm.log.rc` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | R651-1 cold, gone and warm probes re-run at head |
| `receipts/r651/round1/probe-cold.log` | 387 | `a8d963a022d5838611ff00c89cfbdaedb8e4261aee3eb44ad5ae951e04e2780b` | the same probes at the round-1 head 85373de0 |
| `receipts/r651/round1/probe-cold.log.rc` | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | the same probes at the round-1 head 85373de0 |
| `receipts/r651/round1/probe-gone.log` | 268 | `d8735d5cd12691802ae12c47ae5ae9f81e235730becb85cce178058654c5b636` | the same probes at the round-1 head 85373de0 |
| `receipts/r651/round1/probe-gone.log.rc` | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | the same probes at the round-1 head 85373de0 |
| `receipts/r651/round1/probe-warm.log` | 168 | `7b40e5b99f1c38aec5011443f8c202681ed5029a2f5c1e1286dc0d2101852afe` | the same probes at the round-1 head 85373de0 |
| `receipts/r651/round1/probe-warm.log.rc` | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | the same probes at the round-1 head 85373de0 |
| `receipts/rom/layout-base.txt` | 2777 | `ee22e5bd32b2202f473adadedb33909231f41e498f1e775a68bc689beb52bb39` | ROM packing for the three images at head and base |
| `receipts/rom/layout-head.txt` | 2278 | `b30c929b7ff28133b26ccf00df6730393d4886c26b2d2719867a817c2f901773` | ROM packing for the three images at head and base |
| `receipts/scripts/control_run.sh` | 1041 | `fc202e5275d81ea35e608e91c3a302557128093fee1cdd2e3b0f99f54589276c` | the scratch scripts these receipts were produced with |
| `receipts/scripts/make_index.py` | 3004 | `3dff76cb74842e910e04382e1564b03cae98f54be8af7a7bcae6bf922f1abc66` | the scratch scripts these receipts were produced with |
| `receipts/scripts/ports.py` | 386 | `cd7f3bb2d5a28c544a878913a14d653958d497f59257107297c24726309d4714` | the scratch scripts these receipts were produced with |
| `receipts/scripts/r651_probes.py` | 6409 | `ee72840411f03b8e5a70bbf4ea771e65fa411bd402f9f218956900f61e6ba5f5` | the scratch scripts these receipts were produced with |
| `receipts/scripts/romlayout.py` | 1247 | `fbd22e03571dc178c4ae6b67ecac6d25346d2bdab998bd8239119ea199b675e9` | the scratch scripts these receipts were produced with |
| `receipts/scripts/run_by_names.py` | 643 | `69ebef696daf1cc41f37efbf80ccd8b935a1072d6b8362f2a3219927e4a5961d` | the scratch scripts these receipts were produced with |
| `receipts/scripts/shard_mutants.py` | 625 | `fa31ae1b1cdeddc1deef105663a55848a2f0fe35f0d40a962b97473b49bcecb4` | the scratch scripts these receipts were produced with |
| `receipts/scripts/verify_receipts.py` | 966 | `e24836b28cc4ded8d6d545d4b7a0be16beea2e89e3ed0a57ab21eb3f330731f5` | the scratch scripts these receipts were produced with |
| `receipts/synth/stat-base.txt` | 2764 | `fe1da321ca0298d819a6356474469a138603bf7f5beda6f8f2a1d065eefa2e91` | synthesis-proxy statistics of the engine at base and head |
| `receipts/synth/stat-head-variant.txt` | 2764 | `9ed3a82b7fa32521c250d5a9bc129fac4acf1e2eb128b7733c8065234bc7138c` | synthesis-proxy statistics of the engine at base and head |
| `receipts/synth/stat-head.txt` | 2764 | `9f6b27503980a6afd3f2602e75e7cb752185c9e9735d9b591e59b83c7f497e11` | synthesis-proxy statistics of the engine at base and head |

## Kept in scratch (over 200 KB), by size and sha256

| scratch file | bytes | sha256 | what it is |
|---|---:|---|---|

## Kept in the author scratch, not published

These files exceed the size limit. Their bytes and sha256 are the author values; the verifier does not check them.

- <data>/tmp/gptp82-a649/r2/synth/base/synth.log: 750086 bytes, sha256 372e75c5133a18a2f458524a922c8fcf79d6cfa8da0eb63a5af8f4767fc3a6a1 (full synthesis log behind `receipts/synth/`)
- <data>/tmp/gptp82-a649/r2/synth/head-final/synth.log: 744897 bytes, sha256 e4350b25f2af02a58bd57ed300df3b3bc63ffc623e3bc02546f8043a2e07e25c (full synthesis log behind `receipts/synth/`)
- <data>/tmp/gptp82-a649/r2/synth/varb/synth.log: 744567 bytes, sha256 fd64e5dded731fe622838f0e721f1d4dce3de0d9726cfc737092f9e99c121104 (full synthesis log behind `receipts/synth/`)
