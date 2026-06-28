# Eclipse Zenoh — presentation

A [Marp](https://marp.app/) slide deck introducing Eclipse Zenoh and its core
concepts. The source is a single Markdown file, [`zenoh.md`](zenoh.md), with the
theme embedded in a `<style>` block so it stays self-contained.

The deck reuses the diagrams from [`../assets`](../assets) — the
publish/subscribe and query/reply slides embed the **animated** SVGs, which play
when the deck is rendered to **HTML** and opened in a browser.

## Live deck

The deck is published to GitHub Pages from the **`gh-pages`** branch:

- **Main:** <https://zettascalelabs.github.io/Cagliari2026/>
- **Per-PR preview:** `https://zettascalelabs.github.io/Cagliari2026/pr-preview/pr-<N>/`

Two workflows keep this up to date:

- [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) — on every push
  to `main` that touches `presentation/` or `assets/`, it rebuilds the deck and
  publishes it to the site root. It keeps the `pr-preview/` folder intact
  (`clean-exclude`), so open previews survive a main deploy.
- [`.github/workflows/pr-preview.yml`](../.github/workflows/pr-preview.yml) — for
  every pull request that changes `presentation/` or `assets/`, it builds the
  deck and deploys it to `pr-preview/pr-<N>/`, posts a sticky comment with the
  link, and removes the folder when the PR is closed.

Both build with [`build.sh`](build.sh), which renders HTML only (no headless
browser) and copies `assets/` alongside the deck so the relative image paths and
SVG animations keep working under any sub-path.

Setup notes:

- One-time: set **Settings -> Pages -> Source** to **Deploy from a branch**,
  branch **`gh-pages`** / **`/ (root)`**. The first `pages.yml` run creates the
  branch.
- Previews run for same-repo PR branches. Pull requests from **forks** get a
  read-only token, so their preview job is skipped (switch to a
  `pull_request_target` flow if fork previews are needed).

## Build

Build the full publishable site (deck + assets + redirect) exactly like CI, from
the repository root:

```sh
bash presentation/build.sh _site   # output in ./_site
```

Or work with the deck directly. Run these from this `presentation/` directory so
the relative `../assets/...` paths resolve.

```sh
# Interactive preview with live reload (opens in the browser, animations play)
npx @marp-team/marp-cli@latest -p -w zenoh.md

# HTML (recommended — SVG animations play)
npx @marp-team/marp-cli@latest zenoh.md -o zenoh.html

# PDF (static; --allow-local-files is required to embed the local assets)
npx @marp-team/marp-cli@latest zenoh.md --allow-local-files -o zenoh.pdf

# PNG per slide
npx @marp-team/marp-cli@latest zenoh.md --images png --allow-local-files
```

You can also use the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
extension to preview and export `zenoh.md` directly.

## Outline

1. Title — Eclipse Zenoh
2. What is Zenoh
3. Key Expressions
4. Config
5. Session
6. Publish / Subscribe
7. Get / Reply
8. Sample
9. Selector
10. Matching
11. Consolidation
12. Reply
13. Liveliness
14. Serialization
15. Advanced Pub/Sub
16. Language bindings
17. Links
