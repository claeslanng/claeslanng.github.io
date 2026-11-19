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
- **Motion:** the home-page oscilloscope, and one small muted demo loop on the Smartscope
  page (`drag-loop.mp4`, in the zoom section, with a short description beside it). Both
  respect reduced motion (the loop shows controls instead of playing) and pause
  off-screen. The owner asked for video loops to stay small and subtle, always with a
  line saying what they show. Use a muted looping MP4, not a GIF (a GIF of the same loop
  was 13 times bigger and limited to 256 colours).
- **Screenshots** get a crisp 1 px outline (`--shot-shadow`), never a soft drop shadow:
  the owner found the blurred shadows looked low quality (banding on the dark pages).
- **Footers** credit "Claes Lanng Plugins is made by Claes Lanng" (linking to
  https://claeslanng.com), the contact email djclaeslanng@gmail.com, and Patreon
  (https://www.patreon.com/claeslanng).
- **Flow FMX Host** must keep the line saying it isn't affiliated with Google.

## Facts to keep accurate

- **Smartscope:** version 1.2, download https://github.com/claeslanng/Smartscope/releases/latest.
  Resizes from 240 × 110 up to 7680 × 4320 and has a scope-only view (the owner wants
  this promoted: second monitor, TV, tablet). Colors: picker, #RRGGBB hex box, and a dice
  button for random sidechain colors.
- **Spelling on the Smartscope page:** US English ("color", "colored", "gray"), matching
  the plugin (the owner's call, 2026-11-19).
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

Ask the owner for real captures from FL Studio: plugin window enlarged to about 2000 px
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
over on 2026-11-19. If HTTPS isn't enforced yet, the owner has to click "Check again" and
then tick "Enforce HTTPS" in Settings → Pages.

## Open ideas

- All Smartscope images are real captures (`main.webp`, `zoom.webp`, `theme-*.webp`,
  `settings.webp`, `fullscreen.webp` for "Make it as big as you like"). They were taken
  with 1.1, so the header lacks 1.2's corners (scope only) button, and `settings.webp`
  lacks the hex boxes and the dice button. Redo them with 1.2 (by hand or with the
  RenderTest plan below).
- The drag loop is cut from a Gyazo clip (1280 px, end card removed, a short blend at the
  seam). A new recording that starts and ends on the same view, made with the Windows
  Snipping Tool at full size, would loop perfectly.
- The owner is adding features to Smartscope (Nov 2026). When a new version ships, update
  the version facts and ask whether the screenshots need redoing.
- **Planned after Smartscope 1.2.0: automatic screenshots.** Smartscope's
  `Tests/RenderTest.cpp` already renders the real UI to PNG with a fake host. The plan is
  to feed it the owner's real audio (branch `screenshot-audio` in `claeslanng/smartscope`,
  `Tests/audio/`: kick for sidechain 1, ducked bass for the main input, 4 bars at 128 BPM),
  render at 2x the main shot, zoom, the four themes (with different layer colours per
  theme: Graphite orange/grey, Midnight cyan/white, Phosphor amber/green, Daylight deep
  blue or red/near-black), settings, and frames for a perfectly looping drag video, then
  possibly a GitHub Action that updates this site on each release. Wait for the owner to
  say 1.2.0 is merged before touching Smartscope's `main`.
- Privacy-friendly visitor stats (e.g. GoatCounter). The owner would need to sign up.
- A separate support address on the domain (e.g. plugins@claeslanng.shop forwarding to
  Gmail), set up by the owner in GoDaddy.
