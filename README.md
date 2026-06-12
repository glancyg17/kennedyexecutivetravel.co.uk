# Kennedy Executive Travel — Site Guide

Static site, hosted on GitHub Pages at `kennedyexecutivetravel.com`.

## File structure

```
/
├── index.html              Homepage
├── fleet.html               Full fleet overview (all 4 tiers)
├── mercedes-g63.html         VIP — Mercedes G63 AMG
├── mercedes-maybach.html     VIP — Mercedes Maybach
├── audi-sq7.html              VIP — Audi SQ7
├── executive.html             Executive range (V-Class, C-Class, Cayenne)
├── group.html                  Mini Buses (mini buses, Ford Transit)
├── standard.html               Standard range (BMW, VW EOS) — rental available
├── services.html               All 8 services, editorial layout
├── reviews.html                 Full review archive (18 reviews)
├── contact.html                 Contact form + methods
├── privacy.html                 Privacy policy
├── 404.html                     Custom error page
├── sitemap.xml
├── robots.txt
├── llms.txt
├── CNAME                        Domain config — do not edit unless changing domain
├── .gitignore
└── assets/
    ├── icons/
    │   └── favicon.png          512×512px
    └── images/
        ├── logo.png             400×160px, transparent background
        ├── hero.jpg              Homepage hero background, 2400×1600px
        ├── about.jpg
        ├── og-image.jpg          1200×630px — social sharing preview
        ├── [vehicle]-hero.jpg    Main image per vehicle, 1800×1200px
        ├── [vehicle]-2.jpg → -5.jpg   Additional vehicle images, 1400×940px
        └── [service].jpg         8 service images, ~1200×900px
```

## Image checklist

See the image list shared during planning — every placeholder box on every page is labelled with its exact required filename. Drop images into `assets/images/` (or `assets/icons/` for the favicon) using those exact names and the placeholders disappear automatically — no HTML edits needed.

Compression: use squoosh.app, MozJPEG, quality ~70-75, resize to the target dimensions first. Favicon and logo are PNG (OxiPNG).

## Making text changes

All content is plain HTML — find the text in the relevant `.html` file and edit directly. Each page shares the same CSS variables at the top of the `<style>` block:

```css
--black:  #0c0b0b   (background)
--red:    #9e1c1c   (primary accent)
--gold:   #c8a45a   (highlights, prices)
--cream:  #f0ebe0   (text)
```

To change the colour scheme site-wide, these variables would need updating across every page (no shared stylesheet currently — each page is self-contained for simplicity and load speed).

## The reserve modal

Every page (except contact, privacy, 404) includes a "Reserve now" button that opens a booking form modal. It submits via FormSubmit.co to `kennedyexecutivetravel@gmail.com`. The vehicle name is passed automatically based on which button was clicked.

**FormSubmit activation:** the first submission from a new domain triggers a confirmation email to the receiving address — this must be clicked once before submissions start arriving normally.

## Updating prices

Prices appear in multiple places per vehicle — homepage fleet cards, the vehicle's own page, `fleet.html`, and any range pages (`executive.html`, `group.html`, `standard.html`). Search for the price (e.g. `£149`) across files to find all instances when updating.

## Adding a new page

Copy the closest existing page as a template (e.g. copy `mercedes-g63.html` for a new VIP vehicle), update:
1. `<title>` and `<meta name="description">`
2. `<link rel="canonical">`
3. Breadcrumb
4. Page content
5. Add the new page to the nav menus across all pages, the footer links, and `sitemap.xml`

## Deployment

Push changes to the `main` branch — GitHub Pages rebuilds automatically, live within ~2 minutes.
