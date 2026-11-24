#!/usr/bin/env python3
"""Builds the 808 note guides: the chart (guides/808-notes/) and one page per note.

Every number on these pages is calculated here (equal temperament, A4 = 440 Hz), so
the pages can't drift from the facts. Run it from the repo root:

    python3 tools/make_note_pages.py

PUBLISH lists the notes that get their own page. Add notes to it to publish more;
the chart links every note that has a page.
"""
import html
import json
import os

PUBLISH = ["F#1", "G1"]          # notes with their own page (preview: two samples)
OCTAVES = [0, 1, 2]              # the chart covers C0 to B2
UPDATED = "2026-11-24"
SITE = "https://claeslanng.shop"

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLATS = {"C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab", "A#": "Bb"}
SLUG = {"C": "c", "C#": "c-sharp", "D": "d", "D#": "d-sharp", "E": "e", "F": "f",
        "F#": "f-sharp", "G": "g", "G#": "g-sharp", "A": "a", "A#": "a-sharp", "B": "b"}

MAJOR_KEYS = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
MINOR_KEYS = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
CAMELOT_MAJOR = ["8B", "3B", "10B", "5B", "12B", "7B", "2B", "9B", "4B", "11B", "6B", "1B"]
CAMELOT_MINOR = ["5A", "12A", "7A", "2A", "9A", "4A", "11A", "6A", "1A", "8A", "3A", "10A"]
MAJOR_STEPS = [0, 2, 4, 5, 7, 9, 11]
MINOR_STEPS = [0, 2, 3, 5, 7, 8, 10]
DEGREES = ["root", "2nd", "3rd", "4th", "5th", "6th", "7th"]


class Note:
    def __init__(self, midi):
        self.midi = midi
        self.pc = midi % 12
        self.octave = midi // 12 - 1
        self.letter = NAMES[self.pc]
        self.name = f"{self.letter}{self.octave}"
        self.fl_name = f"{self.letter}{self.octave + 1}"      # FL Studio calls middle C "C5"
        self.hz = 440.0 * 2 ** ((midi - 69) / 12)
        self.cycle_ms = 1000.0 / self.hz
        self.slug = f"{SLUG[self.letter]}-{self.octave}"

    @property
    def article(self):
        return "an" if self.letter[0] in "AEF" else "a"

    @property
    def spoken(self):
        flat = FLATS.get(self.letter)
        return f"{self.name} ({flat}{self.octave})" if flat else self.name

    def shifted(self, semitones):
        return Note(self.midi + semitones)


def note_from_name(name):
    letter, octave = name[:-1], int(name[-1])
    return Note((octave + 1) * 12 + NAMES.index(letter))


def hz(x):
    return f"{x:.2f}"


def ms(x):
    return f"{x:.1f}" if x >= 10 else f"{x:.2f}"


def esc(s):
    return html.escape(s, quote=True)


def page_url(note):
    return f"/guides/808-notes/{note.slug}/"


def is_published(note):
    return note.name in PUBLISH


def note_link(note, prefix):
    """Link to a note's own page if it has one, else to its row in the chart."""
    if is_published(note):
        return f'{prefix}{note.slug}/'
    return f'{prefix}#{note.slug}'


def keys_with(note):
    rows = []
    for root, (name, cam) in enumerate(zip(MINOR_KEYS, CAMELOT_MINOR)):
        step = (note.pc - root) % 12
        if step in MINOR_STEPS:
            rows.append((MINOR_STEPS.index(step), f"{name} minor", cam))
    for root, (name, cam) in enumerate(zip(MAJOR_KEYS, CAMELOT_MAJOR)):
        step = (note.pc - root) % 12
        if step in MAJOR_STEPS:
            rows.append((MAJOR_STEPS.index(step), f"{name} major", cam))
    order = {0: 0, 4: 1}                                    # root first, then fifth
    rows.sort(key=lambda r: (order.get(r[0], 2), r[0], "major" in r[1]))
    return rows


def hearing(note):
    f = note.hz
    if f < 20:
        return ("Below 20 Hz, the usual lower limit of hearing. On a big club system you feel it "
                "more than hear it, and most speakers barely move. PitchScope reads notes down to "
                "20 Hz, so it may not show this one.")
    if f < 40:
        return ("Deep sub. It comes through on club systems, subwoofers and good headphones. "
                "Smaller studio monitors start to lose it, and phone and laptop speakers play none "
                "of it, so listeners there only hear its harmonics. Distortion or saturation on the "
                "808 adds harmonics, which is what lets it come through on small speakers.")
    if f < 60:
        return ("The classic 808 range. Clear on a club system, a subwoofer, good headphones and most "
                "studio monitors. Phone and laptop speakers can't play it, so listeners there only "
                "hear its harmonics. Distortion or saturation on the 808 adds harmonics, which is "
                "what lets it come through on small speakers.")
    return ("High for an 808, so it comes through on more systems, including decent earbuds. Phone "
            "speakers still only play its upper harmonics. It can start to crowd the kick and the "
            "low end of the bass line, so check how they sit together.")


