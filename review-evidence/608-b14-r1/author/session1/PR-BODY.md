[A578] B14 bench lane on dev 5603c353: STOP at the identity gate

Refs #608 #645 #647 #667 #682 #686 #691

No pull request is proposed from this session. The lane stopped at item 1: the controller host did not return after the bench VMs restarted, so the DUT could not be read over ATDECC and the identity gate could not run. Every later item needs the controller, so none ran.

- Branch `608-b14-bench` is unchanged at dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`, with no commit.
- No findings page was written, because no item produced a measurement.
- No bench state changed and there is nothing to restore.
- The tap host, both consoles, both audio cards and the board link address were present.

The whole lane, from item 1, reruns on the same image once the controller host answers.
