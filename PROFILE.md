# Profile maintenance

This profile belongs to **Srivaths**, GitHub handle `sriv144`. The current README contains a cozy illustrated header, two autoplay arcade scenes, a toolbox, and interest areas. The terminal and selected-project gallery have been removed from the displayed profile.

## Preview

```powershell
python scripts/preview.py
```

Open http://127.0.0.1:8765/. The helper renders the canonical README using GitHub’s Markdown API. Its light/dark and pause controls are local review tools. On GitHub, the images have static sources and embedded reduced-motion rules.

## Artwork

`assets/cozy-workspace.png` is an original illustration generated using the built-in image-generation tool. Its back-view character is illustrative, with no claim of matching a real facial likeness. The exact prompt is recorded in `assets/cozy-workspace.prompt.txt`.

`scripts/generate-arcade.py` wraps the artwork in a self-contained SVG with gentle star, firefly, and steam animation. It also renders Commit Cosmos from the real daily cells preserved in the contribution snake assets.

```powershell
python scripts/generate-arcade.py
python scripts/generate-arcade.py --check
```

The grouped toolbox is generated with `python scripts/generate-toolbox.py` (or `--check`). It has dark/light and desktop/mobile compositions, uses local vector symbols, and stays still while the header and arcade animate.

The generator uses Python’s standard library. The space-only workflow mode avoids rebuilding the header on daily runs.

## Contribution games

Both scenes are autoplay animations inside README images. GitHub strips scripts and custom page styles; keyboard-controlled games cannot run inside the README.

The workflow refreshes the public calendar daily on the default branch: Platane/snk fetches the data, the Node enhancer adds accessibility/static variants, and the Python arcade generator refreshes the space scene. No personal access token is needed. Commit Cosmos uses a synchronized shot/impact timeline: targets flash, burn away after a hit, and reset for the next round. Reduced-motion artwork keeps the full calendar visible.

Older artwork variants are retained in the workspace but are no longer linked from the current README.

## Voice

Keep the copy playful and warm: short coding riffs on Game of Thrones, Stranger Things, Money Heist, How I Met Your Mother, and Marvel. Current examples include the async “Legen—await for it—dary” header, the Professor/commits introduction, the winter/extra-life arcade line, the friends/contribution-graph joke, and the Avengers/toolbox line. Adapted jokes are original references, not claims of verbatim character dialogue. Avoid repeating generic curiosity slogans.

## Publishing

The profile is published from the root README.md on the default branch of the public `sriv144/sriv144` repository. The daily animation workflow supports a manual refresh from GitHub Actions as well.

## Inspiration

- [Awesome Github Profile gallery](https://zzetao.github.io/awesome-github-profile/)
- [Awesome profile README animation reference](https://github.com/abhisheknaiidu/awesome-github-profile-readme/blob/master/assets/agpr.gif)
- [Contribution snake](https://github.com/Platane/snk)
- [GitHub README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
