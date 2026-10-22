# Maintaining this profile

The profile content lives in `README.md`. The graphics are repository-owned SVG files, so the header does not depend on a third-party image service.

## Preview locally

```powershell
python scripts/preview.py
```

Open http://127.0.0.1:8765/. The helper renders the actual README with GitHub’s Markdown API, then serves a local review canvas. It needs an internet connection for rendering; `GH_TOKEN` is optional. Dark, light, and motion controls belong to the local preview. GitHub applies its own page layout.

The hero uses desktop/mobile `<picture>` sources, light/dark variants, and embedded reduced-motion CSS. The contribution snake is collapsed by default; close its section to hide it.

## Regenerate graphics

```powershell
python scripts/generate-hero.py
```

The contribution workflow refreshes real public contribution data daily and supports a manual run from the Actions tab. It uses the built-in `GITHUB_TOKEN`; no personal access token is required. Its generated files are committed to the default branch.

## Make it appear on GitHub

GitHub displays this README on `https://github.com/sriv144` when the repository is named `sriv144`, is public, and has this README on its default branch. Changing a private repository to public also exposes its Git history. Review the complete repository before changing visibility.

## Profile settings to finish

Suggested bio:

> Building AI and data systems · agents, retrieval, robotics & infrastructure · Python / TypeScript

Suggested pins, in order:

1. FinLens
2. embodied-skill-composer
3. Autonomous-SRE-Agent
4. AegisQuant
5. tds-iitm
6. RSA-Vulnerability-Analyzer

Add your preferred public contact and portfolio links in GitHub’s profile settings. The README intentionally uses only verified public project links.

## Design and content sources

- [GitHub profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [GitHub picture and theme support](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#the-picture-element)
- [Contribution animation generator](https://github.com/Platane/snk)
- [Original video reference](https://www.youtube.com/watch?v=J9ZpaKM0Yqs) — title available; transcript unavailable during this work.
