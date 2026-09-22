[A172] NINE DESCRIBED HISTORICAL RECONSTRUCTIONS - AC1 STILL UNPROVEN

At local correction head b5e6c23e1b9802b5cacbc62db212064d7e429862, these nine synthetic reconstructions preserve the nine distinctions expressly described in [R86-5](https://github.com/kebag-logic/milan-fpga/pull/428#issuecomment-5644834363). They are newly constructed bytes, not recovered originals, and `historical_id: null` is intentional. The report collectively names H01/H02/H05/H06/H10/H13/H25/H28/H29/H31/G02; no unsupported per-ID mapping is assigned. R85-4 adds no retrievable correspondence. Two remaining row identities may be duplicates or further variants; this evidence does not settle that question. R237 F2 remains open under its original MAJOR severity and Conformance/Tests/Docs lenses.

Each request is synthetic-only `POST /markdown` in gfm mode with the repository context. The exact fresh requests/responses and corrected heading lists are below. Each real-Git fixture has an actual synthetic base/head commit pair; its head navigation has generator provenance. Each described family-one base page lacks Old, the generated base navigation omits it, and the copied head label is specifically refused with zero exemptions. These nine successes are not an eleven-case completeness claim.

<details><summary>Exact requests, responses and real-Git/navigation receipts</summary>

```json
[
  {
    "description_name": "two spaces",
    "historical_id": null,
    "request": {
      "text": "- item\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.144837+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n- item\n\n  text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page0.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n- item\\n\\n  text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "three spaces",
    "historical_id": null,
    "request": {
      "text": "- item\n\n   text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.145293+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n- item\n\n   text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page1.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n- item\\n\\n   text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "star item",
    "historical_id": null,
    "request": {
      "text": "* item\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.145852+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n* item\n\n  text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page2.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n* item\\n\\n  text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "ordered item",
    "historical_id": null,
    "request": {
      "text": "1. item\n\n   text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ol dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ol>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.146676+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n1. item\n\n   text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page3.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n1. item\\n\\n   text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ol dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ol>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "two paragraphs",
    "historical_id": null,
    "request": {
      "text": "- item\n\n  first\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">first</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.622796+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n- item\n\n  first\n\n  text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page4.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n- item\\n\\n  first\\n\\n  text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">first</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "task item",
    "historical_id": null,
    "request": {
      "text": "- [ ] item\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ul class=\"contains-task-list\">\n<li class=\"task-list-item\">\n<p dir=\"auto\"><input type=\"checkbox\" id=\"\" disabled=\"\" class=\"task-list-item-checkbox\" aria-label=\"Incomplete task\"> item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.675331+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n- [ ] item\n\n  text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page5.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n- [ ] item\\n\\n  text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ul class=\"contains-task-list\">\n<li class=\"task-list-item\">\n<p dir=\"auto\"><input type=\"checkbox\" id=\"\" disabled=\"\" class=\"task-list-item-checkbox\" aria-label=\"Incomplete task\"> item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "interrupting item",
    "historical_id": null,
    "request": {
      "text": "text\n- item\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<p dir=\"auto\">text</p>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.762934+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\ntext\n- item\n\n  text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page6.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\ntext\\n- item\\n\\n  text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<p dir=\"auto\">text</p>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "bold tag",
    "historical_id": null,
    "request": {
      "text": "- item\n\n  text\n<b>\n## Old\n</b>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<b>\n## Old\n</b>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:28.769305+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n- item\n\n  text\n<b>\n## Old \u2014 heading\n</b>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page7.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n- item\\n\\n  text\\n<b>\\n## Old \\u2014 heading\\n</b>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<b>\n## Old \u2014 heading\n</b>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  },
  {
    "description_name": "two blank lines",
    "historical_id": null,
    "request": {
      "text": "- item\n\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
      "mode": "gfm",
      "context": "kebag-logic/milan-fpga"
    },
    "response_html": "<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old\n</span>\n<h2 dir=\"auto\">Real</h2>",
    "utc": "2026-09-22T14:32:29.205967+00:00",
    "exit": 0,
    "github_headings": [
      "Real"
    ],
    "corrected_headings": [
      "Real"
    ],
    "real_git": {
      "base_page": "# Page\n\n- item\n\n\n  text\n<span>\n## Old \u2014 heading\n</span>\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "head_page": "# Page\n\n## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n- **[Gamma](#gamma)** -- What gamma holds.\n\n## Old \u2014 heading\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n",
      "base_commit": "bdabcdda34a06203b55525ac9db9921048202d7e",
      "head_commit": "1af2f48b0b950302a8972191f95cc8b86866642c",
      "navigation_lists_old": false,
      "findings": [
        "page8.md:5: U+2014 (em dash) in a Contents label that mirrors no heading the base version of this page had -- reword the new heading, then regenerate the block"
      ],
      "exempt": 0,
      "renderer_request_bytes": "{\"text\": \"# Page\\n\\n- item\\n\\n\\n  text\\n<span>\\n## Old \\u2014 heading\\n</span>\\n\\n## Alpha\\n\\nBody.\\n\\n## Beta\\n\\nBody.\\n\\n## Gamma\\n\\nBody.\\n\", \"mode\": \"gfm\", \"context\": \"kebag-logic/milan-fpga\"}",
      "renderer_response_html": "<h1 dir=\"auto\">Page</h1>\n<ul dir=\"auto\">\n<li>\n<p dir=\"auto\">item</p>\n<p dir=\"auto\">text</p>\n</li>\n</ul>\n<span>\n## Old \u2014 heading\n</span>\n<h2 dir=\"auto\">Alpha</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Beta</h2>\n<p dir=\"auto\">Body.</p>\n<h2 dir=\"auto\">Gamma</h2>\n<p dir=\"auto\">Body.</p>"
    }
  }
]
```
</details>
