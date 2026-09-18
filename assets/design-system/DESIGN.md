# Inflexion — Design System

> Category: Brand & Agency
> Full-service marketing agency for the AI era. Editorial monochrome design with a single orange accent (#FF5A1F) and blue data accent (#2438DA). Inspired by vanlent.dev editorial layout, numbered sections, and dark-to-light page flow.

## 1. Visual Theme & Atmosphere

Inflexion's design is **editorial, not templated**. It avoids generic agency motifs — no multi-color gradients, no stock "AI slop" vocabulary, no glassmorphism. The page reads like a high-end publication: monochrome headlines, single accent color for emphasis, data presented in blue, and generous whitespace.

- **Visual style:** editorial, monochrome, numbered-sections
- **Color stance:** monochrome + single accent (#FF5A1F) + data accent (#2438DA)
- **Design intent:** Authority through restraint. One idea lands per section. Every element earns its place.
- **Reference:** vanlent.dev — numbered sections, Montserrat, grid background, dark→light flow
- **Rejects:** Generic templates, multi-color gimmicks, AI-slop vocabulary (optimise, transform, elevate, landscape, vibrant, robust, leverage, holistic, drive, unlock)

## 2. Color

### Brand Palette
- **Accent (orange):** `#FF5A1F` — Primary CTA, emphasis, section numbers, highlights
- **Data accent (blue):** `#2438DA` — Data visualisation, charts, statistics, metrics
- **Foreground:** `#0A0A0B` — Body text, headings on light backgrounds
- **Foreground 2:** `#71717A` — Muted body text, captions, secondary info
- **Foreground 3:** `#A1A1AA` — Tertiary text, meta, tags
- **Background:** `#FAFAF9` — Page background (warm white)
- **Background 2:** `#F4F4F0` — Card/secondary surface
- **Border:** `rgba(10,10,11,.08)` — Subtle dividers
- **Border 2:** `rgba(10,10,11,.12)` — Stronger dividers

### Dark Mode (hero sections, dark slides)
- **Dark bg:** `#0A0A0B` — Dark section backgrounds
- **Dark text:** `rgba(250,250,249,.9)` — Primary text on dark
- **Dark text 2:** `rgba(250,250,249,.7)` — Secondary text on dark
- **Dark border:** `rgba(250,250,249,.08)` — Dividers on dark
- **Dark border 2:** `rgba(250,250,249,.12)` — Stronger dividers on dark

### Usage rules
- Use accent (#FF5A1F) sparingly — never for large surfaces. Only for CTAs, section numbers, emphasis, and interactive elements.
- Use data accent (#2438DA) only for data/chart contexts — never for UI chrome.
- Text on light: #0A0A0B for body, #71717A for secondary. Text on dark: rgba(250,250,249,.9) for body, rgba(250,250,249,.7) for secondary.
- Never use pure black (#000) or pure white (#FFF) — the warm off-whites and near-blacks are intentional.

## 3. Typography

- **Scale:** 10/12/14/15/16/18/22/24/28/36/40/56/72
- **Families:** primary=Montserrat, mono=IBM Plex Mono
- **Weights:** 200 (extralight — hero headings), 300 (light — body), 400 (regular — prose), 500 (medium — navigation, tags), 600 (semibold — emphasis), 700 (bold — strong emphasis)
- **Hero headings:** weight 200, letter-spacing -.03em, line-height 1.0
- **Section headings (h2):** weight 200, letter-spacing -.02em, line-height 1.05
- **Body text:** weight 300, line-height 1.7, color #71717A
- **Tag/eyebrow:** 10px, weight 500, letter-spacing .15em, uppercase
- **Section numbers:** 10–14px, monospace, weight 500, accent color

### Usage rules
- Hero headings should be extralight (200) with tight negative tracking. This is the signature Inflexion look.
- Body text is light weight (300) in muted grey (#71717A) — never full black.
- Numbered sections are a core design element: section number in monospace + accent color, followed by heading.
- IBM Plex Mono for data, metrics, code, and any statistical reference.

## 4. Spacing & Grid

- **Base unit:** 8px
- **Section padding:** 80px vertical (desktop), 60px (mobile)
- **Section inner:** max-width 900px, centered
- **Hero section:** 100vh min-height, vertical centering
- **Content grids:** 2-column feat-grid, 3-column stat-row, auto-fit metric-grid

### Layout principles
- Generous top padding on sections — content should breathe.
- Max-width 900px for reading comfort. Never full-width body text.
- Use horizontal dividers (1px, border color) between sections for rhythm.
- Dark sections (hero, alternating slides) use #0A0A0B background with white text.

## 5. Components

### Hero Section
- Dark background (#0A0A0B) with Three.js Data Field canvas animation
- Tag/eyebrow: 10px uppercase, 500 weight, .15em spacing, 50% opacity
- H1: 200 weight, clamp(36px,7vw,84px), -.03em tracking, line-height 1.0
- Description: 17px, 300 weight, #71717A
- Data banner: 3–6 stat grid below hero, each with value (accent color, 200 weight) + label (10px uppercase)

### Section Headers
- Numbered: `01.` in monospace + accent, followed by h2 heading
- Tag: 10px uppercase above heading
- H2: 200 weight, clamp(28px,3.5vw,44px), -.02em tracking

### Data Banner
- Grid of stats: value (clamp(28px,3vw,48px), 200 weight, accent color) + label (10px, 500 weight, uppercase, #fg3) + source (11px, #fg3)
- 4-column default, 6-column on index, 3-column on tablet, 2-column on mobile

### Feature Cards (2-col grid)
- `.feat-grid` with 2-column layout
- Each card: tag (10px uppercase, accent), heading (16–20px, 600 weight), body (14px, 300 weight, #fg2)
- Cards separated by borders, not padding

### Metric Cards
- Compact: value (20–32px, 200 weight, accent), label (10px uppercase, #fg3), optional source text
- Used for data clusters, KPIs, stats

### Buttons
- Primary: accent background (#FF5A1F), white text, 12px uppercase, 500 weight, .12em spacing, 16px 32px padding
- Outline: transparent, 2px border, matches current text color
- Hover: opacity .85

### Phase Cards
- Numbered content cards with large faded number (monospace, 32px, accent, .15 opacity)
- Used for process steps, approaches, timelines

### Data Table
- Clean tables with uppercase headers (10px, 600 weight, #fg3), dashed bottom borders
- Accent-colored first column for brand names
- Muted (#fg2) for secondary data

### Timeline
- Vertical timeline with accent-colored dots and line
- Date (10px uppercase, accent), heading (16px, 500 weight), body (13px, #fg2)
- Used for schedules, roadmaps, event sequences

## 6. Data Presentation

- **Data accent (#2438DA)** is used exclusively for data-related contexts: charts, data tables, statistical callouts, dashboards
- Never mix accent orange and data blue in the same UI element — orange is for action/emphasis, blue is for data
- Tufte-inspired chart rendering: range-frame axes (top + right only), direct labels instead of legends, high data-ink ratio
- Sparklines for trend data, slopegraphs for before/after comparisons, radar charts for multi-dimensional comparisons

## 7. Dark/Light Flow

- **Hero:** Always dark (#0A0A0B) with Three.js animated background
- **Alternating sections:** Light (#FAFAF9) → dark → light → dark flow
- Dark sections use: `rgba(250,250,249,.9)` text, `rgba(250,250,249,.7)` secondary, `rgba(250,250,249,.08)` borders
- The dark-to-light rhythm creates editorial pacing

## 8. Motion & Interaction

- **GSAP ScrollTrigger** for scroll-reveal animations
- **IntersectionObserver** fallback when GSAP not loaded
- Default reveal: fade-up with 0.6s ease, staggered per element
- 100ms delay increments between sibling elements
- Reduced motion: `prefers-reduced-motion` disables all animations
- Three.js Data Field: animated particle field in hero background

## 9. Anti-patterns

- Do not use multi-color gradients or rainbow palettes — the system is monochrome + one accent + one data accent
- Do not use glassmorphism or backdrop-filter except on navigation headers
- Do not use AI-slop vocabulary: optimise, transform, elevate, landscape, vibrant, robust, leverage, holistic, drive, unlock
- Do not use generic SaaS layouts (centered hero + three equal feature cards) — vary section structure
- Do not use pure black (#000) or pure white (#FFF) — always use the warm off-whites and near-blacks
- Do not use emoji as design elements
- Do not use left-border accent callout cards (decorative rail)
- Every CTA must be distinct per page — vary the first-argument structure
- Do not use Inter or system-ui as default type — Montserrat is the Inflexion typeface