# Eclipse Zenoh — presentation

A [Marp](https://marp.app/) slide deck introducing Eclipse Zenoh and its core
concepts. The source is a single Markdown file, [`zenoh.md`](zenoh.md), with the
theme embedded in a `<style>` block so it stays self-contained.

The deck reuses the diagrams from [`../assets`](../assets) — the
publish/subscribe and query/reply slides embed the **animated** SVGs, which play
when the deck is rendered to **HTML** and opened in a browser.

## Build

Run the commands from this `presentation/` directory so the relative
`../assets/...` paths resolve.

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
3. Zenoh's advantages
4. Concepts — Key Expressions
5. Concepts — Publish / Subscribe
6. Concepts — Sample
7. Concepts — Get / Reply
8. Concepts — Selector, Reply
9. Concepts — Session
10. Concepts — Liveliness
11. Concepts — Serialization
12. Concepts — Advanced Pub/Sub
