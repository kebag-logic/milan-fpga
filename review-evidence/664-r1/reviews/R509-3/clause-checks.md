Primary-clause checks at the reviewed head

The local primary PDFs named and hashed in standards-identity.json were inspected. Full extractions and one page render were kept only in scratch and are not publication artifacts.

| Authority | Checked result | Requirement location |
|---|---|---|
| IEEE 802.1Q-2018 Table 10-1 | Customer Bridge MVRP uses 01:80:C2:00:00:21. | REQUIREMENTS.md:73,84 |
| IEEE 1722.1-2021 8.2.1 | ACMP transmission uses multicast. Own-unicast reception is a project tolerance, not a normative transmission claim. | REQUIREMENTS.md:69,85 |
| IEEE 1722.1-2021 Table B.1, printed page 387 | Visual inspection confirms 91:E0:F0:01:00:00 for ADP/ACMP. The extracted address glyphs were corrupted, so the rendered table was checked. | REQUIREMENTS.md:68,69,86 |
| IEEE 1722.1-2021 9.2.2.7 and 9.2.2.8 | The target identifies the command destination; the controller identifies the command originator and response recipient. | REQUIREMENTS.md:70 |
| Milan v1.2 5.4.5.3 | An entity originates CONTROLLER_AVAILABLE to monitor a registered controller and consumes the response. The two-sided identity rule admits that return path. | REQUIREMENTS.md:88; docs/reference/FR_NFR.md:406 |

No clause conflict with owner decision 6014311316 was found. The PDFs are authority for protocol claims; the public owner decision is authority for the stricter project acceptance filter and the receive tolerance.
