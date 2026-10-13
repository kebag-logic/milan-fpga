#!/bin/sh
set -eu
repo=$1
packet=$2
shift 2
exec bwrap --unshare-all --die-with-parent --new-session \
 --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/sbin /sbin \
 --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 --ro-bind /etc/ld.so.cache /etc/ld.so.cache \
 --ro-bind /etc/passwd /etc/passwd --ro-bind /etc/group /etc/group \
 --proc /proc --dev /dev --tmpfs /run --tmpfs /home \
 --ro-bind "$repo" /work --bind "$packet" /packet \
 --bind "$packet/scratch/tmp" /tmp --chdir /work \
 --clearenv --setenv PATH /usr/bin:/bin --setenv HOME /tmp/home \
 --setenv TMPDIR /tmp --setenv LANG C.UTF-8 --setenv PYTHONDONTWRITEBYTECODE 1 \
 --setenv GIT_CONFIG_COUNT 1 --setenv GIT_CONFIG_KEY_0 safe.directory --setenv GIT_CONFIG_VALUE_0 /work \
 "$@"
