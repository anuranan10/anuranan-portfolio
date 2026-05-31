# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static personal portfolio website for Anuranan Bharadwaj, hosted at [anuranan.info](https://anuranan.info). Pure HTML5 + CSS3, no JavaScript, no build tooling, no frameworks. Changes are visible immediately by opening the HTML files in a browser.

## Architecture

Single shared stylesheet (`style.css`) consumed by all pages. No preprocessing, no bundling. Navigation links and the footer block are duplicated across every HTML file — changes to nav or footer must be applied to each page manually.

### Page structure

| File | Purpose |
|---|---|
| `index.html` | Homepage with profile photo and bio |
| `aerospace.html` | AE project cards linking to detail pages |
| `cs.html` | CS project cards |
| `experience.html` | Work/research/leadership experience |
| `lab-testing-experience.html` | ERAU lab experimentation (in progress) |
| `resume.html` | Resume download cards |
| `contact.html` | Contact info and social links |
| `*.html` (root, long names) | Individual AE project detail pages |

### Assets

- `Folder/` — profile photo and AE project images (wing, tunnel, MATLAB, stability)
- `CS/` — CS project screenshots
- `AnurananBharadwaj_RESUME_AE.pdf` / `AnurananBharadwaj_RESUME_SE.pdf` — linked from `resume.html` and section footers

## CSS layout conventions

- `.project-row` — flex card used on both `aerospace.html` and `cs.html`; text on left, image on right
- `.project-image-group` — 3-image row (or note placeholders) used for most AE projects
- `.project-image-group2` — wider 3-image row with fixed height, used for wind tunnel / MATLAB projects
- `.project-image-cs` — single image variant used on CS project cards
- `.exp-card` — experience/lab entry card
- Color palette: `#004080` (navy, primary), `#1f1f1f` (nav/footer dark), `#f4faff` (card background), `#f0a30a` (download button yellow)
- Responsive breakpoint at `max-width: 768px` in `style.css`

## Deployment

Deployed via GitHub Pages with the custom domain in `CNAME` (`anuranan.info`). Push to `main` to deploy — no CI, no build step.

## Working with Technical Reports (PDFs)

When instructed, read a PDF technical report at the path provided in the prompt. Use it to generate a new page or populate content in an existing page. Follow these rules strictly:

- Match the HTML structure of the closest existing detail page (typically one of the AE project pages). Use the same nav, footer, section layout, and CSS classes.
- Writing style is professional and portfolio-appropriate. Concise, first-person where relevant, technically accurate. No filler language. No casual tone.
- Do not dump raw report text. Synthesize and rewrite content as if Anuranan is presenting his own work. Maintain technical accuracy but write it as a portfolio narrative, not a lab report transcript.
- If the report contains figures or data tables worth referencing, note their placement in comments (`<!-- insert figure: X here -->`) so assets can be added manually later.
- Ask for clarification on which sections of the report to prioritize if the prompt is ambiguous.

## Reference Portfolio (Nick's Portfolio)

Nick's portfolio at https://nicholas-speredelozzi.github.io/ is approved as a reference for layout ideas, section structure, and design inspiration.

Rules for using it:

- Use it for structural and layout inspiration only. Do not copy HTML, CSS, copy, or visual design verbatim.
- When referencing it, adapt ideas to fit the existing color palette, typography, and CSS conventions of this project.
- The final output must be distinctly Anuranan's portfolio. If a suggestion would make it look like a clone, push back and propose an adapted version instead.
- Refer to it as "Nick's portfolio" in all communications.