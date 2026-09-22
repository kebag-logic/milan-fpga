https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5778469246
[A10] MANAGER VALIDATION COMMAND CORRECTION

The manager found stale explicit endpoints in the candidate-bank `git diff --check` command: #478 candidate72e16 used source149, #372 candidate60c522 used author5bbf, and #423 candidate df53 used the inherited5bbf endpoint (which is absent there and exited128). Other commands ran from their recorded candidate checkouts. No source defect or changed acceptance is established by this runner-spec error.

Each lane will now execute `git diff --check <recorded live base> <exact candidate commit>` as a separately recorded correction. Original commands, exits and logs remain immutable; the corrected result replaces only that invalid candidate-whitespace claim in an explicitly composed final bank. All other completed commands retain their original receipts and are not rerun. Candidate source integrity is verified again. The #423 bank cannot be called complete while its other command or correction is pending.

The earlier #372/#478 builder comments correctly reported all raw command exits as zero but overstated the candidate endpoint of this one check. This comment corrects that evidence scope; no failed or stale command is relabeled as a pass.
