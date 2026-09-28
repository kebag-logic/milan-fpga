[A410]

Closes #577

## Status

Local head: `a53682ed38720de758006602a19f78c8e40d69da`.
Implementation and complete builder/documentation gates pass.
Independent review and publication remain pending.

## Description

Validate the packed shipping image before the builder returns it.
L6 requires the served clock-source list to be the identity sequence.
L10 checks the rate offset, walk count and exact full-word extent.
Each refusal names its cause.

The checker reads index rows and descriptor fields from emitted bytes.
It derives the rate walk limits from the pinned processor consumer.
The ownership matrix records the implementation and discriminating evidence.
The loader scope and processor pin remain unchanged.

## How to reproduce

```sh
python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml -o /tmp/image-contract-build
```

## How to validate

```sh
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
GIT_DIR=/dev/null python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_feature_status.py --self-test
python3 scripts/check_py_idiom.py
```

Gate 36b covers legal one/eight-rate boundaries and each named refusal.
It also checks every descriptor across configurations, strides and repeated runs.
All five shipping images remain byte-identical to the assigned base.
The committed test kills eight required refusal deletions, four defensive
refusal deletions and removal of the image-boundary hook.

## Definition of done

Implementation and mutation evidence are complete.
Full builder and documentation gates return rc 0. The existing gate 11
calibration arm remains NOT RUN because its placement report is absent.
The compiler-absent audit also returns rc 0, explicitly recording its
unavailable instruments; those instruments passed in the compiler-backed run.
Independent reviews remain with the assigned internal and external reviewers.
