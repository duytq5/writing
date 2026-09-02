#!/usr/bin/env bash
#
# Create a starter reference.docx whose body and heading fonts have full
# Vietnamese coverage.
#
#   make reference-docx                    # uses Times New Roman
#   FONT="Arial" make reference-docx       # or pick another font
#
# Pandoc's built-in template uses "Aptos", which is not installed on most Macs
# and is not offered by Google Docs, so it gets font-substituted. Substitution
# usually still renders Vietnamese, but pinning a known-good font removes the
# guesswork. This is only a fallback: if your faculty supplies a template, put
# it at reference.docx and this script will refuse to overwrite it.

set -euo pipefail

OUT="${1:-reference.docx}"
FONT="${FONT:-Times New Roman}"

for tool in pandoc unzip zip; do
  command -v "$tool" >/dev/null 2>&1 || { echo "Required tool not found: $tool" >&2; exit 1; }
done

if [ -e "$OUT" ]; then
  echo "Refusing to overwrite the existing $OUT" >&2
  echo "If that is your faculty's template, keep it as-is." >&2
  echo "To regenerate anyway:  rm $OUT && make reference-docx" >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

pandoc --print-default-data-file reference.docx > "$tmp/base.docx"
unzip -q "$tmp/base.docx" -d "$tmp/x"

theme="$tmp/x/word/theme/theme1.xml"
[ -f "$theme" ] || { echo "Unexpected: no word/theme/theme1.xml in pandoc's template" >&2; exit 1; }

# word/styles.xml binds body and heading text through the theme
# (w:asciiTheme="minorHAnsi" / "majorHAnsi"), so replacing the theme's Latin
# typefaces changes both. Written to a temp file rather than sed -i, because
# BSD and GNU sed disagree about -i's argument.
sed -E 's|<a:latin[^/]*/>|<a:latin typeface="'"$FONT"'"/>|g' "$theme" > "$theme.new"
mv "$theme.new" "$theme"

( cd "$tmp/x" && zip -q -r -X "$tmp/out.docx" . )
mv "$tmp/out.docx" "$OUT"

echo "Created $OUT  (body and heading font: $FONT)"
echo "It will be picked up automatically on the next build."
