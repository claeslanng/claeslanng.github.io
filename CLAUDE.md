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
- **Motion:** only the home-page oscilloscope. It respects reduced motion and pauses
  off-screen.
- **Footers** credit "Claes Lanng Plugins is made by Claes Lanng" (linking to
  https://claeslanng.com), the contact email djclaeslanng@gmail.com, and Patreon
  (https://www.patreon.com/claeslanng).
- **Flow FMX Host** must keep the line saying it isn't affiliated with Google.

## Facts to keep accurate

- **Smartscope:** version 1.1, download https://github.com/claeslanng/Smartscope/releases/latest
- **PitchScope:** version 0.9 beta (a pre-release, so link to `/releases`, not `/releases/latest`), repo `claeslanng/Pitchscope`
- **Flow FMX Host:** version 0.3, download https://github.com/claeslanng/flow-fmx-host/releases/latest
- **Requirements:** Windows 10 or 11 (64-bit), a VST3 host. Flow FMX Host also needs WebView2.
- **MonoSafe** (the owner's description): a four-band stereo widener with a built-in guard
  that automatically pulls back the width in any band that would cancel out or lose level
  in mono.

When a plugin gets a new release, update its version on its page (hero fine print, the
install file name, and the JSON-LD `softwareVersion`). For a new .fmx version, replace the
file in `flow-fmx-host/downloads/` and update the version and size on the card.

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

- More real FL Studio screenshots, or a short screen recording, for Smartscope. One
  real shot is on the page (`assets/img/smartscope/fl-studio.jpg`, under the sidechain
  steps); the hero, zoom, themes and settings images are still synthetic renders.
- Privacy-friendly visitor stats (e.g. GoatCounter). The owner would need to sign up.
- A separate support address on the domain (e.g. plugins@claeslanng.shop forwarding to
  Gmail), set up by the owner in GoDaddy.
