#!/usr/bin/env bash
#
# Upload a built .docx to Google Drive AND convert it to a native Google Doc,
# so the advisor can comment on it directly.
#
#   scripts/upload.sh build/02-litreview.docx
#
# Configuration lives in .upload.env at the repo root (gitignored):
#   RCLONE_REMOTE=gdrive
#   DRIVE_FOLDER=Thesis
#
# If rclone is missing or unconfigured, this prints manual upload instructions
# and exits non-zero. It never claims an upload happened when it did not.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FILE="${1:-}"

die() { printf '%s\n' "$*" >&2; exit 1; }

manual_fallback() {
  cat >&2 <<EOF

--------------------------------------------------------------------
Automatic upload unavailable: $1

The document itself built fine:
    $FILE

Upload it by hand (~30 seconds):
  1. Open https://drive.google.com
  2. Drag $(basename "$FILE") into the folder you share with your advisor.
  3. Right-click the uploaded file -> "Open with" -> "Google Docs".
     That produces a native, commentable Google Doc.

  Tip: Drive -> Settings -> General -> tick "Convert uploaded files to
  Google Docs editor format" makes step 3 automatic in future.

To enable automatic upload, see "One-time Drive setup" in README.md.
--------------------------------------------------------------------
EOF
  exit 1
}

[ -n "$FILE" ] || die "Usage: scripts/upload.sh <path-to-.docx>"
[ -f "$FILE" ] || die "No such file: $FILE  (run 'make docx' or 'make chapter CH=...' first)"

# shellcheck source=/dev/null
[ -f "$ROOT/.upload.env" ] && . "$ROOT/.upload.env"

REMOTE="${RCLONE_REMOTE:-}"
FOLDER="${DRIVE_FOLDER:-}"

command -v rclone >/dev/null 2>&1 || manual_fallback "rclone is not installed"
[ -n "$REMOTE" ] || manual_fallback "RCLONE_REMOTE is not set (no .upload.env yet)"
rclone listremotes | grep -qx "${REMOTE}:" \
  || manual_fallback "rclone remote '${REMOTE}:' is not configured (run: rclone config)"

DEST="${REMOTE}:${FOLDER}"
NAME="$(basename "$FILE")"
STEM="${NAME%.docx}"

echo "Uploading $NAME -> $DEST  (converting to Google Docs format)"

# --drive-import-formats docx makes rclone convert an uploaded .docx into a
# native Google Doc rather than storing it as a raw file.
rclone copy "$FILE" "$DEST" --drive-import-formats docx

# Find what Drive actually named the result. rclone's docs do not state whether
# the .docx extension survives conversion, so accept either form.
#   lsf --format p=path  i=ID  m=MimeType
line="$(rclone lsf "$DEST" --files-only --format "pim" --separator "|" 2>/dev/null \
        | awk -F'|' -v a="$NAME" -v b="$STEM" '$1==a || $1==b { print; exit }')" || true

if [ -z "$line" ]; then
  echo
  echo "Uploaded, but could not find the file back in $DEST to build a link."
  echo "Check the folder at https://drive.google.com"
  exit 0
fi

name="${line%%|*}"
rest="${line#*|}"
id="${rest%%|*}"
mime="${rest#*|}"

echo
if [ "$mime" = "application/vnd.google-apps.document" ]; then
  echo "Google Doc ready: $name"
  echo "  https://docs.google.com/document/d/${id}/edit"
else
  echo "Uploaded '$name', but it is NOT a native Google Doc (type: $mime)."
  echo "  Open it in Drive and choose 'Open with -> Google Docs',"
  echo "  or check that --drive-import-formats is supported for this remote."
  echo "  https://drive.google.com/file/d/${id}/view"
fi

echo
echo "File ID: $id"
echo "If this ID matches the previous push, your advisor's existing link and"
echo "comments still point at this same document."
