# CLAUDE.md: claeslanng.shop

The website of **Claes Lanng Plugins**: free, open-source (AGPLv3) VST3 plugins for
Windows, made by Claes Lanng (a DJ and producer from Copenhagen) for FL Studio. Nothing is
sold, despite the `.shop` domain.

Hosting: GitHub Pages from this repo (`claeslanng/claeslanng.github.io`, branch `main`,
root), with the custom domain in `CNAME`. Plain static HTML, no build step. A push goes
live in a minute or two. His DJ site is separate: `claeslanng/claeslanng.com`.

## Pages

```
index.html              home: hero oscilloscope + one panel per plugin, "Free, and open"
smartscope/             Smartscope page    (theme-smartscope: graphite #141517 + orange #F08A24)
pitchscope/             PitchScope page    (theme-pitchscope: kraft + white label, like the plugin)
flow-fmx-host/          Flow FMX Host page (theme-flow: dark #0D1113 + green #2FD18F)
flow-fmx-host/downloads/  the free .fmx plugins (Studio Sampler v38, PitchScope for Flow v32, MonoSafe v25)
404.html                not-found page (uses absolute /assets paths)
assets/site.css         shared styles; colours come from a theme class on <body>
assets/scope.js         the animated kick + bass oscilloscope on the home page
assets/img/<plugin>/    screenshots per plugin
sitemap.xml, robots.txt, CNAME, .nojekyll
```

Each plugin page has the same structure: hero (name, purpose, Download button, version
and requirements), features, plugin-specific sections, install steps, and a footer. Each
page also has JSON-LD (SoftwareApplication) and a canonical link.

## Design rules

- **The owner chose separate, focused pages per plugin**, each in that plugin's own
  colours. The home page uses the brand style: the kraft-box and white-label palette from
  PitchScope's DESIGN.md.
- **Fonts:** Archivo and Archivo Narrow (OFL, self-hosted woff2). No other webfonts.
- **Copy:** plain and specific, sentence case. No all-caps eyebrow labels, no "→" on
  buttons, no numbered markers unless it's a real sequence (install steps are).
- **Motion:** the home-page oscilloscope, and two muted demo loops on the Smartscope page:
  `drag-loop.mp4` in the zoom section (with a short description beside it) and
  `resize-loop.mp4` at the top of "Make it as big as you like" (with a caption; the owner
  asked for it, 2026-11-19). All respect reduced motion (the loops show controls instead
  of playing) and pause off-screen; one script handles every `.demo-video`. The owner asked for video loops to stay small and subtle, always with a
  line saying what they show. Use a muted looping MP4, not a GIF (a GIF of the same loop
  was 13 times bigger and limited to 256 colours). Save loop posters as lossy WebP
  (quality ~88, sharp YUV): they load with the page, before anything plays, and lossless
  posters were 155–180 KB each against 47 KB.
- **Screenshots** get a crisp 1 px outline (`--shot-shadow`), never a soft drop shadow:
  the owner found the blurred shadows looked low quality (banding on the dark pages).
- **Smartscope's name in its two big headings** (the page's `<h1>` and the home-page
  card title) is written like the plugin's logo: "Smart" in the page's text color,
  "scope" in orange (`<span class="logo-accent">`). Only there: the nav, buttons and body
  text keep the plain name.
