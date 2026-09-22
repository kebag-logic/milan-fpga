"""Real-Git replay histories from the public #423 R242 matrix.

The 31 expectations are the settled decision's outcomes, including its
conservative refusals and the unchanged linear historical policy. Builders
adapt the published factual fixtures; they do not implement the predicate.
Run through check_merge_containment.py --selftest (the existing owner).
"""

import os
import subprocess
from pathlib import Path

from merge_containment_selftest_scratch import scratch
from merge_containment_selftest_mutations import mutation_cases

MOD = "".join(f"line {i:02d}\n" for i in range(1, 41))

ADDED = ('def stage(work, tag, mutate=None):\n    """Stage one suite."""\n'
         '    return work / tag\n\n\n'
         'def build(suite):\n    """Build one suite."""\n    return suite\n\n\n'
         'def main():\n    return 0\n')


class _History:
    """Deterministic fixture Git with checked commands and isolated config."""

    def __init__(self):
        self.tick = 1790000000

    def _git(self, *args):
        self.tick += 60
        env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                   GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                   GIT_AUTHOR_DATE=f"@{self.tick} +0000", GIT_COMMITTER_DATE=f"@{self.tick} +0000",
                   LC_ALL="C")
        result = subprocess.run(("git", "-c", "commit.gpgsign=false", "-c",
                                 "core.autocrlf=false", *args), env=env,
                                capture_output=True, text=True, errors="surrogateescape")
        if result.returncode != 0:
            raise RuntimeError(f"fixture git {args}: {result.stderr}")
        return result.stdout.strip()

    def _write(self, path, text, mode=None):
        dest = Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(text if isinstance(text, bytes) else text.encode())
        if mode is not None:
            dest.chmod(mode)

    def _read(self, path):
        return Path(path).read_text()

    def _commit(self, message):
        self._git("add", "-A")
        self._git("commit", "-q", "-m", message)
        return self._git("rev-parse", "HEAD")

    def _replace_line(self, path, old, new):
        text = self._read(path)
        if old not in text:
            raise RuntimeError(f"fixture missing text in {path}")
        self._write(path, text.replace(old, new, 1))

    def _seed(self):
        """O, the PR61-like incoming commit A, redundant merge M, PR62-like C."""
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        self._write('added.py', ADDED)
        a = self._commit('A original (PR61-like)')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '-m', 'M redundant merge of incoming', 'incoming')
        m = self._git('rev-parse', 'HEAD')
        self._replace_line('added.py', '    return work / tag\n', '    return work / f"suite_{tag}"\n')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C original (PR62-like)')
        return dict(O=o, A=a, M=m, C=c)

    def _replay(self, ids, with_c=True, c_mutator=None):
        """Target history: A', redundant M', C' on a side branch, merge M2'."""
        self._git('checkout', '-q', 'main')
        self._git('checkout', '-q', '-b', 'replay-a', ids['O'])
        self._git('cherry-pick', ids['A'])
        self._git('commit', '-q', '--amend', '-m', "A' replay")
        self._git('checkout', '-q', 'main')
        self._git('merge', '-q', '--no-ff', '-m', "M' replayed redundant merge", 'replay-a')
        if not with_c:
            return
        self._git('checkout', '-q', '-b', 'replay-c', 'main')
        if c_mutator is None:
            self._git('cherry-pick', ids['C'])
            self._git('commit', '-q', '--amend', '-m', "C' replay")
        else:
            c_mutator()
            self._commit("C' altered replay")
        self._git('checkout', '-q', 'main')
        self._git('merge', '-q', '--no-ff', '-m', "M2' replayed PR merge", 'replay-c')

    def _later(self, msg, fn):
        self._git('checkout', '-q', 'main')
        fn()
        return self._commit(msg)

    def _far_extension(self):
        self._replace_line('mod.txt', 'line 35\n', 'line 35 later extension\n')

    def _s_positive(self):
        ids = self._seed()
        self._replay(ids)
        self._later('L far extension of a touched file', self._far_extension)

    def _s_positive_two_later(self):
        ids = self._seed()
        self._replay(ids)
        self._later('L far extension', self._far_extension)
        self._later('L2 unrelated new file', lambda: self._write('new.txt', 'new\n'))

    def _s_pr62_faithful(self):
        ids = self._seed()
        self._replay(ids)

        def rewrite() -> None:
            """Change the branch-added signature after its exact replay."""
            self._replace_line('added.py',
                               'def stage(work, tag, mutate=None):\n',
                               'def stage(work: Path, tag: str, mutate=None) -> Path:\n')
            self._far_extension()
        self._later('L annotate a PR-introduced line (0ac3e2c-like) + far edit', rewrite)

    def _s_adjacent_extension(self):
        ids = self._seed()
        self._replay(ids)
        self._later('L extension adjacent to the replayed hunk',
                    lambda: self._replace_line('mod.txt', 'line 05 changed by A\n',
                                               'line 05 changed by A\nline 05b later extension\n'))

    def _s_no_later(self):
        ids = self._seed()
        self._replay(ids)

    def __revert_c(self):
        self._git('checkout', '-q', 'main')
        self._git('revert', '--no-edit', 'main^2')

    def _s_revert_all(self):
        ids = self._seed()
        self._replay(ids)
        self.__revert_c()
        self._git('revert', '--no-edit', self._git('rev-parse', 'main~2^2'))

    def _s_revert_c(self):
        ids = self._seed()
        self._replay(ids)
        self.__revert_c()

    def _s_revert_partial_hunk(self):
        ids = self._seed()
        self._replay(ids)
        self._later('L restore only the A hunk of mod.txt',
                    lambda: self._replace_line('mod.txt', 'line 05 changed by A\n', 'line 05\n'))

    def _s_revert_plus_extension(self):
        ids = self._seed()
        self._replay(ids)
        self.__revert_c()
        self._later('L far extension after revert', self._far_extension)

    def _s_revert_then_reapply(self):
        ids = self._seed()
        self._replay(ids)
        self.__revert_c()
        self._git('revert', '--no-edit', 'HEAD')

    def _s_omit_linear(self):
        ids = self._seed()
        self._replay(ids, with_c=False)
        self._later('L far extension', self._far_extension)

    def _s_omit_partial(self):
        ids = self._seed()

        def only_added() -> None:
            """Replay only the added-file part of C."""
            self._replace_line('added.py', '    return work / tag\n', '    return work / f"suite_{tag}"\n')
        self._replay(ids, c_mutator=only_added)
        self._later('L far extension', self._far_extension)

    def _s_whitespace(self):
        ids = self._seed()

        def spaced() -> None:
            """Replay C with deliberately different whitespace."""
            self._replace_line('added.py', '    return work / tag\n', '    return work /  f"suite_{tag}"\n')
            self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        self._replay(ids, c_mutator=spaced)
        self._later('L far extension', self._far_extension)

    def __seed_resolution(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        self._write('added.py', ADDED)
        a = self._commit('A original')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '--no-commit', 'incoming')
        self._write('resolution.txt', 'resolution work only in the merge\n')
        self._git('add', '-A')
        self._git('commit', '-q', '-m', 'M merge WITH resolution work')
        m = self._git('rev-parse', 'HEAD')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C original')
        return dict(O=o, A=a, M=m, C=c)

    def _s_resolution_missing(self):
        ids = self.__seed_resolution()
        self._replay(ids)
        self._later('L far extension', self._far_extension)

    def _s_resolution_present(self):
        ids = self.__seed_resolution()
        self._replay(ids)
        self._later('L resolution content landed separately',
                    lambda: self._write('resolution.txt', 'resolution work only in the merge\n'))
        self._later('L far extension', self._far_extension)

    def _s_octopus(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'in1')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        a = self._commit('A')
        self._git('checkout', '-q', '-b', 'in2', o)
        self._write('added.py', ADDED)
        a2 = self._commit('A2')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '-m', 'octopus', 'in1', 'in2')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        for x in (a, a2, c):
            self._git('cherry-pick', x)
        self._later('L far extension', self._far_extension)

    def _s_octopus_absorbed(self):
        """Octopus whose tree equals its second parent: only the count refuses."""
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        self._write('keep.txt', 'keep A\n')
        a = self._commit('A')
        self._git('checkout', '-q', '-b', 'side', o)
        self._write('keep.txt', 'keep A\n')
        x = self._commit('X (its change is also inside A)')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '-m', 'octopus absorbing X', 'incoming', 'side')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', '-b', 'replay-x', o)
        self._git('cherry-pick', x)
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        self._git('merge', '-q', '--no-ff', '-m', 'merge X replay', 'replay-x')
        self._git('cherry-pick', c)
        self._later('L far extension', self._far_extension)

    def _s_disabling_rewrite(self):
        ids = self._seed()
        self._replay(ids)
        self._later('L rewrite a PR-introduced line to disable it',
                    lambda: self._replace_line('added.py',
                                               'def main():\n    return 0\n',
                                               "def main():\n    raise SystemExit('disabled')\n"))

    def _s_unrelated_parent(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '--orphan', 'unrelated')
        self._git('rm', '-q', '-rf', '.')
        self._write('u.txt', 'unrelated history\n')
        u = self._commit('U unrelated root')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '--allow-unrelated-histories', '-m', 'merge unrelated root', 'unrelated')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        self._write('u.txt', 'unrelated history\n')
        self._commit('u.txt landed linearly')
        self._git('cherry-pick', c)
        self._later('L far extension', self._far_extension)

    def __seed_multi(self, redundant_second=True):
        ids = self._seed()
        self._git('checkout', '-q', '-b', 'side2', ids['C'])
        self._replace_line('mod.txt', 'line 30\n', 'line 30 changed by D\n')
        d = self._commit('D')
        self._git('checkout', '-q', 'pr')
        if not redundant_second:
            self._git('checkout', '-q', '-b', 'side3', ids['M'])
            self._write('x.txt', 'x\n')
            self._commit('X diverging from M')
            self._git('checkout', '-q', 'pr')
            self._git('merge', '-q', '--no-ff', '-m', 'M2 non-redundant', 'side3')
        else:
            self._git('merge', '-q', '--no-ff', '-m', 'M2 second redundant merge', 'side2')
        self._replace_line('added.py', 'def main():\n    return 0\n', 'def main():\n    return 1\n')
        e = self._commit('E')
        return (ids, d, e)

    def _s_multi_redundant(self):
        ids, d, e = self.__seed_multi()
        self._replay(ids)
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', d)
        self._git('cherry-pick', e)
        self._later('L far extension', self._far_extension)

    def _s_mixed_merges(self):
        ids, d, e = self.__seed_multi(redundant_second=False)
        self._replay(ids)
        self._git('checkout', '-q', 'main')
        self._write('x.txt', 'x\n')
        self._commit('X landed')
        self._git('cherry-pick', e)
        self._later('L far extension', self._far_extension)

    def _s_distance_two(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A1\n')
        a1 = self._commit('A1')
        self._write('added.py', ADDED)
        a2 = self._commit('A2')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '-m', 'M of a two-commit branch', 'incoming')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        for x in (a1, a2, c):
            self._git('cherry-pick', x)
        self._later('L far extension', self._far_extension)

    def _s_evil_byte(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        a = self._commit('A')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '--no-commit', 'incoming')
        self._replace_line('mod.txt', 'line 10\n', 'line 10 \n')
        self._git('add', '-A')
        self._git('commit', '-q', '-m', 'M with a one-byte evil change')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        self._git('cherry-pick', c)
        self._later('L far extension', self._far_extension)

    def _s_reversed_parents(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._replace_line('mod.txt', 'line 03\n', 'line 03 base\n')
        o2 = self._commit('O2')
        self._git('checkout', '-q', '-b', 'incoming')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        a = self._commit('A')
        tree = self._git('rev-parse', a + '^{tree}')
        m = self._git('commit-tree', tree, '-p', a, '-p', o2, '-m', 'M: incoming first, its parent second')
        self._git('checkout', '-q', '-b', 'pr', m)
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        self._git('cherry-pick', c)
        self._later('L far extension', self._far_extension)

    def _s_linear_revert_control(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'pr')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        a = self._commit('A')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        self._git('cherry-pick', c)
        self._git('revert', '--no-edit', 'HEAD')
        self._git('revert', '--no-edit', 'HEAD~2')

    def _s_linear_extension_control(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'pr')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        a = self._commit('A')
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        self._later('L adjacent extension',
                    lambda: self._replace_line('mod.txt', 'line 05 changed by A\n', 'line 05 changed by A\nline 05b\n'))

    def _s_mode_loss(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._write('tool.sh', '#!/bin/sh\necho tool\n', 493)
        a = self._commit('A adds an executable')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '-m', 'M redundant', 'incoming')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        self._git('cherry-pick', c)
        self._later('L drops the executable bit', lambda: os.chmod('tool.sh', 420))

    def _s_binary_later_edit(self):
        self._git('init', '-q', '-b', 'main')
        self._write('mod.txt', MOD)
        self._write('keep.txt', 'keep\n')
        self._write('data.bin', b'\x00\x01head\x00' + b'\x00' * 64 + b'tail\x00\n')
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._write('data.bin', b'\x00\x01HEAD\x00' + b'\x00' * 64 + b'tail\x00\n')
        a = self._commit('A edits a binary')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '-m', 'M redundant', 'incoming')
        self._replace_line('mod.txt', 'line 20\n', 'line 20 changed by C\n')
        c = self._commit('C')
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        self._git('cherry-pick', c)
        self._later('L edits the binary elsewhere',
                    lambda: self._write('data.bin', b'\x00\x01HEAD\x00' + b'\x00' * 64 + b'TAIL\x00\n'))

    def _s_delete_later(self):
        ids = self._seed()
        self._replay(ids)
        self._later('L deletes a touched file', lambda: os.remove('mod.txt'))

    def _s_hostile_config(self):
        ids = self._seed()
        self._replay(ids)
        self.__revert_c()
        self._git('revert', '--no-edit', self._git('rev-parse', 'main~2^2'))
        self._later("L attributes asking for an 'ours' merge driver",
                    lambda: self._write('.gitattributes', '* merge=ours diff=quiet\n'))
        self._git('config', 'merge.ours.driver', 'true')
        self._git('config', 'merge.ours.name', 'always keep ours')
        self._git('config', 'diff.quiet.textconv', 'true')

    def _s_repeated_block(self):
        self._git('init', '-q', '-b', 'main')
        block = 'a\nb\nc\nold\nd\ne\nf\n'
        sep = ''.join((f'separator-{i}\n' for i in range(10)))
        self._write('rep.txt', block + sep + block)
        self._write('mod.txt', MOD)
        o = self._commit('O base')
        self._git('checkout', '-q', '-b', 'incoming')
        self._replace_line('mod.txt', 'line 05\n', 'line 05 changed by A\n')
        a = self._commit('A')
        self._git('checkout', '-q', '-b', 'pr', o)
        self._git('merge', '-q', '--no-ff', '-m', 'M redundant', 'incoming')
        self._write('rep.txt', (block + sep + block).replace('old', 'new', 1))
        c = self._commit('C edits the FIRST block')
        self._git('checkout', '-q', 'main')
        self._git('cherry-pick', a)
        before, after = self._read('rep.txt').rsplit('old', 1)
        self._write('rep.txt', before + 'new' + after)
        self._commit("C' edits the SECOND block (same verbatim patch-id)")
        self._later('L far extension', self._far_extension)


