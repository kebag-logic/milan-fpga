[A615] TAKEN - PR #738

Head: `18f2df92b13cb3f4036b073ed76940187bf10487`; branch: `737-ci-image`.

Resuming under PR #738 comment 6165220472. Run only the unchanged `test_baremetal_profile_contract` with `--require-rv32` inside the final image as a background job without a timeout; record the completed verdict and wall time, then update the evidence packet. The two cold builds stand. No implementation changes or push.