- **Footers** credit "Claes Lanng Plugins is made by Claes Lanng" (linking to
  https://claeslanng.com), the contact email djclaeslanng@gmail.com, and Patreon
  (https://www.patreon.com/claeslanng).
- **Flow FMX Host** must keep the line saying it isn't affiliated with Google.

## Facts to keep accurate

- **Smartscope:** version 1.2, download https://github.com/claeslanng/Smartscope/releases/latest.
  Resizes from 240 × 110 up to 7680 × 4320 and has a scope-only view (the owner wants
  this promoted: second monitor, TV, tablet). Colors: picker, #RRGGBB hex box, and a dice
  button for random sidechain colors.
- **Spelling: US English across the whole site** ("color", "gray", "license"), matching
  Smartscope's own interface (the owner's call, 2026-11-19). Keep HTML attributes such as
  `aria-labelledby` as they are.
- **PitchScope:** version 0.9 beta (a pre-release, so link to `/releases`, not `/releases/latest`), repo `claeslanng/Pitchscope`
- **Flow FMX Host:** version 0.3, download https://github.com/claeslanng/flow-fmx-host/releases/latest
- **Requirements:** Windows 10 or 11 (64-bit), a VST3 host. Flow FMX Host also needs WebView2.
- **MonoSafe** (the owner's description): a four-band stereo widener with a built-in guard
  that automatically pulls back the width in any band that would cancel out or lose level
  in mono.

When a plugin gets a new release, update its version on its page (hero fine print, the
install file name, and the JSON-LD `softwareVersion`). For a new .fmx version, replace the
file in `flow-fmx-host/downloads/` and update the version and size on the card.

## Screenshots

**Smartscope's images are rendered, not captured** (since 1.2.0). Smartscope's
RenderTest feeds the owner's real kick and bass audio through the real plugin UI and renders
it at 2x. In the Smartscope repo:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release -DSMARTSCOPE_BUILD_TESTS=ON
cmake --build build --target RenderTest
build/RenderTest_artefacts/Release/RenderTest --site /tmp/renders
python3 Tests/make_site_images.py /tmp/renders --readme docs/images \
    --site ../claeslanng.github.io/assets/img/smartscope
```

That writes `main.webp`, `zoom.webp` (2280 × 784, lossless), `main-share.jpg` (1200 px),
`theme-*.webp` (1140 px), `settings.webp` (2x: its `width`/`height` attributes are half
its pixel size, 822 × 302, so it's sharp on high-density screens) and `drag-loop.mp4` +
poster (1280 × 440, 5.7 s, Zoom x5 on two bars: the arrow rests on the next kick, the
grabbing hand pulls it one beat into place, lets go, and later drags it back, so it loops
without a seam; the pointer is drawn by RenderTest to match what the plugin shows), and
`resize-loop.mp4` + poster (1600 × 702, about 8 s: dragged from 760 × 360 down to a strip,
up to fill the frame, scope only on and off, back to 760 × 360). It's rendered on the page's
own background, so it's shown without the outline (`.demo-bare`) and shows no box; keep
that background in sync with `--bg` of `theme-smartscope`. `fullscreen.webp` (1920 × 920,
rendered at 1x like a big monitor, one bar, kick on sidechain 2 in cyan).
Captions name the layer colors for each theme (Graphite orange/light gray,
Midnight cyan/white, Phosphor amber/green, Daylight deep blue/near-black). If the renders
change what's shown, change the captions too.

For other plugins, or a hand capture: ask the owner for real captures from FL Studio: plugin window enlarged to about 2000 px
wide (or Windows scaling at 200%), Hold pressed, mouse pointer out of the window, saved as
PNG and attached in the chat (Gyazo links can't be downloaded from the workspace). Crop off
FL Studio's wrapper bar and border (about 74 px at the top and 5–6 px at the sides and
bottom). Save as lossless WebP at full size; the `width`/`height` attributes are the
pixel size. Social previews (`og:image`, JSON-LD) use a 1200 px JPEG, since some sites
don't read WebP. The settings dialog doesn't grow with the plugin window, so
`settings.webp` is a 900 px crop around the dialog, shown at its natural size; a capture at
Windows 200% scaling would make it sharper on high-density screens. Theme shots are scaled
to 1140 px wide for the two-column grid.

## Checking changes

Serve locally with `python3 -m http.server`, then take desktop (1440 px) and mobile
(390 px) screenshots with Playwright, using system Chrome (`/usr/bin/google-chrome`) if
it's there. Scroll the page so lazy-loaded images appear. Look at the screenshots before
pushing, and send the user the relevant ones.

## Domain status

GoDaddy DNS (nameservers ns53/ns54.domaincontrol.com): four A records for `@` pointing to
185.199.108–111.153, and `www` as a CNAME to `claeslanng.github.io`. The DNS was switched
over on 2026-11-19, and the owner turned on "Enforce HTTPS" in Settings → Pages the same
day. Both claeslanng.shop and www resolve correctly and the site loads over HTTPS. The
`CNAME` file must keep `claeslanng.shop`: changing the custom domain in GitHub's Pages
settings rewrites or deletes that file.

## Open ideas

- All of Smartscope's images and loops are rendered from 1.2.0 (see Screenshots).
- The owner is adding features to Smartscope (Nov 2026). When a new version ships, update
  the version facts and ask whether the screenshots need redoing.
- **Automatic screenshots on release (optional, not set up).** The rendering works (see
  Screenshots); a GitHub Actions job in the Smartscope repo could run it on each release
  and push the images and version number here. It needs a token or deploy key with write
  access to this repo, added by the owner as a secret in the Smartscope repo.
- A separate support address on the domain (e.g. plugins@claeslanng.shop forwarding to
  Gmail), set up by the owner in GoDaddy.

## Guides (live since 2026-11-24)

Practical pages that bring search traffic and lead to a plugin. Brand theme (kraft + white
label), extra styles in `assets/guides.css`. Every page's nav has a Guides link. The guides
other than the note pages are plain HTML: edit them directly, listen buttons from `assets/tone.js`
(`<button data-tone="46.25">`).

```
guides/                         index of all guides
guides/kick-808-phase/          live phase demo -> Smartscope
guides/tune-808-to-key/         5 steps + "which notes for my key" table -> PitchScope
guides/bpm-to-ms/               tempo calculator (default 128; owner picked the genre buttons: Hip-hop 90,
                                Pop 100, House 125, EDM 128, Garage 136, Trap 140, Techno 145, DnB 174);
                                click any number to copy it (number only, units in headers) -> Smartscope
guides/camelot-wheel/           clickable SVG wheel + all 24 codes -> PitchScope, claeslanng.com
guides/flow-music-plugins-windows/  .fmx on Windows, steps + FAQ -> Flow FMX Host
guides/bass-disappears-in-mono/ stereo/mono demo with a mono frequency plot -> MonoSafe
guides/808-notes/               chart of every note C0-B2 (generated)
guides/808-notes/<note>/        one page per note, e.g. f-sharp-1 (generated) -> PitchScope
tools/make_note_pages.py        builds the chart and note pages; PUBLISH lists the notes
```

FL Studio facts confirmed by the owner (2026-11-24, his screenshot in
`assets/img/guides/fl-root-note.webp`): the root note is set by right-clicking a key on the
keyboard in the second Channel settings tab (envelope icon); the label reads "Root note:
D#5"; the "Fine tune" slider sits next to it. He sets the root in FL's default octave (D#5).

Rules for every guide:
- Answer the question in the first sentence, with the number (people and AI tools quote it).
- Every number is calculated or checked, never guessed. Note pages get all their numbers
  from `make_note_pages.py`; edit the template there, not the HTML, then rerun it.
- Something only this site has: a demo, a calculation, or the plugin author's experience.
  No filler pages: if a page would only swap a word, don't publish it.
- Ends with one plugin, the one that solves the problem on the page.
- Octaves: middle C is C4, like PitchScope; always give FL Studio's name too (one higher).
- Add new guides to `guides/index.html` and `sitemap.xml`, and to the "Guides" section at the
  bottom of the plugin page it leads to (`.related` cards, styles in `site.css`).

## Patreon
Each plugin also has a free, public Patreon post (in his "Free plugins" collection), linked from
the hero fine print of its page ("Questions and updates on Patreon"):
- Smartscope: https://www.patreon.com/claeslanng/posts/smartscope-free-176248736
- PitchScope: https://www.patreon.com/claeslanng/posts/pitchscope-free-176300222
- Flow FMX Host: https://www.patreon.com/claeslanng/posts/flow-fmx-host-in-176300568
Patreon shop products can't be free (minimum $3), so free plugins go out as public posts that
link to the site's download, not an uploaded zip (one download to update, counted by GoatCounter).

## Visitor stats
GoatCounter (no cookies, no consent banner needed), site code `claeslanng`: dashboard at
https://claeslanng.goatcounter.com. Every page has its script tag just before `</head>`
(the note pages get it from `head()` in `tools/make_note_pages.py`); add it to every new page.
Download buttons carry `data-goatcounter-click` names (download-smartscope-top,
download-smartscope-install, download-fmx-monosafe, ...), so each download is counted as an event.

## Google
Search basics are in place on every page (title, description, canonical, Open Graph,
JSON-LD: Organization on the home page, SoftwareApplication per plugin), plus robots.txt
and sitemap.xml (update lastmod when a page changes; add new plugin pages to it).
Search Console verification uses Google's HTML file method: google0789dddcf62e118d.html
at the site root (same file as on claeslanng.com). Never delete or rename it.