# ---------------------------------------------------------------- shared page parts

def head(title, description, canonical, depth, extra_ld):
    up = "../" * depth
    ld = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(obj, indent=1, ensure_ascii=False)}\n</script>'
        for obj in extra_ld)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title.split(' | ')[0])}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{SITE}/assets/img/pitchscope/label.jpg">
<meta property="og:url" content="{SITE}{canonical}">
<meta name="theme-color" content="#5E4630">
<link rel="canonical" href="{SITE}{canonical}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{up}assets/fonts/ArchivoNarrow_700Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/site.css">
<link rel="stylesheet" href="{up}assets/guides.css">
{ld}
</head>
<body class="theme-brand">

<header class="site-header">
  <div class="wrap">
    <a class="wordmark" href="{up}" aria-label="Claes Lanng Plugins, home">Claes Lanng <span>Plugins</span></a>
    <nav class="site-nav" aria-label="Site">
      <a href="{up}smartscope/">Smartscope</a>
      <a href="{up}pitchscope/">PitchScope</a>
      <a href="{up}flow-fmx-host/">Flow FMX Host</a>
      <a href="{up}guides/" aria-current="page">Guides</a>
      <a href="https://github.com/claeslanng">GitHub</a>
    </nav>
  </div>
</header>
"""


def footer(depth):
    up = "../" * depth
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <p>Frequencies use standard tuning (A4 = 440 Hz) and name middle C as C4, like PitchScope. FL Studio's piano roll names it C5, one octave higher.</p>
    <nav aria-label="Footer">
      <a href="{up}guides/">All guides</a>
      <a href="{up}">All plugins</a>
    </nav>
    <p class="maker">Claes Lanng Plugins is made by <a href="https://claeslanng.com">Claes Lanng</a>, a DJ and producer from Copenhagen. Questions or problems? Email <a href="mailto:djclaeslanng@gmail.com">djclaeslanng@gmail.com</a>. Like the plugins? <a href="https://www.patreon.com/claeslanng">Support them on Patreon</a>.</p>
  </div>
</footer>
<script src="{up}assets/tone.js" defer></script>
</body>
</html>
"""


def article_ld(headline, description, url):
    return {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": headline,
        "description": description,
        "url": f"{SITE}{url}",
        "dateModified": UPDATED,
        "author": {"@type": "Person", "name": "Claes Lanng", "url": "https://claeslanng.com"},
        "publisher": {"@type": "Organization", "name": "Claes Lanng Plugins", "url": f"{SITE}/"},
    }


def breadcrumbs_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{SITE}{url}"}
            for i, (name, url) in enumerate(items)
        ],
    }


def pitchscope_panel(depth, note=None):
    up = "../" * depth
    if note:
        title = f"Is your 808 really {note.name}?"
        body = (f"PitchScope reads the note of an 808 down to 20 Hz, shows how many cents off it is, "
                f"and turns green within 4 cents. At {note.name}, 4 cents is only "
                f"{note.hz * (2 ** (4 / 1200) - 1):.2f} Hz. It's free, for Windows.")
    else:
        title = "Find the note of your 808"
        body = ("PitchScope reads the note of an 808, bass or kick down to 20 Hz, with the frequency "
                "and how many cents off it is. It's free, for Windows, made for FL Studio.")
    return f"""
  <section class="section">
    <div class="wrap">
      <div class="next">
        <div>
          <h2>{esc(title)}</h2>
          <p>{esc(body)}</p>
          <div class="actions">
            <a class="btn btn-download" href="{up}pitchscope/">Get PitchScope</a>
          </div>
        </div>
        <img src="{up}assets/img/pitchscope/label.jpg" width="840" height="600" loading="lazy" alt="PitchScope reading an 808 as F sharp 1, 46.3 Hz">
      </div>
    </div>
  </section>
"""


# ---------------------------------------------------------------- the chart

