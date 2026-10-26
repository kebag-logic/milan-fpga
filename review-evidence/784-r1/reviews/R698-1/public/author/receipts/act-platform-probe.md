# Pinned act: does it serve a second runs-on label? (STOP-condition probe)

Binary: act version 0.2.89+milan-ci5, sha256 4d30fb23a2d2485ea7a48c6c679d4dd3b482eafe73d55c1ec544842f96bbd3f5 (30195511 bytes), equal to the build receipt's binary_sha256.
Source read: cmd/root.go:82 declares --platform/-P as a StringArray (repeatable); cmd/platforms.go newPlatforms() maps each 'label=image' entry over act's defaults (ubuntu-latest, ubuntu-22.04, ubuntu-20.04, ubuntu-18.04 -> node:16 images); pkg/runner/run_context.go:796-826 isEnabled() skips a job whose label maps to no image ('Skipping unsupported platform') and Executor() returns nil for it.

Probe: dry run (-n), no privilege, private HOME and XDG roots, an empty environment, DOCKER_HOST pointing at a socket path that does not exist in a fresh scratch directory, so no Docker daemon is reached. The job failures below are that missing socket, by construction.

Command shape (scratch paths elided):

    act push -n --directory <scratch>/repo -W <workflow> --container-daemon-socket - --concurrent-jobs 1 --env MILAN_CI_CPU_RANGES=0-15 --env MILAN_CI_FALLBACK_CPUS=12 -P ubuntu-latest=catthehacker/ubuntu:full-latest [-P ubuntu-24.04=catthehacker/ubuntu:full-latest]

## Fixture labels.yml

    name: labels
    on: push
    jobs:
      on-latest:
        runs-on: ubuntu-latest
        steps:
          - run: echo latest
      on-2404:
        runs-on: ubuntu-24.04
        steps:
          - run: echo 2404
## A. Both labels mapped (this change's platform list): exit 1 (no daemon by construction)

    time="2026-10-25T18:36:05+01:00" level=info msg="Using docker host 'unix://<scratch>/nosock/docker.sock', and daemon socket '-'"
    *DRYRUN* [labels/on-2404] ⭐ Run Set up job
    *DRYRUN* [labels/on-2404] 🚀  Start image=catthehacker/ubuntu:full-latest
    *DRYRUN* [labels/on-2404] CPU range reserved before container creation
    *DRYRUN* [labels/on-2404]   🐳  docker pull image=catthehacker/ubuntu:full-latest platform= username= forcePull=true
    *DRYRUN* [labels/on-2404] failed to connect to the docker API at unix://<scratch>/nosock/docker.sock; check if the path is correct and if the daemon is running: dial unix <scratch>/nosock/docker.sock: connect: no such file or directory
    *DRYRUN* [labels/on-2404]   ❌  Failure - Set up job
    *DRYRUN* [labels/on-2404] 🏁  Job failed
    Error: failed to connect to the docker API at unix://<scratch>/nosock/docker.sock; check if the path is correct and if the daemon is running: dial unix <scratch>/nosock/docker.sock: connect: no such file or directory

## B. Only ubuntu-latest mapped (dev's platform list): exit 1 (no daemon by construction)

    time="2026-10-25T18:36:05+01:00" level=info msg="Using docker host 'unix://<scratch>/nosock/docker.sock', and daemon socket '-'"
    *DRYRUN* [labels/on-2404] 🚧  Skipping unsupported platform -- Try running with `-P ubuntu-24.04=...`
    *DRYRUN* [labels/on-latest] ⭐ Run Set up job
    *DRYRUN* [labels/on-latest] 🚀  Start image=catthehacker/ubuntu:full-latest
    *DRYRUN* [labels/on-latest] CPU range reserved before container creation
    *DRYRUN* [labels/on-latest]   🐳  docker pull image=catthehacker/ubuntu:full-latest platform= username= forcePull=true
    *DRYRUN* [labels/on-latest] failed to connect to the docker API at unix://<scratch>/nosock/docker.sock; check if the path is correct and if the daemon is running: dial unix <scratch>/nosock/docker.sock: connect: no such file or directory
    *DRYRUN* [labels/on-latest]   ❌  Failure - Set up job
    *DRYRUN* [labels/on-latest] 🏁  Job failed
    Error: failed to connect to the docker API at unix://<scratch>/nosock/docker.sock; check if the path is correct and if the daemon is running: dial unix <scratch>/nosock/docker.sock: connect: no such file or directory

## C. only2404.yml, only ubuntu-latest mapped: exit 0, the job never ran

    name: only2404
    on: push
    jobs:
      on-2404:
        runs-on: ubuntu-24.04
        steps:
          - run: echo 2404

    time="2026-10-25T18:36:16+01:00" level=info msg="Using docker host 'unix://<scratch>/nosock/docker.sock', and daemon socket '-'"
    *DRYRUN* [only2404/on-2404] 🚧  Skipping unsupported platform -- Try running with `-P ubuntu-24.04=...`

Conclusion: a second -P entry maps ubuntu-24.04 to the same runner image with no change to act, the dispatcher patch or the image; no STOP. Without it act skips the job and can exit 0.
