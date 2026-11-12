# Haseeb Asim

Personal site for [haseeb-asim.github.io](https://haseeb-asim.github.io/). It is a single static page: HTML, CSS, and a small script. There is no build step. GitHub Pages serves the files from the root of `main`.

`.nojekyll` is in the root so Jekyll does not process the site.

## What’s on the page

- Hero, with email and GitHub
- Services he offers (AI agents, RAG, CRM automation, and the full stack around them)
- How he works
- Shipped products, grouped into Web3 / web apps and React Native mobile apps
- Ten self-initiated concept designs, each opening a dialog with six screens
- Skills
- Contact

Concept designs use fictional sample data. They are not client work. Shipped cards stay limited to the projects that have write-ups.

## Update the copy

Edit `index.html`.

- Hero, services, process, skills, and contact are ordinary sections near the top and bottom of `<main>`.
- Each shipped project is an `<article class="card">` inside `#work`.
- Each concept is a `<button class="concept">` inside `#concepts`, plus a matching `<template id="tpl-…">` at the bottom of the page. The button’s `data-concept` value must match the template id after `tpl-`.

Keep claims limited to what Haseeb has actually written. Do not add projects, clients, metrics, or testimonials.

## Update images

Shipped mockups live in `assets/projects/`. Concept covers and screens live in `assets/concepts/<study>/`. Files are WebP. Grids use a smaller `-sm` or `cover-sm` file via `srcset`.

To replace a picture, export a WebP with the same filename. If the pixel size changes, update the `width` and `height` attributes on that `<img>` so the layout does not jump.

Images with no write-up are intentionally absent. Tastee has a write-up and no mockup, so its card is text only.

## Publish

GitHub Pages is set to deploy from the `main` branch, `/` (root). Merge to `main` and the site updates at [https://haseeb-asim.github.io/](https://haseeb-asim.github.io/).

To preview locally:

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080`.
