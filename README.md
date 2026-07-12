# QA Portfolio

A curated static portfolio site that showcases manual QA artifacts, testing strategies, and quality engineering examples built across 13+ years of experience in SaaS, enterprise software, web applications, and mobile products.

## What’s in this repository

This portfolio now includes:

- A polished landing page in [index.html](index.html) with sections for about, artifacts, skills, and contact
- Shared styling in [styles.css](styles.css)
- Artifact folders for:
  - [test-plans](test-plans/)
  - [test-cases](test-cases/)
  - [bug-reports](bug-reports/)
  - [checklists](checklists/)
  - [process-docs](process-docs/)
  - [exploratory-testing](exploratory-testing/)
- Supporting scripts and templates:
  - [convert_markdown.py](convert_markdown.py)
  - [markdown-to-html.js](markdown-to-html.js)
  - [page-template.html](page-template.html)

## Highlights

The portfolio demonstrates core QA capabilities such as:

- Risk-based test planning
- Detailed test case design
- Defect reporting with reproduction steps and impact
- Regression and release readiness checklists
- Exploratory testing notes and session-based investigation
- QA process documentation and workflow examples

## Viewing the site locally

Open the site directly in a browser from the repository root, or serve it locally with:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Updating or adding content

If you add markdown-based documents to an artifact folder, you can generate HTML pages with:

```bash
python3 convert_markdown.py
```

This will create rendered HTML files alongside the markdown source files using the shared portfolio styling.

## Notes

All artifacts in this repository are fictional recreations and anonymized examples created for portfolio purposes. No proprietary or confidential client information is included.
