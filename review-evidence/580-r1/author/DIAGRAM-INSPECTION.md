# Boundary diagram inspection

The repository generator regenerated the SVG, editable master, PNG and manifest.
The decoded committed PNG, direct master export and simulated A4 landscape print
were inspected. All labels, pin text and connectors remain visible and legible;
no clipping was observed. The current protocol pin reads `16be6768f710`.
Inspection artifacts remain under `/tmp/580-a366-diagram`, outside this output.

Commands, all rc 0:

```sh
python3 docs/diagrams/submodule_boundaries.gen.py
xvfb-run -a drawio --disable-gpu --no-sandbox --export --format png --crop --scale 2 --output /tmp/580-a366-diagram/direct.png docs/diagrams/submodule_boundaries.drawio
xvfb-run -a drawio --disable-gpu --no-sandbox --export --format pdf --crop --output /tmp/580-a366-diagram/native.pdf docs/diagrams/submodule_boundaries.drawio
pdftocairo -svg /tmp/580-a366-diagram/native.pdf /tmp/580-a366-diagram/native.svg
rsvg-convert -f pdf --page-width 297mm --page-height 210mm -w 277mm -h 160.73mm --left 10mm --top 24.635mm -a /tmp/580-a366-diagram/native.svg -o /tmp/580-a366-diagram/a4.pdf
pdftoppm -png -r 150 -singlefile /tmp/580-a366-diagram/a4.pdf /tmp/580-a366-diagram/a4
```

| Artifact | Bytes | SHA256 |
|---|---:|---|
| `a4.pdf` | 445910 | `d9b4a7ca010a6e2e4a4ebb20a324b0a5b2bc344767ccdbdfb2d8f1e363158a36` |
| `a4.png` | 151383 | `66fb6537aae817fda7648c4bbe48e777b6b4826b2d2c450a5f16176b0427a2ae` |
| `direct.png` | 446885 | `b3daf8b792ab0f2252d109fe2d0a871d2fea4ad8151394e5772e2c35d38070ff` |
| `native.pdf` | 31521 | `8e7253aee37b290047cd9840ca99324874dca15d813adc04f7a974c8ba2bfa58` |
| `native.svg` | 432209 | `563f7450b65daa7ac608e4d70505e02fc087f8accfe1ceec9d729128e182020e` |
