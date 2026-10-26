# Hosted image evidence (read-only, gh run view --log), excerpts

## run 40187576861 (docs, PR #783 head 91bf51e4), job 121179871493 docs-check: failure
2026-10-25T13:18:20.1119549Z ##[group]Operating System
2026-10-25T13:18:20.1120810Z Ubuntu
2026-10-25T13:18:20.1121733Z 26.04.1
2026-10-25T13:18:20.1122779Z LTS
2026-10-25T13:18:20.1123716Z ##[endgroup]
2026-10-25T13:18:20.1124614Z ##[group]Runner Image
2026-10-25T13:18:20.1125929Z Image: ubuntu-26.04
2026-10-25T13:18:20.1127235Z Version: 20261012.163.1
2026-10-25T13:18:43.3076471Z ERROR: Cannot install PyYAML==6.0.2 because these package versions have conflicting dependencies.
2026-10-25T13:18:43.3078493Z ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts
2026-10-25T13:18:43.3566938Z ##[error]Process completed with exit code 1.

## run 40187422760 (docs, dev push d385b38e), job 121155262818 docs-check: success
2026-10-25T11:32:56.3873224Z Image: ubuntu-24.04

Full job logs were read, not kept: run 40187576861 job 121179871493 log sha256 c0d46815a865d7099fd8a6309f99187a50e5d870cb93c98ae21dee7e0dd41e2f (78813 bytes); run 40187422760 job 121155262818 log sha256 a629f8c18ededfbb1437c54dc33c6314b522afb6a765e24d83954238044f7610 (77900 bytes).
