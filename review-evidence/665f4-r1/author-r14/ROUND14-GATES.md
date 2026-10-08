[A560]

# Round 14 gate table

All 87 final command receipts return zero.

| Gate | Command | rc | Seconds | Log bytes | SHA256 |
| --- | --- | ---: | ---: | ---: | --- |
| docs-00 | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.264 | 415 | `2c7fe5c5be823ea2eae34ad831e279e93d739462a46cc3667f17856d7b984ee8` |
| docs-01 | `python3 scripts/gen_hdl_reference.py --output $SCRATCH/milan-hdl-reference` | 0 | 1.921 | 414 | `4172b4a9fe8dcd2abf25ca128c8793a2f5d604eb257e941e3bed1d69f3c33def` |
| docs-02 | `python3 scripts/docs_check.py` | 0 | 5.983 | 128 | `03c9094ff213e3c806d007b5cbf63cf12e2c229ff5118b64a3de3e36b4738bc1` |
| docs-03 | `python3 scripts/check_em_dash.py --base 154722e14781c7373f3229420b6e007f9bcf9835` | 0 | 3.475 | 138 | `517f34249cf01c426095bf908de543343d7da2c98695465f925402a7f3e1b4bb` |
| docs-04 | `python3 scripts/check_doc_style.py` | 0 | 0.114 | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| docs-05 | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.067 | 33 | `0acc8195c60dd145a8f17d24b7b07c29074ac131d71893f9cef5f880239dd909` |
| docs-06 | `python3 scripts/check_gptp_docs.py` | 0 | 0.214 | 41 | `d8a77a32600566f0613626fd361bad845759693a08b1095dd54865c1aa25455d` |
| docs-07 | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.264 | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| docs-08 | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.517 | 61 | `74408f0fbcdfc1c7e22f6eccd3eb299da61cabe9bb4526eed416b31a8bf61e16` |
| docs-09 | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.465 | 60 | `85ddf25d9a99974b71a9c165cbfbbf390be3d7bf74f081b4cc669622a0a562b9` |
| docs-10 | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.365 | 60 | `51058c96a481bf763246394b619601227bdec11b6b11ddcaa1d6f57593d2f1f4` |
| docs-11 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.515 | 61 | `7c7ad79fa685d29607abf71e3a99d98855fd7ffa1ba5fbf7de23bfb41a33c8fa` |
| docs-12 | `python3 scripts/check_solution_docs.py` | 0 | 0.164 | 87 | `48ac84ddbd532247deb21834ee60bd4b7322f69bb9ab9fc5f9901969ccb38c42` |
| docs-13 | `python3 scripts/check_solution_docs.py --selftest` | 0 | 3.024 | 59 | `c57d3ed2e5c9be43085106227b69fe55f866b1198ad209fbb27f940e5757ec30` |
| docs-14 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.465 | 54 | `d1ae5c433282f7f6f0b3df74fb92180c7567e27714311c0b98d16e6f237f8e55` |
| docs-15 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.568 | 60 | `51bca8fb66fd6f0acc480e3364f74fd7a4874946b191468bfbe20ad159cca889` |
| docs-16 | `python3 scripts/check_submodule_docs.py` | 0 | 0.516 | 47 | `79be302e03c97636315bf0b9d13d7d4160d1b0ac67f93f42874e51838b6de78c` |
| docs-17 | `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.064 | 66 | `54dbecff3ad17dc651e86c7b313ef57fa96baf89fb40f0fb90af4bbb8ddc802b` |
| docs-18 | `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.164 | 77 | `8439889f74aa49f8d61f50d6b525f358d0774a4133b54cd9895edad971302d42` |
| docs-19 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.315 | 58 | `b3f8f3a790f92f14932f7c8a8c6b7ad9f33d327b6a6cfe653364d5f34617f8e3` |
| docs-20 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.415 | 54 | `4d9e7670f2a4615d27d64a23c95a4882fd923026e00120f90d44a031c39b61d5` |
| docs-21 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.365 | 52 | `411f08b7121f1a0c6b28105fe433aa4561caad5a8e4caf9e7a6c6aa2fd33cac9` |
| docs-22 | `python3 scripts/check_diagram_pngs.py` | 0 | 0.365 | 66 | `05e0fcfa26a97494e8983dcfca3ad89cdaf91e390acbfb9dbdfb6f614cba4e51` |
| docs-23 | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 7.339 | 59 | `918e8cc85a2a2b0d45eeb3f0c7b006824c81e2ed404a535eded095b09d875dc5` |
| docs-24 | `python3 scripts/check_feature_status.py --self-test` | 0 | 1.066 | 1500 | `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184` |
| docs-25 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.32 | 118 | `d0be3b6428ae2079134f2a21b2972c524a26103b0e9c8b64039bb24ae22797dc` |
| docs-26 | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.214 | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| docs-27 | `make -C gptp-processor docs` | 0 | 0.766 | 2668 | `a4af3015d9c6ced375d65a0284c5936d6b40247347da058fee9503a41badf40f` |
| docs-28 | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.215 | 2565 | `34d85283c432e38af30c33dcc6de6b85208e1ec98a538b78e68061d27421972b` |
| docs-29 | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.064 | 728 | `10f526cea8560a3a39135260553e767b316076d7598559fb5f07e8cfab2c5363` |
| docs-30 | `python3 scripts/check_baremetal_only.py --check` | 0 | 19.983 | 72 | `5856a73c909c1a82bfed7c1ea70e5214349dc945a7e3989e08cb4265997f63d3` |
| docs-31 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 7.489 | 43 | `09b491b87735efaef68eafe7f45f4fe4ba1f8ad036c0d252d2a93a00906d51f8` |
| docs-32 | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.268 | 6389 | `5fe2ee75f993506ab0dbe190c8d00c0acf66beee3e64c40ecc1396bfa57c1487` |
| docs-33 | `python3 scripts/ci_rv32_sdk.py --destination $SDK` | 0 | 1.828 | 1501 | `817bee33c7348e43502b4167a374a68511bda120ea38ed7e129b9ddfac1fd8c4` |
| docs-34 | `python3 scripts/check_nvm_record_space.py` | 0 | 2.525 | 2578 | `cf53746e34d5ec76dc263f5ce98c17e9f1b227048b67c9e6bdbb8e798007f4f0` |
| docs-35 | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 47.811 | 7010 | `8e636c8b39e0ce66934ec2a3a7088ef7e6be29b5820a3a87f147d40c612320c6` |
| docs-36 | `python3 scripts/check_nvm_capture.py` | 0 | 0.866 | 324 | `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439` |
| docs-37 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 75.897 | 5189 | `4928189ff11ec557fe7fa80a3eb28b91ba56eed839cb6accf24847335a2d516d` |
| docs-38 | `python3 scripts/check_soc_sources.py` | 0 | 0.164 | 85 | `7ea77f321df0437a49feae4436006813f0653a8151945dbf7601fe0e5e289033` |
| docs-39 | `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.264 | 1501 | `d877c9fa9a5d1db2854c5ed3486ca7d2d135944cf3953143bdf63b554f8c3dc0` |
| docs-40 | `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.601 | 3208 | `36285e124542418c660615cce715d7a1479327c9e1d849139a46b86f00868f3f` |
| docs-41 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.695 | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| docs-42 | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 3.162 | 3300 | `418b0ce0f1f8a55805a4c0e75385ae0f3c18b83b3af16598f5cfc45b40591f1d` |
| docs-43 | `python3 scripts/measure_naming.py --check` | 0 | 0.565 | 36608 | `0ece46e4cc0fc61cd15de56f4fd34704f1ca469845684b20d7a6d118d890d49e` |
| docs-44 | `python3 scripts/measure_naming.py --selftest` | 0 | 0.566 | 4026 | `20635e2ee5994ddc3555ad8acef6af506885fef1ccec25b9c4efb88ab4984c02` |
| docs-45 | `python3 scripts/check_port_contracts.py` | 0 | 2.824 | 421 | `c4a0b9e89f19df346a9b837d45d0eb04d65ab38de0a07edd5adef08c408ef5f8` |
| docs-46 | `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.277 | 4619 | `8cbdbe06b994bf0db6efd8d9289a0a237bb965d3a771a9d536aa23e8ae0ae75e` |
| docs-47 | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.769 | 6085 | `bbf0264b3cc1beedf3b725b71c379498d33eceeff22f734695af87a77240563e` |
| docs-48 | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.769 | 6597 | `ef92c9eb4e29bf495c938a2ebe16cb2ec7896671a4e7a63ae465c76f5ca8373a` |
| docs-49 | `python3 scripts/check_todo_ownership.py` | 0 | 1.868 | 161 | `3c59f22784200901ba3b70073fd723f68144dd48a7fe76972c5bc7132365ce51` |
| docs-50 | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.969 | 2584 | `696cea82f33dcda09f3d8b1047ee2682f9ca7c6da9348a07813eaf3d3d6f978b` |
| docs-51 | `python3 scripts/measure_test_evidence.py --check` | 0 | 6.913 | 14871 | `30d8fb61edeb6851416d834317922c33ff8744eccd8c133a10e72e49282400bf` |
| docs-52 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.085 | 5895 | `9665bb06c04a7169e36eb253ae73089a4786ac51c2db1b5c8f5a67e8e090f9b2` |
| docs-53 | `python3 scripts/check_hygiene.py --check` | 0 | 0.415 | 2000 | `f75f93e8ae0271eeeafdd63ba9c66b09cba2a8bbbe0e2d0cff7b774acdcdcc7e` |
| docs-54 | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.416 | 1847 | `2c7b5cb25dc4cc0407fc27441f4bba2291c74fa2aa2b22f1276e129651f615a8` |
| docs-55 | `python3 scripts/check_sv_idiom.py` | 0 | 0.515 | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| docs-56 | `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.465 | 2955 | `0e4826a9db5e2e72c2d3a62bfef0d017bacb9a51238353b44b469b7dbd1c5f9b` |
| docs-57 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.718 | 316 | `c4e43580d928601e38756c0a0ed7007f62e742d81ef33787999b457eb26f922f` |
| docs-58 | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.869 | 3593 | `7fd74c4ebf8b2f0a9812a20518981f63c8350a34c535bcde2c7fa6c58fbec2b9` |
| docs-59 | `python3 scripts/check_py_idiom.py` | 0 | 4.478 | 461 | `9b4bb38c8b1ae551ac52ecdbbfbdf14f45f0cf99550765ad41d14befc4f135b5` |
| docs-60 | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.478 | 2531 | `d7413b83955948950d15e364a901be97cf05148dad38e97be07b2d63eb46406d` |
| docs-61 | `python3 scripts/check_sh_idiom.py` | 0 | 0.264 | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| docs-62 | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.264 | 2461 | `b9af4f07f8aabdddc7af15799e1e06640c7a0a356ef30681b059784e385d3a57` |
| docs-63 | `python3 scripts/ci_events.py --check` | 0 | 0.214 | 167 | `617e44ed66b13896b9bf7fa2c76c7242990622e9ced9ba79a693484ad4bd4a77` |
| docs-64 | `python3 scripts/ci_events.py --selftest` | 0 | 17.804 | 151471 | `db420a4b83a96d53cefdd88cc69322ed20d7ac02ec28012258d3175fdb7eea37` |
| docs-65 | `python3 scripts/check_doc_paths.py` | 0 | 0.114 | 100 | `920e2c5342a247a9fc249045f66da047aed7f636918fb7965f8f81e90ab1c9ce` |
| docs-66 | `python3 scripts/check_archive.py` | 0 | 0.415 | 93 | `69d45782911c2958be2fef681f849e9b3915293c938de331bb6885dab21fd46c` |
| docs-67 | `python3 scripts/check_archive.py --selftest` | 0 | 0.064 | 35 | `83aa5efe967935657a1678bf63262a7c435d29d571cc08dd2ae8cf6f8569d34a` |
| docs-68 | `python3 scripts/gen_toc.py --selftest` | 0 | 0.916 | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| docs-69 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.123 | 64 | `508dfb485babef5b0c1da1d36e187721f1e3640f232bfe9b8323d4b94379a1ee` |
| docs-70 | `python3 scripts/gen_toc.py --check` | 0 | 4.835 | 94 | `fddbe675291483bdeb63f3889244a9ff3eedf33303fdb81d182eaf3966f7357a` |
| docs-71 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.114 | 3596 | `9f126bf9dfc7cb552a2414b98d2792449dc4ae126395997750d5039cb896f022` |
| docs-72 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 15.156 | 19678 | `4c9549b33f4c9cde9eafa1b568817657010b6ec43ab3850f9ba9eaf6448eaf28` |
| docs-73 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.466 | 9268 | `e424a100293545585d0d9cd212edab2d524ee6f56cdc0568f1cb9684f6049274` |
| docs-74 | `python3 scripts/check_entity_shape.py --self-test` | 0 | 56.994 | 25693 | `016d0ddb5406a250386877b6de32a63744377f51b3c0ed4249a855b6c681ddb2` |
| runner-final | `bash $SCRATCH/runner-job.sh` | 0 | 4.177 | 37154 | `455eca12b5e8082311119fa4e879bc146b8c40a401c3ca29f5a3ad83e6474e8b` |
| runner-mutants | `bash $SCRATCH/runner-mutants-job.sh` | 0 | 3.864 | 851 | `6ad90fe019b515ea84eeca2178938ff35cfaff047ac44ddde421ee2dd64ad55c` |
| ctrl | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir $SCRATCH/ctrl-build` | 0 | 244.576 | 69707 | `909972aa8be1622477be9ae37d37d152b543d9a6d51ada4088336fe536c5e534` |
| builder | `bash $SCRATCH/builder-job.sh` | 0 | 1167.402 | 102954 | `c48124ac658aa40f096716b90fc07c8dfbdad180aa3066994e72deeba49a0213` |
| compiler-pinned | `python3 sw/builder/test_firmware_compiler.py --sdk-destination $SDK --audit $SCRATCH/rv32-pinned.jsonl` | 0 | 972.832 | 51055 | `8a1bf57abf5404aff6486fb6d1d6b83e4b07c79175862d4fa57b8e42075d1f46` |
| compiler-controls | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | 1.868 | 138 | `f6da142138888df7ecd9ef31e7b86895260648309005e1400148d78004e385d7` |
| docs-no-git | `python3 scripts/docs_check.py` | 0 | 5.675 | 196 | `06a3dc54a73d1c0a68523d1ed92241e2dca7eee05706d891dd48d62814c2eab0` |
| features-no-git | `python3 scripts/check_feature_status.py` | 0 | 1.066 | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| integrity | `python3 $SCRATCH/integrity.py $SOURCE $SCRATCH/integrity-result.json` | 0 | 0.214 | 1375 | `8b037c55ff5e314fb64a0dfc680aa1b7dc3ecb18c8a19531cf42692b61245936` |
| builder-integrity | `python3 $SCRATCH/integrity.py $SCRATCH/builder-tree $SCRATCH/builder-integrity-result.json` | 0 | 0.315 | 22890 | `a80bcdbffe531a6cfa6fc315a371ec0741a3cc124f204214e7af272086b21134` |
| compiler-integrity | `python3 $SCRATCH/integrity.py $SCRATCH/compiler-tree $SCRATCH/compiler-integrity-result.json` | 0 | 0.415 | 1375 | `8b037c55ff5e314fb64a0dfc680aa1b7dc3ecb18c8a19531cf42692b61245936` |
| diff-final | `git diff --check 154722e14781c7373f3229420b6e007f9bcf9835 HEAD` | 0 | 0.016 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
