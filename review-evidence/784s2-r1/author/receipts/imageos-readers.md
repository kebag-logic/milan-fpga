# ImageOS readers in actions/setup-python@v5 (read-only gh api, 2026-10-26)

act sets ImageOS from the runs-on label (ubuntu-latest -> ubuntu20, ubuntu-24.04 -> ubuntu24), so the replay's ImageOS changes with this PR.

- v5 resolved to commit a26af69be951a213d495a4c3e4e4022e16d87065
- dist/setup/index.js: 3880887 bytes, sha256 2ef3f65c84bd14c7dd472795793e6cfe869bc6b42e78de8294e24659e9c851ae, occurrences of ImageOS: 0
- dist/cache-save/index.js: 3523970 bytes, sha256 abb8a49210dbf5506092452b24ad76025ab79a1cf840315d6612db4119bfadeb, occurrences of ImageOS: 0
- this repository: git grep ImageOS/ImageVersion over .github scripts ci: none

## Pinned act 0.2.89 source (milan-ci5 build source tree act-4f411281)

```
pkg/runner/run_context.go sha256 692c9c91e50fc3afc6c55187ca1fccf0717827d2c990113dc0fda9612237af03
		if platformName != "" {
			if platformName == "ubuntu-latest" {
				// hardcode current ubuntu-latest since we have no way to check that 'on the fly'
				env["ImageOS"] = "ubuntu20"
			} else {
				platformName = strings.SplitN(strings.Replace(platformName, `-`, ``, 1), `.`, 2)[0]
				env["ImageOS"] = platformName
			}
		}
cmd/platforms.go sha256 c0938412c72f92fee1a7b396a32cf63ccd9e0b92b7314c316880fdbb5998354f
	platforms := map[string]string{
		"ubuntu-latest": "node:16-buster-slim",
		"ubuntu-22.04":  "node:16-bullseye-slim",
		"ubuntu-20.04":  "node:16-buster-slim",
		"ubuntu-18.04":  "node:16-buster-slim",
	}
```

So the replay of a ubuntu-24.04 job sets ImageOS=ubuntu24, where a ubuntu-latest replay set ubuntu20; and without a --platform entry act would run ubuntu-latest on node:16-buster-slim (R697-1-01's wording).
