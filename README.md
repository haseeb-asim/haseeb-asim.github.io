# Haseeb Asim

Personal site for [haseeb-asim.github.io](https://haseeb-asim.github.io/). Static HTML, CSS, and one small script. GitHub Pages serves the files from the root of `main`. There is no build step. `.nojekyll` is in the root so Jekyll does not process the site.

## Pages

- `/` is an index: one sentence, four shipped projects, the full shipped list, and contact.
- `/work/<slug>/` is a case study. Client work with no public URL is marked Private.
- `/concepts/` is a wall of self-initiated concept designs. Each study is at `/concepts/<slug>/`. The screens use fictional sample data and are not client work.
- `/about/` has background, education, how he works, services, and skills.
- `404.html` is the missing page.

## Edit the copy

The HTML is generated so the nav and footer stay the same. Edit `tools/render_site.py`, then run:

```bash
python3 tools/render_site.py
```

The committed HTML is what GitHub Pages serves.

Do not add projects, clients, metrics, or testimonials that are not already in the source notes.

## Motion

`/js/site.js` is the only script. It sets the Central Time clock, the theme toggle, and the thumbnail-to-case-study view transition. The transition is skipped for keyboard activation and for `prefers-reduced-motion`. The concept stack and the tilted concept wall are CSS.
