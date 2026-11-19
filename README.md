# claeslanng.shop

The website of **Claes Lanng Plugins**: free, open-source VST3 plugins for the low end. It's served by GitHub Pages at [claeslanng.shop](https://claeslanng.shop).

It's plain static HTML with no build step. To change it, edit a file and push to `main`; GitHub Pages updates the live site within a minute or two.

- `index.html`: the home page, linking to each plugin.
- `smartscope/`, `pitchscope/`, `flow-fmx-host/`: one page per plugin, each in that plugin's own colours.
- `assets/site.css`: shared styles and the colour themes. `assets/scope.js`: the animated oscilloscope on the home page.
- `CNAME`: the custom domain. Keep this file.
- `assets/img/`: plugin screenshots, one folder per plugin.
- `assets/fonts/`: Archivo and Archivo Narrow, under the SIL Open Font License (`OFL.txt`).

Preview it locally with `python3 -m http.server`, then open http://localhost:8000.
