[A325] Submodule diagram inspection

Generated `submodule_boundaries.drawio`, `.svg`, `.png`, and the corresponding PNG manifest row with the repository generator. Confirmed processor label `0922e43408f8`, unchanged other pins, visible connectors, and readable text without overlap.

Inspected the committed PNG, a direct Draw.io PNG export, and an A4 landscape print raster. Inspection renders are under `/tmp/567-a325-diagram`; they are not project build artifacts and are not committed.

Commands used:

```sh
python3 docs/diagrams/submodule_boundaries.gen.py
xvfb-run -a drawio --disable-gpu --export --format png --crop --scale 2 --output /tmp/567-a325-diagram/direct.png docs/diagrams/submodule_boundaries.drawio
xvfb-run -a drawio --disable-gpu --export --format pdf --crop --output /tmp/567-a325-diagram/native.pdf docs/diagrams/submodule_boundaries.drawio
pdftocairo -svg /tmp/567-a325-diagram/native.pdf /tmp/567-a325-diagram/native.svg
rsvg-convert -f pdf --page-width 297mm --page-height 210mm -w 277mm -h 160.73mm --left 10mm --top 24.635mm -a /tmp/567-a325-diagram/native.svg -o /tmp/567-a325-diagram/a4.pdf
pdftoppm -png -r 150 -singlefile /tmp/567-a325-diagram/a4.pdf /tmp/567-a325-diagram/a4
```

All commands returned 0. Direct export emitted graphics-acceleration diagnostics but produced complete, readable artifacts.
