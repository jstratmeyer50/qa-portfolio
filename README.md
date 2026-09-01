# 🎯 QA Portfolio

A static QA portfolio site highlighting manual testing experience, risk-based quality strategy, and real-world evidence across SaaS, web, mobile, and enterprise product workflows.

## Overview

This portfolio is designed to present a professional, recruiter-friendly view of QA work through a polished front-end and curated artifact library. It combines profile content, skills overview, and sample case files that demonstrate practical quality engineering thinking.

## Current site structure

- [index.html](index.html) — landing page with hero section, experience summary, and key entry points
- [about.html](about.html) — background, QA philosophy, and professional overview
- [case-files.html](case-files.html) — archive landing page for test plans, test cases, bug reports, and other artifacts
- [skills.html](skills.html) — testing and automation skill set overview
- [contact.html](contact.html) — contact details and outreach information
- [styles.css](styles.css) — shared visual system and responsive layout styling

## Artifact folders

- [test-plans](test-plans/) — risk-based planning, strategy, and release criteria
- [test-cases](test-cases/) — structured scenario-based validation for web and mobile flows
- [bug-reports](bug-reports/) — defect examples with severity, steps, and impact analysis
- [checklists](checklists/) — regression and release readiness checklists
- [process-docs](process-docs/) — QA workflow documentation and operating procedures
- [exploratory-testing](exploratory-testing/) — exploratory session notes and investigation examples

## Recent updates

The portfolio has recently been expanded and refined to better reflect a more complete QA brand presence:

- Updated landing page with clearer positioning and a stronger value proposition
- Added dedicated About, Skills, and Contact pages for a fuller portfolio experience
- Reworked the Case Files archive so each artifact category has a clearer entry point
- Expanded the QA content library with additional test plans, test cases, and workflow examples
- Improved styling and navigation for readability, responsiveness, and a more professional presentation
- Added a consistent structure across portfolio pages and artifact sections

## Local preview

To view the site locally, run:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in a browser.

## Content workflow

The site is built as a static HTML portfolio. For markdown-based additions, use the conversion utility:

```bash
python3 convert_markdown.py
```

This generates HTML output from markdown source while preserving the shared portfolio styling.

## Notes

All sample artifacts in this repository are fictional or anonymized portfolio examples created for demonstration purposes.

---

Built for quality engineering excellence.
