[A358] TAKEN

Branch: `397-service-budget`, base `ac18b50968b12efe4d15c0a06301264b35656b31`.
Authoritative references: the re-scope in issuecomment-5854787465; REQUIREMENTS section 1 and REQ-CSR-02; FR_NFR NFR-SCOUT-01/03; SAVED_STATE_FASTCONNECT section 9.4; BAREMETAL_FIRMWARE build and UART contracts.
Interpreted scope: a sibling product-CPU simulation harness at 50 MHz, running unchanged firmware and observing external markers or enclosing intervals. The existing capture harness remains unchanged. Report CPU-side time separately from flash waits, with explicitly bounded scenarios. The existing flash simulation handles reads only, so the sibling must supply an independent writable device model for commit measurements.
Validation plan: new harness and its over-budget self-test; `python3 -B scripts/check_nvm_capture.py`; `python3 -B scripts/check_feature_status.py --self-test`; documentation gates; `git diff --check`.
Blockers: none identified. Every requested duty has an external marker or an enclosing boot/command interval. No hart-count decision or FR/NFR change is part of this lane. Reviewers remain [R348] and [R349].