SCENARIOS = (
    ('positive-replay-far-extension', "_s_positive",
     (0, 'contained')),
    ('positive-replay-two-later-commits', "_s_positive_two_later",
     (0, 'contained')),
    ('two-redundant-merges', "_s_multi_redundant",
     (1, 'STRANDED')),
    ('control-replay-no-later-edit', "_s_no_later",
     (0, 'contained')),
    ('control-revert-then-reapply', "_s_revert_then_reapply",
     (0, 'contained')),
    ('pr62-faithful-later-rewrite', "_s_pr62_faithful",
     (1, 'UNKNOWN')),
    ('later-disabling-rewrite', "_s_disabling_rewrite",
     (1, 'UNKNOWN')),
    ('published-shape-adjacent-extension', "_s_adjacent_extension",
     (1, 'UNKNOWN')),
    ('later-deletion-of-touched-file', "_s_delete_later",
     (1, 'UNKNOWN')),
    ('later-exec-bit-loss', "_s_mode_loss",
     (1, 'UNKNOWN')),
    ('later-binary-edit', "_s_binary_later_edit",
     (1, 'UNKNOWN')),
    ('exact-revert-whole-replay', "_s_revert_all",
     (1, 'UNKNOWN')),
    ('exact-revert-pr-commit', "_s_revert_c",
     (1, 'UNKNOWN')),
    ('partial-revert-one-hunk', "_s_revert_partial_hunk",
     (1, 'UNKNOWN')),
    ('revert-plus-far-extension', "_s_revert_plus_extension",
     (1, 'UNKNOWN')),
    ('revert-under-hostile-merge-config', "_s_hostile_config",
     (1, 'UNKNOWN')),
    ('omitted-linear-commit', "_s_omit_linear",
     (1, 'STRANDED')),
    ('omitted-part-of-a-commit', "_s_omit_partial",
     (1, 'STRANDED')),
    ('whitespace-different-postimage', "_s_whitespace",
     (1, 'STRANDED')),
    ('repeated-block-other-location', "_s_repeated_block",
     (1, 'STRANDED')),
    ('merge-resolution-work-missing', "_s_resolution_missing",
     (1, 'STRANDED')),
    ('merge-resolution-work-present', "_s_resolution_present",
     (1, 'STRANDED')),
    ('merge-one-byte-evil-change', "_s_evil_byte",
     (1, 'STRANDED')),
    ('octopus-merge', "_s_octopus",
     (1, 'STRANDED')),
    ('octopus-absorbed-third-parent', "_s_octopus_absorbed",
     (1, 'STRANDED')),
    ('unrelated-parent-merge', "_s_unrelated_parent",
     (1, 'STRANDED')),
    ('redundant-plus-nonredundant-merge', "_s_mixed_merges",
     (1, 'STRANDED')),
    ('first-parent-is-grandparent', "_s_distance_two",
     (1, 'STRANDED')),
    ('reversed-parent-order', "_s_reversed_parents",
     (1, 'STRANDED')),
    ('linear-control-exact-revert', "_s_linear_revert_control",
     (0, 'contained')),
    ('linear-control-adjacent-extension', "_s_linear_extension_control",
     (0, 'contained')),
)


def replay_cases(fx: object) -> None:
    """Execute the public matrix through the production CLI and aggregator."""
    for index, (name, builder, expected) in enumerate(SCENARIOS, 1):
        with scratch(fx.leftovers) as directory:
            cwd = os.getcwd()
            try:
                os.chdir(directory)
                history = _History()
                getattr(history, builder)()
                rc, output = fx.run(["--no-fetch", "--base", "main", "pr"])
                lines = [line.split() for line in output.splitlines() if line.strip()]
                actual = (rc, lines[0][0] if lines else "no verdict")
                fx.case(f"replay-{index:02d}-{name}", actual, expected,
                        "settled public matrix: exit AND verdict")
                if index in (1, 2):
                    fx.case(f"replay-{index:02d}-proof", "raw no-op retention" in output,
                            True, "the new arm proves retention after real historical replay")
                if expected[1] == "UNKNOWN":
                    fx.case(f"replay-{index:02d}-evidence",
                            "historical whitespace-exact replay" in output
                            and "current retention unproved on:" in output,
                            True, "historical landing is distinguished from unproved paths")
                mutation_cases(fx, index)
            finally:
                os.chdir(cwd)
