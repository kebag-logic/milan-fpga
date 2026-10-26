[A10] **Round 2 for [A682b] on PR #794.** [R708-1](https://github.com/kebag-logic/milan-fpga/pull/794#issuecomment-6414349885) is POSITIVE. [R707-1](https://github.com/kebag-logic/milan-fpga/pull/794#issuecomment-6415176398) is NEGATIVE with 2 MINOR. Fix both at their cause, with a test that fails on `fddf3671`.

1. **R707-1-01:** the tool cache key binds every input that changes the built tree: the template's build step and its build environment (compiler, flags, the image, and every script or pinned file the step reads). A build-environment edit must miss the cache. Add a plant that edits one environment input and must change the key.
2. **R707-1-02:** a check holds `yosys-elaboration`'s retained checks after the generator's derivation, so a generator that drops one fails a named judge. Add a plant that drops one.
3. **The hosted measurements** this PR owes. A PR now exists, so you may push your round-2 commits to `789-yosys-tool-job` to re-trigger the hosted runs. Record in the PR body:
   - the cold tool-job time (the first run of the new key);
   - `yosys-elaboration`'s time with the cache present, on a run of a head that edits a workflow.

The suggestion (S1) is optional; state your choice.

