Both shipping ALINX profiles have byte-identical complete programming data before and after the optional audio changes.

| Profile | Programming bytes | SHA-256, both sides |
| --- | ---: | --- |
| Single eight-channel stream | 3825788 | `379154b150173c369cc6aa45f25063a581362b3086bd800c05f208311aff2031` |
| Eight-stream profile | 3825788 | `e5deca48b039d8c89de687f79ee20def5e24a9210bea8d073eeacb8c1f0142c7` |

The complete programming-data field is compared directly, including every configuration word. No CRC or configuration content is masked. The surrounding containers have different metadata and their hashes are recorded separately. The extraction helper was independently cross-checked against a separately generated Arty flash image, which matched its full programming payload exactly.

Both release firmware images, initialized memories, descriptors and constraints also match. Generation used a fixed hash seed of zero. Generated top-level logic was compared after removing comments and normalizing memory-file references only after the referenced files themselves were proved byte-identical. Equal generated logic or equal resource counts were preliminary checks; the complete programming-data comparisons above are the image-identity proof.

All four corner reports pass for each side of each profile, and their slack values match exactly. The reports cover Slow and Fast models at the two stated temperature settings; those settings are report metadata within the device models, not four independent characterization libraries. See [all corner results](r2-alinx-all-corners.json), [single-stream comparison](r2-alinx-1x1-identity.json), and [eight-stream comparison](r2-alinx-8x8-identity.json).

The baseline head is `2d4c593075791f4a4beec37bf47f596231875810`, before the connected audio implementation and including the pinned network attachment. The accepted candidate head is `e5e2a91f5bff4f5e5093f71f95924ebd762f8e5f`. The compared shared RTL has not changed since these exports. Later commits changed only the optional Arty profile, its construction code, tests and documentation.

The independent reviewer recomputed both complete payload equalities and confirmed that only the containers’ time metadata field differs. All sixteen report hashes and before/after summary rows were checked, with zero failing constrained endpoints. [Shared-source lineage](r2-alinx-source-lineage.json) binds the comparison to the two source heads.

Candidate `ba2a66f72db495bd7c48700d46688de08a6c2c61` retains the same ALINX inputs. Subsequent changes affect the counted harness, optional Arty source-level/pad registers, constraints, reporting and placement grader, defect controls and documentation. None of those changed files occurs in either ALINX build source list; the four shared RTL files retain the accepted bytes. The accepted complete-image equality therefore carries forward.
