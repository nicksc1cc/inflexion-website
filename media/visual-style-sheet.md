# Inflexion Media — Visual Style Sheet

## Brand Colours (from DESIGN.md + tokens.css)

| Token | Value | Usage |
|-------|-------|-------|
| `--inf-accent` | `#FF5A1F` | CTAs, emphasis, section numbers, highlights |
| `--inf-data` | `#2438DA` | Charts, data tables, statistical callouts, metrics |
| `--inf-fg` | `#0A0A0B` | Body text on light |
| `--inf-fg2` | `#71717A` | Muted text, captions |
| `--inf-fg3` | `#A1A1AA` | Tertiary text, tags |
| `--inf-bg` | `#FAFAF9` | Page bg (warm white) |
| `--inf-bg2` | `#F4F4F0` | Card/secondary surface |
| `--inf-border` | `rgba(10,10,11,.08)` | Dividers |
| `--inf-dark-bg` | `#0A0A0B` | Dark section bg |
| `--inf-dark-text` | `rgba(250,250,249,.9)` | Text on dark |

**Rules:** Orange for action/emphasis only. Blue for data/charts only. Never teal. Never pure black or white.

## Typography

| Element | Font | Weight | Size | Tracking |
|---------|------|--------|------|----------|
| H1 (hero) | Montserrat | 200 | clamp(36px,7vw,84px) | -.03em |
| H2 (section) | Montserrat | 200 | clamp(28px,3.5vw,44px) | -.02em |
| H3 | Montserrat | 500 | clamp(16px,1.4vw,22px) | — |
| Body | Montserrat | 300 | 15px | — |
| Tag/eyebrow | Montserrat | 500 | 10px | .15em uppercase |
| Mono data | IBM Plex Mono | 500 | 13-14px | — |
| Section number | IBM Plex Mono | 500 | 14px | — accent colour |

## Editorial Rhythm (7 sections)

1. **Hero** — Dark bg (#0A0A0B). Bold headline in extralight 200. Exhibit preview as visual.
2. **Problem & System** — Light bg (#FAFAF9). Numbered section. Integrated system diagram.
3. **Measurement & Investment** — Light bg. Full-width analytical exhibits (A, B, C) as editorial gallery.
4. **Amazon & Retail Media** — Alternating dark/light. Exhibit D as centrepiece. Compact capability tags.
5. **AI Intelligence** — Light bg. Exhibit E. Editorial explanation, no cards.
6. **Judgement** — Dark bg. Short, decisive. Brand tagline.
7. **Conversion** — Light bg. Two CTAs, minimal copy.

## Components to use (from tokens.css)
- `.inf-h1`, `.inf-h2`, `.inf-h3` — heading classes
- `.inf-prose` — body text
- `.inf-tag` — eyebrow labels
- `.inf-btn`, `.inf-btn-outline` — buttons
- `.inf-data` — data blue colour class
- `.inf-dark` — dark section wrapper
- `.inf-data-banner` — stat grid
- `.inf-metric-card` — compact KPI cards
- `.inf-feat-grid` — 2-col feature grid
- `.inf-phase-card` — numbered content cards
- `.inf-sec-num` — section number prefix

## What to remove from current page
- All teal colours (#167171, #1a8a8a, var(--accent) pointing to teal)
- Custom CSS classes: `.svc-grid`, `.proc-grid`, `.proc-step`, `.eff-grid`, `.eff-card`, `.stk`, `.stk-d`
- Custom layout classes: `.flow-row`, `.flow-node`, `.chan-grid`, `.agent-grid`
- Three.js canvas (unless meaningful analytical visual — remove and replace with static exhibit preview)
- All inline styles using wrong colour variables

## Analytical Exhibit Design Language (Tufte-inspired)
- Range-frame axes (top + right only)
- Direct labels next to data points, not legends
- High data-ink ratio — no gridlines, no fills
- Annotations adjacent to the evidence
- Small multiples for comparisons
- Sparklines for trends, slopegraphs for changes
- Data blue (#2438DA) for chart elements
- Orange (#FF5A1F) only for the primary finding callout
- Captions: short sentence explaining commercial implication
- Consistent footnote treatment: methodology and assumptions

## Mobile adaptations
- Single-column stack for exhibits
- Simplified annotations
- No horizontal scroll on main page
- Exhibit summaries accessible without the full detail view