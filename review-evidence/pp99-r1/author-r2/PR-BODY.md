[A302]

Complete the integration parameter inventory

Closes #99

The integrator guide previously omitted public top-level parameters. Section 2 now lists every overridable parameter and links each to its authoritative owner without copying defaults. Diagram 21's editable master and committed render carry the same complete inventory. A new inventory check runs in CI and the documentation check target.

[A244] authored round-1 commit `52659df180cd74592b11aaf208efe37bd243ba79`. This completion merges main `60152f3ff068b81333326b5081b5303253ba7fe7` into that work and documents four checker functions to satisfy the consumer's existing idiom gate. The parameter header remains byte-identical to `008edbbf`; all 24 names still match the guide and diagram. No authored RTL or default changes.

Validated at `663d50d65ff49c33b153107b2f79d6f3c5725799`: every repository CI gate, the documentation check target, all 33 suites (1,014,637 checks), RTL lint, historical figures, and portability returned 0. All eleven parent-consumer checks returned 0, including 371 passing integration checks. The final parent gitlink is committed locally at `ce65f96b8aee17dc589ca253188801da9db9ceef`.

Round 2

Fixed the five parameter-owner links using the existing descriptor-memory anchor and a new explicit response-memory anchor. Section 7 of the verification plan now documents the parameter inventory gate, including missing, extra, duplicate, empty and unparseable inputs. Only the three assigned documentation files changed.

Validated at `9cde1c19dbfd859257be8e012d4455856fcfce3b`: all assigned documentation and link gates returned 0; the reviewer-equivalent anchor check covered 59 links with 0 dead, including the edited local anchor rendered by GitHub.