def chart_page():
    url = "/guides/808-notes/"
    title = "808 note frequency chart: every note from C0 to B2 in Hz | Claes Lanng Plugins"
    desc = ("The frequency of every 808 note from C0 to B2, with FL Studio's octave names, the length "
            "of one cycle, and a button to hear each note.")
    out = [head(title, desc, url, 2, [
        article_ld("808 note frequency chart", desc, url),
        breadcrumbs_ld([("Guides", "/guides/"), ("808 note frequency chart", url)]),
    ])]
    out.append(f"""<main>
  <section class="g-hero">
    <div class="wrap">
      <p class="crumbs"><a href="../">Guides</a></p>
      <h1>808 note frequency chart</h1>
      <p class="answer">Most 808s sit in the first octave, roughly <strong>C1 (32.7 Hz)</strong> to <strong>B1 (61.7 Hz)</strong>. Here's every note from C0 to B2, with the name FL Studio uses for it.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="prose">
        <p class="lead">Frequencies use standard tuning, A4 = 440 Hz. "One cycle" is how long one wave of the note takes, which matters when you line a kick up with an 808 (more on that in <a href="../kick-808-phase/">Kick and 808 phase</a>).</p>
        <p class="lead">Headphones or a subwoofer help with the listen buttons. Laptop and phone speakers can't play most of these notes.</p>
      </div>
""")
    for octave in OCTAVES:
        out.append(f"""
      <h3 id="octave-{octave}">Octave {octave}</h3>
      <div class="table-scroll">
      <table class="data">
        <thead><tr><th scope="col">Note</th><th scope="col">Frequency</th><th scope="col">In FL Studio</th><th scope="col">One cycle</th><th scope="col"><span class="visually-hidden">Listen</span></th></tr></thead>
        <tbody>
""")
        for pc in range(12):
            n = Note((octave + 1) * 12 + pc)
            label = esc(n.spoken)
            name_cell = f'<a href="{n.slug}/">{label}</a>' if is_published(n) else label
            faint = ' class="faint"' if n.hz < 20 else ""
            out.append(
                f'          <tr id="{n.slug}"{faint}><th scope="row">{name_cell}</th>'
                f'<td>{hz(n.hz)} Hz</td><td>{n.fl_name}</td><td>{ms(n.cycle_ms)} ms</td>'
                f'<td class="play-cell"><button type="button" data-tone="{n.hz:.4f}" aria-pressed="false" '
                f'aria-label="Listen to {n.name}">Listen</button></td></tr>\n')
        out.append("        </tbody>\n      </table>\n      </div>\n")
    out.append("""
      <p class="fineprint">Grayed-out notes are below 20 Hz, the usual lower limit of hearing.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="fl-title">
    <div class="wrap prose">
      <h2 id="fl-title">Why FL Studio shows a different octave</h2>
      <p>There are two ways to number octaves. Most tuners, PitchScope included, call middle C "C4". FL Studio's piano roll calls it "C5". Same note, same frequency, different name: an 808 that a tuner reads as F#1 is F#2 in FL's piano roll. The chart shows both.</p>
    </div>
  </section>
""")
    out.append(pitchscope_panel(2))
    out.append("</main>\n")
    out.append(footer(2))
    return "".join(out)


# ---------------------------------------------------------------- one note

