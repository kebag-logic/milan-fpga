[A177] ACCEPTANCE CONFLICT: PTOF restore has no implementation at the authorized pin

The corrected #403 contract asks for legal restored PTOF and default/restore precedence. The selected PP revision 8452f564294300a82d56eed464276576f65f4d58 only adds the default-VID seam. At this revision, protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:176,262,273,304-305 holds a volatile offset/valid array, reset to invalid and written only by the AECP state-port command path. No restore input exists. The parent firmware's NVM_ID_PTOF/NVM_PL_PTOF entries reserve and validate record geometry; they do not replay a PTOF into that store. hdl/milan/KL_pp_shadow.sv:920-923 explicitly retains the no-record-writer pending state.

The authoritative current design entry docs/design/SAVED_STATE_MATERIALIZATION.md:6-13 is PROPOSED and says nothing on that page is implemented; its section 1 names the offset among the non-binding groups without a writer. This is #500/#70 work, not a behavior this declaration lane can preserve end to end. A hierarchical store injection could prove fold precedence but would not be a restored-PTOF measurement.

Options for the manager's public decision:
1. Clarify this bundle's acceptance to preserve and test per-output stored-value/default precedence, with real PTOF persistence/restore explicitly unmet and owned by #500/#70. Keep legal SET_STREAM_INFO and transmitted timestamps fully measured here. No claim of a restore pass.
2. Retain actual restored PTOF as mandatory for #403 and block this bundle's review-ready state until a separately authorized, reviewed materialization prerequisite exists. That would also require revisiting the currently exact-only donor pin authorization.

Recommended: option 1 matches the declaration-only scope without importing unapproved donor work. I am continuing independent declaration/reset/boot/RX/runtime work, but will not publish REVIEW READY or mark restored PTOF met without a public resolution. No test has been substituted for restore evidence.
