#!/usr/bin/env bash
# Build the Eclipse Zenoh Marp decks into a publishable site directory.
#
# Usage (run from the repository root):
#   presentation/build.sh [output_dir]
#
# The output directory mirrors the repo layout so each deck's relative
# "../assets/..." image paths (and the SVG animations) resolve no matter which
# sub-path the site is served from:
#
#   <output_dir>/index.html               -> redirect to presentation/
#   <output_dir>/presentation/index.html  -> the main deck (zenoh.md)
#   <output_dir>/presentation/zenoh.pptx  -> downloadable PowerPoint export
#   <output_dir>/presentation/pitch.html  -> the 2-slide pitch deck (pitch.md)
#   <output_dir>/presentation/pitch.pptx  -> downloadable PowerPoint export
#   <output_dir>/assets/...               -> diagrams and logos
#
# The PowerPoint export renders each slide via headless Chrome, so a Chrome or
# Chromium binary must be available (GitHub's ubuntu runners ship one; locally
# Marp auto-detects Google Chrome / Chromium / Edge).
set -euo pipefail

OUT="${1:-_site}"
MARP_VERSION="4.4.0"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

rm -rf "$OUT"
mkdir -p "$OUT/presentation"
cp -r assets "$OUT/assets"

npx --yes "@marp-team/marp-cli@${MARP_VERSION}" presentation/zenoh.md \
  -o "$OUT/presentation/index.html"

# PowerPoint export. --allow-local-files lets the headless browser read the
# relative "../assets/..." images while rendering each slide.
npx --yes "@marp-team/marp-cli@${MARP_VERSION}" presentation/zenoh.md \
  --pptx --allow-local-files \
  -o "$OUT/presentation/zenoh.pptx"

npx --yes "@marp-team/marp-cli@${MARP_VERSION}" presentation/pitch.md \
  -o "$OUT/presentation/pitch.html"

npx --yes "@marp-team/marp-cli@${MARP_VERSION}" presentation/pitch.md \
  --pptx --allow-local-files \
  -o "$OUT/presentation/pitch.pptx"

cat > "$OUT/index.html" <<'EOF'
<!doctype html>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=./presentation/">
<link rel="canonical" href="./presentation/">
<title>Eclipse Zenoh presentation</title>
<a href="./presentation/">Eclipse Zenoh presentation</a>
EOF

echo "Built deck into $OUT"