def note_page(note):
    url = page_url(note)
    flat = FLATS.get(note.letter)
    also = f" ({flat}{note.octave})" if flat else ""
    title = f"{note.name} 808: {hz(note.hz)} Hz ({note.fl_name} in FL Studio) | Claes Lanng Plugins"
    desc = (f"An 808 on {note.name}{also} is {hz(note.hz)} Hz. One cycle lasts {ms(note.cycle_ms)} ms. "
            f"Which keys it fits, how to tune the kick to it, and who will hear it.")
    down, up1 = note.shifted(-1), note.shifted(1)
    oct_down, oct_up = note.shifted(-12), note.shifted(12)
    fifth = note.shifted(7)
    fourth_below = note.shifted(-5)            # the fifth's pitch class, below the root
    half = note.cycle_ms / 2
    gap_down, gap_up = note.hz - down.hz, up1.hz - note.hz

    out = [head(title, desc, url, 3, [
        article_ld(f"{note.name} 808: {hz(note.hz)} Hz", desc, url),
        breadcrumbs_ld([("Guides", "/guides/"), ("808 note frequency chart", "/guides/808-notes/"),
                        (note.name, url)]),
    ])]
    out.append(f"""<main>
  <section class="g-hero">
    <div class="wrap">
      <p class="crumbs"><a href="../../">Guides</a> / <a href="../">808 note frequency chart</a></p>
      <h1>{note.name} 808</h1>
      <p class="answer">An 808 on {esc(note.name + also)} is <strong>{hz(note.hz)} Hz</strong>. FL Studio's piano roll calls it {note.fl_name}.</p>
      <dl class="facts">
        <div><dt>Frequency</dt><dd>{hz(note.hz)} Hz</dd></div>
        <div><dt>In FL Studio</dt><dd>{note.fl_name}<small>Same note, FL names octaves one higher</small></dd></div>
        <div><dt>One cycle</dt><dd>{ms(note.cycle_ms)} ms</dd></div>
        <div><dt>MIDI note</dt><dd>{note.midi}</dd></div>
      </dl>
      <div class="actions" style="margin-top:24px">
        <button class="btn btn-quiet btn-listen" type="button" data-tone="{note.hz:.4f}" aria-pressed="false">Listen to {note.name}</button>
      </div>
      <p class="fineprint">A plain sine wave, the core of an 808. Use headphones or a subwoofer: laptop and phone speakers can't play it.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="hear-title">
    <div class="wrap prose">
      <h2 id="hear-title">Who will hear it</h2>
      <p>{esc(hearing(note))}</p>
      <h3>Close neighbors</h3>
      <p>The note below, {down.name}, is {hz(down.hz)} Hz, and the note above, {up1.name}, is {hz(up1.hz)} Hz. That's only {gap_down:.1f} and {gap_up:.1f} Hz away, so an 808 that's a little out of tune is easy to miss by ear down here. An octave down, {oct_down.name} is {hz(oct_down.hz)} Hz{", below the usual limit of hearing" if oct_down.hz < 20 else ""}. An octave up, {oct_up.name} is {hz(oct_up.hz)} Hz.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="keys-title">
    <div class="wrap">
      <h2 id="keys-title">Keys that use {note.letter}</h2>
      <p class="intro">An 808 usually plays the root of the key, and often the fifth. These are the keys where {note.letter} is in the scale, with the root and fifth first. Camelot codes are for DJ mixing and key detectors.</p>
      <div class="table-scroll">
      <table class="data" style="max-width:760px">
        <thead><tr><th scope="col">Key</th><th scope="col">Camelot</th><th scope="col">{note.letter} is the</th></tr></thead>
        <tbody>
""")
    for degree, key, cam in keys_with(note):
        here = ' class="is-here"' if degree in (0, 4) else ""
        out.append(f'          <tr{here}><th scope="row">{esc(key)}</th><td>{cam}</td><td>{DEGREES[degree]}</td></tr>\n')
    out.append(f"""        </tbody>
      </table>
      </div>
      <p class="fineprint">Natural minor and major scales. Highlighted rows: {note.letter} is the root or the fifth.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="kick-title">
    <div class="wrap prose">
      <h2 id="kick-title">Tuning the kick to {note.article} {note.name} 808</h2>
      <p>A kick has a pitch too: the low tone it settles on after the click. When that tone matches the 808, or sits a fifth away, the two blend instead of clashing. With an 808 on {note.name}, that means a kick that settles on {note.letter}, or on {fifth.letter} ({fifth.name} is {hz(fifth.hz)} Hz, {fourth_below.name} is {hz(fourth_below.hz)} Hz).</p>
      <h3>The timing that cancels it out</h3>
      <p>One cycle of {note.name} lasts {ms(note.cycle_ms)} ms. If a kick at the same pitch starts half a cycle, <strong>{ms(half)} ms</strong>, before or after the 808, the two waves push in opposite directions and the low end drops away. Line them up within a millisecond or two and they add up instead. <a href="../../kick-808-phase/">Try it in the phase demo</a>, or see it on your own track with <a href="../../../smartscope/">Smartscope</a>.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="more-title">
    <div class="wrap">
      <h2 id="more-title">Other notes</h2>
      <div class="cards" style="margin-top:20px">
        <a class="card" href="{note_link(down, '../')}"><strong>{down.name}</strong><span>{hz(down.hz)} Hz, one note down</span></a>
        <a class="card" href="{note_link(up1, '../')}"><strong>{up1.name}</strong><span>{hz(up1.hz)} Hz, one note up</span></a>
        <a class="card" href="../"><strong>All 808 notes</strong><span>The full chart, C0 to B2</span></a>
        <a class="card" href="../../kick-808-phase/"><strong>Kick and 808 phase</strong><span>Why they cancel, with a live demo</span></a>
      </div>
    </div>
  </section>
""")
    out.append(pitchscope_panel(3, note))
    out.append("</main>\n")
    out.append(footer(3))
    return "".join(out)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path)


if __name__ == "__main__":
    write("guides/808-notes/index.html", chart_page())
    for name in PUBLISH:
        n = note_from_name(name)
        write(f"guides/808-notes/{n.slug}/index.html", note_page(n))
