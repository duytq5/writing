# Luận văn Thạc sĩ — Markdown → Pandoc → Google Docs

Markdown is the single source of truth. Pandoc turns it into `.docx`, and
rclone uploads that to Google Drive as a native Google Doc so your advisor can
comment on it. No LaTeX anywhere in this pipeline.

## Quick start

```bash
brew install pandoc          # required
make docx                    # -> build/thesis.docx
```

Then fill in `metadata.yaml` (title, author, date — currently blank) and start
writing in `chapters/`.

## The workflow

```
edit chapters/*.md  →  make push CH=02-litreview  →  advisor comments in Google Docs
        ↑                                                        │
        └──────────────── you read the comments ─────────────────┘
```

1. Write in `chapters/`. One Markdown file per chapter.
2. `make push CH=02-litreview` builds *that one chapter* and uploads it as a
   Google Doc. The script prints the document link — send that to your advisor.
3. Your advisor comments in Google Docs (they never touch the Markdown).
4. You read the comments, edit the Markdown source, and run `make push CH=...`
   again to update.

Sending one chapter at a time is the point: your advisor gets a short document
to review instead of the whole thesis, and you don't rebuild everything.

## Commands

| Command | What it does |
|---|---|
| `make docx` | Whole thesis → `build/thesis.docx` |
| `make chapter CH=02-litreview` | One chapter → `build/02-litreview.docx` |
| `make push CH=02-litreview` | Build that chapter, upload as a Google Doc |
| `make push CH=thesis` | Build and upload the whole thesis |
| `make list` | Show the chapter names you can pass as `CH=` |
| `make doctor` | Report what's installed and configured |
| `make reference-docx` | Create a starter Word style template |
| `make clean` | Delete `build/` |

## Layout

```
chapters/         00-abstract.md … 05-conclusion.md  (concatenated in filename order)
references.bib    bibliography — cite with [@key]
assets/           figures; reference them as assets/foo.png
metadata.yaml     title, author, lang: vi — fill this in
reference.docx    optional Word style template (see below)
build/            generated .docx — gitignored
scripts/          upload.sh, make-reference-docx.sh
```

Chapters are ordered by filename, which is why they're numbered. To insert a
chapter between two others, number it accordingly (`02a-...`) or renumber.

## Writing

**Citations.** Put sources in `references.bib`, cite with `[@key]`:

| You write | Renders as |
|---|---|
| `[@devlin2019]` | (Devlin và c.s. 2019) |
| `@devlin2019` | Devlin và c.s. (2019) |
| `[@devlin2019; @nguyen2020phobert]` | (Devlin và c.s. 2019; Nguyen và Nguyen 2020) |
| `[@devlin2019, tr. 4171]` | (Devlin và c.s. 2019, tr. 4171) |

Because `metadata.yaml` sets `lang: vi`, pandoc's citation processor uses the
Vietnamese locale — hence *và c.s.* rather than *et al.*, and `tr.` works as the
page locator. The reference list is generated automatically at the end under
the heading "Tài liệu tham khảo" and only ever lists sources you actually cited.

The default style is Chicago author–date. If your faculty mandates a different
one, download the matching `.csl` file from
<https://github.com/citation-style-language/styles> and add `csl: your-style.csl`
to `metadata.yaml`.

**Figures.** Put the file in `assets/` and reference it from the repo root:

```markdown
![Hình 4.1: Chú thích hình.](assets/so-do.png){width=60%}
```

**Vietnamese.** Everything is UTF-8 end to end; diacritics pass through
unchanged. Just write normally — `ạ ả ấ ầ ẫ ậ ắ ằ ẵ ặ ế ề ể ễ ệ ố ồ ổ ỗ ộ ớ ờ ỡ
ợ ứ ừ ữ ự đ Đ ỳ ỹ ỵ` all round-trip correctly into the `.docx`.

## Word styling (`reference.docx`) — optional

Pandoc controls the look of the `.docx` through a *reference document*. There
isn't one in the repo, so pandoc uses its built-in default. The Makefile picks
one up automatically the moment the file exists — no flag to remember.

- **Your faculty gave you a template?** Save it as `reference.docx` in the repo
  root. Done.
