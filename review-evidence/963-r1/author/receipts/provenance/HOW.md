# Firmware evidence carried to the final comment-only commit

The tested firmware is `e9627b31ef8b35f8804b959ebebabe6f5c29646b`.
`1b3e27ce` changes the design document only. `9860395a85e1cb3c41f33cb93b0e039a04e90290`
changes only the check-loop comment in `aecp_maps.c`.

`proof.json` compares the complete `-E -P` translation unit from the tested revision with
that from the final head, using each of the 16 measured arm images' generated entity
header, RV32IM/ILP32, freestanding C11 and NDEBUG. All are byte-identical.
No code, constants, interfaces or tests change after the tested firmware revision.
