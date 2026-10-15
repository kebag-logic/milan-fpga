[A615] TAKEN
Branch: 737-ci-image at fa7347fc59173f90e4feec2df207692e6e6e72ec
Authoritative references: assignment #737 comment 6160953880; CONTRIBUTING.md; REQUIREMENTS.md section 8; docs/testing/CI_WORKFLOWS.md.
Interpreted scope: derive the complete CI tool inventory, build a checksum-pinned multi-stage tools image, record layer/image locks and in-image smoke evidence, and document rebuilding and digest consumption. Workflows remain unchanged. Executor [A615]; reviewers [R638] and [R639]. The explicit lane assignment authorizes work while the shared issue board still reads Backlog.
Validation plan: inventory drift controls, checksum verification, reproducible image build, each tool version and smoke check inside the image, and all touched repository gates. Record image size and build time.
Blockers: none identified yet; STOP if a required tool cannot be checksum pinned. Manager owns push and publication.
