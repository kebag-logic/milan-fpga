import sys
p = sys.argv[1]
L = open(p).read().split('\n')
out = []
i = 0
hunk = 0
while i < len(L):
    if L[i].startswith('<<<<<<< '):
        j = L.index('=======', i)
        k = next(n for n in range(j, len(L)) if L[n].startswith('>>>>>>> '))
        ours, theirs = L[i+1:j], L[j+1:k]
        hunk += 1
        if hunk == 1:
            assert ours[1].strip() == 'dynmap_map_records_section();', ours[:2]
            assert [t.strip() for t in theirs] == ['stopped_input_law_on_the_shipping_geometry();']
            out += ['        //! #762 next, on its own fresh boot as on the #762 leg; the',
                    '        //! [MAPREC] then boots over an erased window, so neither case',
                    '        //! reads the other\'s state',
                    theirs[0]] + ours
        elif hunk == 2:
            assert ours[0].strip() == '#endif', ours[0]
            assert theirs[-1].strip() == 'prove_a_stopped_stream_input_counts_no_interruption();'
            out += theirs + ['    }', ''] + ours
        else:
            raise SystemExit('unexpected hunk')
        i = k + 1
    else:
        out.append(L[i]); i += 1
assert hunk == 2
open(p, 'w').write('\n'.join(out))
