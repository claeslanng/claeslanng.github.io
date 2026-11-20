# CLAUDE.md: claeslanng.com

The personal website of **Claes Lanng**, an open-format DJ and producer from Copenhagen.
Its job: let promoters and fans listen, see who he is, and book him.

Hosting: GitHub Pages from this repo (`claeslanng/claeslanng.com`, branch `main`, root),
with the custom domain in `CNAME`. One static page (`index.html`), no build step. His
plugin site is separate: `claeslanng/claeslanng.github.io` (claeslanng.shop).

## Never invent facts

Everything about Claes on the site has been approved by him. Don't add venues, numbers,
releases, genres or quotes he hasn't given you, and ask before adding a new social link.

**Approved facts** (from his own SoundCloud, Bandcamp and TikTok profiles, and his
approval in chat):
- Open-format DJ and producer, based in Copenhagen, Denmark. He DJs full-time.
- For more than a decade he has played clubs, venues and festivals across Europe.
- He "plays everything". His productions are mashups, bootlegs, remixes and originals.
- Booking email: **djclaeslanng@gmail.com**
- He has a second SoundCloud account, "Claes Lanng 2", for mashups and bootlegs, many
  with free downloads (from its own bio; he asked for it on the site).

**Approved links** (only these; he explicitly left out Mixcloud):
- Instagram https://www.instagram.com/claeslanng/
- TikTok https://www.tiktok.com/@claeslanng
- Facebook https://www.facebook.com/djclaeslanng/
- SoundCloud https://soundcloud.com/claeslanng
- SoundCloud 2 https://soundcloud.com/claeslanng2 (mashups & bootlegs)
- Bandcamp https://claeslanng1.bandcamp.com/
- Patreon https://www.patreon.com/claeslanng

**Releases shown:** Finde Tilbage (Claes Lanng Remix, 2026, SoundCloud), Tropico Swing
(original, Bandcamp), Boing! (Claes Lanng Remix of Nik & Jay, 2024, Bandcamp), Dark Room
(Claes Lanng Remix, 2024, Bandcamp).

## Page structure

Fixed top menu: Music, Photos, About, Booking, then "Plugins ↗" (to claeslanng.shop, set
apart by a thin divider; he wanted the plugin site easier to find). Phones drop Photos to
fit. See-through over the hero, then a dark bar with a small logo (back to top) once you
scroll past 40 px.
Hero (full-screen live photo, logo, tagline, Listen and Book buttons), Music (SoundCloud
player that only loads on click, with Main account / Mashups & bootlegs tabs above it that
pick which account it shows, release list, platform links), Photos (four-photo grid),
About (portrait + bio), Booking (white section: big email, write/copy buttons, press kit,
socials), footer (logo + ©).

The bio text appears in two places: `index.html` (About) and `press/bio.txt`. After
changing it, rebuild `press/claes-lanng-press-kit.zip`. It contains bio.txt, five photos
at up to 2400 px, and the logo as PNG and SVG. The originals came from the owner's
uploads; ask him for them if you need to rebuild the photos.

## Logo (keep it as close to the original as possible)

- `assets/logo-original.svg`: white letters, black outline. A vector trace of his
  `CLAES_LANNG-01.png`.
- `assets/logo-rim.svg`: the same with an extra white outer edge, like his YouTube banner.
  **Use this one on dark backgrounds and photos**: hero, footer, 404. He asked for the
  white-outlined version in the footer.
- Don't recolour it or redraw the letters.

## Design

- Black and white like the logo, with amber `#FFB23E` (from the festival light) as a
  sparing accent for hover and focus. Booking is the one white section.
- Fonts: **Schibsted Grotesk Black** (display: headings, email, track titles, buttons;
  one 900 woff2, Latin incl. æøå) and **Archivo** (body), both OFL and self-hosted.
  He chose Schibsted on 2026-11-20 over Anton, Big Shoulders Display and Space Grotesk;
  he found the old display font (Unbounded) too wide.
- Buttons are "cut out" of the logo: white blocks with a hard black edge.
- Fast loading is a requirement: about 300 KB before play, and no third-party requests
  until someone clicks the SoundCloud player. Photos are WebP plus JPEG fallbacks at a few
  widths (`assets/img/<name>-<width>.webp|jpg`). Lazy-load everything below the hero.
- On iPhone: the page has no bottom bounce (`overscroll-behavior-y: none`), and the html
  background matches the footer. The booking email must fit on one line on phones.

## Photos

Used: the warm festival shot (hero), the seated portrait in the "CHAOTIC" shirt (About),
the Copenhagen street party, the club shaka shot, and two black-and-white studio
portraits (gallery).

Left out on purpose: the teal version of the festival shot (same moment), the other two
seated portraits (same pose), the YouTube banner, and the pink cut-out banner.

## Checking changes

Serve locally with `python3 -m http.server`, then take desktop (1440 px) and mobile
(390 px) screenshots with Playwright, using system Chrome (`/usr/bin/google-chrome`) if
it's there. Look at them before pushing, and send the user the relevant ones.

## Domain status

GoDaddy DNS: four A records for `@` pointing to 185.199.108–111.153, and `www` as a CNAME
to `claeslanng.github.io`. If HTTPS isn't enforced yet, the owner has to click "Check
again" and then tick "Enforce HTTPS" in Settings → Pages.

## Missing (needs material from Claes)

- Venues and festivals he has played (the most useful thing for bookers).
- A short video clip of a set.
- A recent 30–60 minute DJ mix.
- Upcoming shows, only if he plays regularly.
- Spotify or YouTube links, if he has them.
- A booking address on the domain (e.g. booking@claeslanng.com forwarding to Gmail, set
  up in GoDaddy).

## Google
Search basics are in place: title, meta description, canonical, Open Graph, Person
structured data (JSON-LD with sameAs to every profile), robots.txt and sitemap.xml.
Update sitemap.xml's lastmod when the page changes. As of 2026-11-20 the site was not
in search results yet and Search Console was not set up; Claes has to verify it
himself with his Google account. He verified with Google's HTML file method:
google0789dddcf62e118d.html at the site root. Never delete or rename that file
(removing it un-verifies the site in Search Console).
