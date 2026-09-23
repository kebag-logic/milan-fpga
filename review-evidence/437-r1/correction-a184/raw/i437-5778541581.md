[A172] ADDITIONAL OBSERVATION / ACCEPTANCE REMAINS OPEN

The requested outside-tag/comment boundary sweep found an additional rendered-output limitation. Exact synthetic page:

```text
- item

  text
<span>
<!--

## Old
</span>

## Real
```

Fresh GitHub gfm response is `<ul dir="auto">\n<li>\n<p dir="auto">item</p>\n<p dir="auto">text</p>\n</li>\n</ul>\n<span>\n</span>` (no heading elements). The original 88e9276b walk lists no headings; both starting 65df1df5 and the correction walk list Old and Real. The first-paragraph counterpart lists Old/Real at all three revisions. Twelve variants (first/resumed, tag column 0/1, opening/closing/attribute) reproduce the rendered-output mismatch; six resumed variants differ from the original base, and none changes under this correction.

This is an unclosed comment inside an already-open raw HTML block, outside the named live-paragraph/tag and dedented-container corrections. Fixing nested HTML/comment handling would require a further parser behavior decision; no such scope or acceptance change is taken privately. The exact requests/responses and three-revision comparison remain in the correction packet; these are recorded mismatches, not passing regression controls. Separate closed-comment outside-tag controls and the named live-item comment counterexamples agree with rendering. The docstring and CONTRIBUTING state this tested limit rather than implying all escape directions closed.

Manager decision/follow-up remains required for this additional observation. The concrete requested correction continues; AC1 and overall completion are not claimed. R237/R238 finding identities, severities and lenses are unchanged.

Historical wording clarification: nine descriptions and eleven row IDs do not prove two further distinct shapes. The remaining row identities could be duplicates or additional variants; neither interpretation is assumed.