- **Want deterministic fonts?** Run `make reference-docx`. This takes pandoc's
  default template and pins the body and heading font to Times New Roman, the
  usual choice for a Vietnamese thesis. Override with
  `FONT="Arial" make reference-docx`. It refuses to overwrite an existing
  `reference.docx`, so it can't clobber a faculty template.

A note on fonts: pandoc 3.11's default template uses *Aptos*, which does contain
Vietnamese glyphs but isn't installed on most Macs and isn't in Google Docs'
font list, so it gets silently substituted. Your text renders correctly either
way — pinning a font only removes the guesswork about *which* font you get.
Google Docs re-maps fonts on import regardless, so this matters most if you also
hand in a `.docx`.

## One-time Drive setup

Needed only for `make push`. `make docx` and `make chapter` work without it.

```bash
brew install rclone
rclone config
```

In the interactive prompts:

1. `n` for a new remote.
2. **name**: `gdrive`
3. **storage**: `drive` (Google Drive).
4. **client_id** / **client_secret**: leave both blank. This uses rclone's
   shared credentials, which is fine at this volume. (Heavy use can hit rate
   limits; if that happens, create your own OAuth client in Google Cloud
   Console — rclone's prompt links to the instructions.)
5. **scope**: choose full access (`drive`). The narrower `drive.file` scope only
   lets rclone see files it created itself, which means it can't upload into a
   folder you made in the Drive web UI.
6. **root_folder_id**, **service_account_file**: leave blank.
7. **advanced config**: no.
8. **auto config**: yes — this opens your browser for the Google OAuth consent
   screen. Sign in and approve. That is the only manual step, and it's once.
9. **Shared Drive (Team Drive)**: no, unless your university actually uses one.
10. Confirm with `y`, then `q` to quit.

Menu wording and numbering shift slightly between rclone versions, so go by the
option names above rather than the numbers.

Then verify and configure this repo:

```bash
rclone lsd gdrive:                    # should list your Drive folders
cp .upload.env.example .upload.env    # then edit it
make doctor                           # confirms everything is wired up
```

`.upload.env` holds two settings and is gitignored:

```sh
RCLONE_REMOTE=gdrive
DRIVE_FOLDER=Thesis
```

Create that `Thesis` folder in Drive first and share it with your advisor
(Commenter access is enough). Leave `DRIVE_FOLDER` empty to upload to your
Drive root.

**Headless machine?** `rclone authorize "drive"` on a computer with a browser,
then paste the token back. See <https://rclone.org/remote_setup/>.

### How the conversion works

`scripts/upload.sh` runs `rclone copy` with `--drive-import-formats docx`, which
tells Drive to convert the uploaded `.docx` into a native Google Doc rather than
storing it as a raw attachment. The script then looks the file back up to
confirm its MIME type really is `application/vnd.google-apps.document`, and
prints the `docs.google.com` link.

If rclone isn't installed or isn't configured, the script prints manual upload
instructions and exits non-zero. It will not pretend an upload happened.

## Advisor comments coming back

Comments live in Google Docs; they never flow into the Markdown automatically.
The loop is:

1. Advisor comments on the Google Doc.
2. You read them in Drive, and edit the corresponding `chapters/*.md`.
3. `make push CH=...` re-uploads.
4. Resolve the comments in Google Docs once you've addressed them.

**Worth verifying on your first re-push:** whether re-uploading updates the
existing Google Doc in place (advisor's link and comments preserved) or creates
a second copy. `upload.sh` prints the Drive **File ID** after every push —
if the ID is unchanged from the previous push, it updated in place. I could not
test this without your Drive credentials, so check it once on a throwaway
chapter before relying on it.

If it does create duplicates, the reliable habit is to keep one Google Doc per
chapter and paste new content into it manually, or simply send your advisor the
newest link each round.

Note that Google Docs anchors comments to specific text. If you substantially
rewrite a paragraph, comments attached to it may end up orphaned even when the
document updates in place — expected behaviour, not a pipeline bug.

## Requirements

| Tool | Needed for | Install |
|---|---|---|
| pandoc | `make docx`, `make chapter` | `brew install pandoc` |
| rclone | `make push` only | `brew install rclone` |
| make, zip, unzip | already on macOS | — |

Verified against pandoc 3.11 and rclone v1.75.0.
