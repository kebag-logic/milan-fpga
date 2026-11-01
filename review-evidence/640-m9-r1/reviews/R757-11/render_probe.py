# Renders the status section of ieee8021q.md and prints its list structure.
# Usage: PYTHONPATH=<renderer dir> python3 render_probe.py <clone>
import os, re, sys
txt = open(os.path.join(sys.argv[1], 'docs/traceability/ieee8021q.md')).read()
sec = txt[txt.index('## STATUS 2026-08-13'):txt.index('Two consequences worth stating')]
try:
    import markdown_it
    html = markdown_it.MarkdownIt().render(sec)
except ImportError:
    import markdown
    html = markdown.markdown(sec)
print('top-level list items:', html.count('<li>'))
for it in re.findall(r'<li>(.*?)</li>', html, re.S):
    print(' item starts:', re.sub(r'<.*?>', '', it)[:50].replace('\n', ' '), '| holds MRP-1:', 'MRP-1' in it)
print('after list:', re.sub(r'<.*?>', '', html[html.rindex('</ul>'):]).strip().replace('\n', ' '))
