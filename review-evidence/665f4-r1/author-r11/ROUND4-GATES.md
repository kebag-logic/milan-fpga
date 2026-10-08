[A560]

# Round 4 gate receipts

Head: `6f7deea15a9160761b30aaa93fe152f20d416695`. All final gates exit 0. Commands run in the foreground without output pipelines, with a 540-second timeout per command, four build workers, disk scratch and the verified SDK. `$SCRATCH`, `$SOURCE`, `$SDK` and `$DOCS_ENV` name provisioned paths. Raw and normalized receipt hashes are distinguished in ROUND4-GATES.json.

| Command | rc | Seconds | Raw log bytes | Raw SHA-256 |
|---|---:|---:|---:|---|
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir '$SCRATCH/firmware-final'` | 0 | 397.062 | 94627 | `d22db01799055ab485a80f4e35e3f12ca162230321fefe2c40eaad3785e8524c` |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep '$SCRATCH/coverage-final'` | 0 | 151.755 | 2706 | `feeb60e857d3d987dd27195a106385b11c08a9d91f4c007996baccaefd839bc9` |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.465 | 3710 | `3788b02a1c5d91d7ff2c8581f2ed09040261511d92565dd669103fee911dca0b` |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 4.475 | 793 | `9cd3b019b88560e4f902812b20cbb7d859405f50f0e686d6d71b6474287e7c94` |
| `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 57.877 | 3982 | `02268c336448885863d0308d88968cde7fe44eedb9743f0589fc01020f7eca11` |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 90.736 | 3981 | `aca49c80a6f07d0deff6a0d261526709c396b3c5cafa419c3e8bbf360a0f1175` |
| `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.166 | 6368 | `4401cee29fc27eda026415b5504bb87ef3a2102a87875731470429094f90c2a5` |
| `python3 scripts/ci_rv32_sdk.py --destination '$SDK'` | 0 | 1.368 | 1501 | `817bee33c7348e43502b4167a374a68511bda120ea38ed7e129b9ddfac1fd8c4` |
| `python3 scripts/docs_check.py` | 0 | 5.78 | 128 | `54907fa47d23a984cae9e36189e2aa0e111eb7f78280948ab3d9eb57b34acb4b` |
| `python3 scripts/docs_check.py --selftest` | 0 | 0.164 | 56 | `83cb6b9c5f7a556a8ea31ad3a751a39e6d573b00fe44ac39f5e1591022048339` |
| `python3 scripts/check_doc_paths.py` | 0 | 0.114 | 100 | `8862c3c4ca0dff440c78c90420ccb1e16ef8832addb83a595e2c2b157d092539` |
| `python3 scripts/gen_toc.py --check` | 0 | 4.378 | 94 | `327a49b965f12e7f77c6ab1ae5812d3fed54f2dd64786e400f71111120c97fbd` |
| `python3 scripts/check_em_dash.py --base c1049de1970e93d2c36ace62891ee9d947cd3191` | 0 | 3.277 | 138 | `c94b668170de3cf51a97fc13d955275db9288bbe358504294ef804e101042508` |
| `python3 scripts/check_doc_style.py` | 0 | 0.064 | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `python3 scripts/check_cpp_idiom.py` | 0 | 1.619 | 316 | `4f37b0cf782484c207b3ab78799290797a61c8aa342b598baa2500226183f384` |
| `python3 scripts/check_py_idiom.py` | 0 | 4.326 | 461 | `6d4934286986cbc4acaea61a88aa4d3d916ae3c65e94b1d9d6e2ba452353723a` |
| `python3 scripts/check_hygiene.py --check` | 0 | 0.415 | 2000 | `30d803ec0c6f62e13a0fa664d995c164c5492e0ca88f55e226a2287948dc391f` |
| `python3 sw/mailbox/gen_mailbox.py --check` | 0 | 0.164 | 26 | `9bb7d3a8faff1627f39a3bb7c9462a0b15ec8dd6c94a44c48d2fc7ac515a982f` |
| `git diff --check c1049de1970e93d2c36ace62891ee9d947cd3191 HEAD` | 0 | 0.004 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The firmware command includes all 100 control plants, all 70 SRP plants and both pin-refusal controls. Compile errors never count as caught defects. The builder bank and compiler-absent check remain with the manager under assignment 6036454509. The round-3 manager compiler-absent pass is PR comment 6036186046; it is not a new local round-4 run.
