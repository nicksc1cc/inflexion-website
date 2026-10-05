# Perspectives article contract

Every new Perspectives article must use the shared editorial system. The purpose of this contract is to prevent page-local article geometry from drifting.

## Required structure

Each post must:

- load `../assets/design-system/tokens-built.css` before `../assets/common.css`;
- load `../assets/perspectives-editorial.css` after page-local styles;
- include an `.article-hero` section;
- use either `.article-layout` or `.article-grid` as the article shell;
- use `.article-body` or `.article-content` for the reading column;
- include valid JSON-LD;
- preserve the shared navigation and footer;
- contain no page-local max-width or grid rule that changes the reading contract without an intentional design decision.

Both legacy article variants are supported by the shared stylesheet. New posts should prefer:

```html
<section class="article-hero">
  <div class="section-inner">
    <div class="tag">Category</div>
    <h1>Article title <em>with one accent phrase</em></h1>
    <p class="article-dek">Standfirst.</p>
    <div class="article-meta">Date · reading time · Inflexion journal</div>
  </div>
</section>

<section class="article-body">
  <div class="section-inner">
    <div class="article-grid">
      <aside class="article-toc">...</aside>
      <article class="article-content">
        <p class="lead">Opening argument.</p>
        <h2 id="section-id">Section heading</h2>
        <p>Body copy.</p>
      </article>
    </div>
  </div>
</section>
```

## Geometry rules

The shared stylesheet controls:

- hero padding and title scale;
- article shell width;
- margin-note/TOC column;
- reading column width;
- paragraph measure and line-height;
- heading rhythm;
- list, quote, source and CTA treatment;
- 375px, 768px and 1440px behaviour.

Do not add a new article-specific `grid-template-columns`, `max-width`, `margin-left`, or body font rule unless the decision is recorded and the complete route suite is re-rendered.

## Required checks

Run from the website root:

```bash
python3 scripts/audit-perspectives.py
```

Then render every route at 375px, 768px and 1440px. Inspect at least one full-page screenshot for each route and check:

- no horizontal overflow;
- no extreme accidental margins;
- no clipped headings or lists;
- consistent hero geometry;
- consistent body measure;
- visible keyboard focus;
- reduced-motion fallback;
- valid JSON-LD;
- zero browser console errors.

The current route inventory is defined in `scripts/audit-perspectives.py`. Update that list when a new article is published, then run the complete suite again.
