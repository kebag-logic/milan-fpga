[A253]

Closes #43
Closes #49

GET_STREAM_INFO now reads input failure information from the SRP registrar and probing/ACMP status from committed listener records. Input selectors 5 and 7 are handled internally, and selector 4's failure-code byte uses the same captured SRP sample. The top-level interface and parent instantiation stay compatible.

Solicited and unsolicited responses use the same gather. Changed failure information and committed probing status notify controllers; missing descriptors return a full zero body. The architecture and integration documents describe internal ownership and sampling.

Response tests drive real binding, discovery, probe timeout, settle, failure registration, withdrawal and unbind transitions across two sinks, including reset and a missing descriptor. Eight retained mutations fail named checks; golden and restored controls pass 416 checks each.

A new binding first becomes ACTIVE, then reaches PASSIVE after unanswered probes and backoff, following Milan 5.5.3.5.3 and 5.5.3.5.29. Both states are checked. Synthesis for the default shape changes area by +640 LUTs (+2.28%) and +784 registers (+2.58%), with no block RAM increase.

Validation: 16,317 regression checks pass, including 1,876 processor-top checks; documentation, lint, historical figures and portability gates pass. The parent consumer simulation passes 371 checks and its source lists pass. Its three pin-guarded checks reject a checkout-only update because the indexed pin stays unchanged. All five parent checks pass in an isolated copy of the identical parent tree with the candidate gitlink staged. The designated parent index is untouched.
