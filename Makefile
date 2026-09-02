# Vietnamese master's thesis — Markdown -> Pandoc -> .docx -> Google Docs.
#
#   make docx                     whole thesis  -> build/thesis.docx
#   make chapter CH=02-litreview  one chapter   -> build/02-litreview.docx
#   make push    CH=02-litreview  build + upload to Google Drive as a Google Doc
#   make doctor                   check what is installed / configured
#   make help                     all targets
#
# Requires: pandoc. Optional, only for `make push`: rclone.

PANDOC      ?= pandoc
BUILD       ?= build
CHAPTER_DIR ?= chapters
ASSET_DIR   ?= assets
METADATA    ?= metadata.yaml
BIB         ?= references.bib
REFDOC      ?= reference.docx
THESIS      ?= thesis
FONT        ?= Times New Roman

# Chapters in filename order. The NN- prefixes make sort order = reading order.
CHAPTERS := $(sort $(wildcard $(CHAPTER_DIR)/*.md))

PANDOC_OPTS := \
	--from=markdown \
	--to=docx \
	--standalone \
	--citeproc \
	--metadata-file=$(METADATA) \
	--resource-path=.:$(ASSET_DIR)

# Use the faculty style template only when that file is actually present.
# Expands to nothing when absent, so it is also a no-op as a prerequisite.
REFDOC_PRESENT := $(wildcard $(REFDOC))
ifneq ($(REFDOC_PRESENT),)
PANDOC_OPTS += --reference-doc=$(REFDOC)
endif

.PHONY: all docx chapter push clean list doctor reference-docx help
.DEFAULT_GOAL := docx

all: docx

# ---- Build ----------------------------------------------------------------

docx: $(BUILD)/$(THESIS).docx

# Whole thesis: every chapter concatenated, in order, in one pandoc run.
$(BUILD)/$(THESIS).docx: $(CHAPTERS) $(METADATA) $(BIB) $(REFDOC_PRESENT) | $(BUILD)
	@echo "==> whole thesis -> $@"
	$(PANDOC) $(PANDOC_OPTS) -o $@ $(CHAPTERS)

# Single chapter. Explicit rule above wins for thesis.docx, so no clash.
$(BUILD)/%.docx: $(CHAPTER_DIR)/%.md $(METADATA) $(BIB) $(REFDOC_PRESENT) | $(BUILD)
	@echo "==> chapter -> $@"
	$(PANDOC) $(PANDOC_OPTS) -o $@ $<

$(BUILD):
	@mkdir -p $@

chapter:
	@test -n "$(CH)" || { echo "Usage: make chapter CH=<name>   e.g. make chapter CH=02-litreview"; echo; $(MAKE) -s list; exit 1; }
	@test -f "$(CHAPTER_DIR)/$(CH).md" || { echo "No such chapter: $(CHAPTER_DIR)/$(CH).md"; echo; $(MAKE) -s list; exit 1; }
	@$(MAKE) -s $(BUILD)/$(CH).docx

# ---- Upload ---------------------------------------------------------------

push:
	@test -n "$(CH)" || { echo "Usage: make push CH=<name>   (use CH=$(THESIS) for the whole thesis)"; echo; $(MAKE) -s list; exit 1; }
	@if [ "$(CH)" = "$(THESIS)" ]; then $(MAKE) -s docx; else $(MAKE) -s chapter CH=$(CH); fi
	@scripts/upload.sh "$(BUILD)/$(CH).docx"

# ---- Utilities ------------------------------------------------------------

# Generate a starter reference.docx using a font with full Vietnamese coverage.
# Refuses to clobber an existing reference.docx (e.g. your faculty's template).
reference-docx:
	@FONT="$(FONT)" scripts/make-reference-docx.sh "$(REFDOC)"

list:
	@echo "Chapters (pass the name without .md as CH=):"
	@for f in $(CHAPTERS); do echo "   $$(basename $$f .md)"; done
	@echo "   $(THESIS)  <- the whole thesis"

doctor:
	@echo "Dependencies"
	@printf '  pandoc          : '; if command -v $(PANDOC) >/dev/null 2>&1; then $(PANDOC) --version | head -1; else echo "MISSING  -> brew install pandoc"; fi
	@printf '  rclone          : '; if command -v rclone >/dev/null 2>&1; then rclone version | head -1; else echo "missing (only needed for make push)  -> brew install rclone"; fi
	@echo "Configuration"
	@printf '  .upload.env     : '; if [ -f .upload.env ]; then echo "present"; else echo "absent  -> cp .upload.env.example .upload.env"; fi
	@printf '  rclone remote   : '; \
		if ! command -v rclone >/dev/null 2>&1; then echo "n/a (rclone not installed)"; \
		else r=$$( [ -f .upload.env ] && . ./.upload.env; echo "$$RCLONE_REMOTE" ); \
		  if [ -z "$$r" ]; then echo "no RCLONE_REMOTE set in .upload.env"; \
		  elif rclone listremotes | grep -qx "$$r:"; then echo "'$$r:' configured"; \
		  else echo "'$$r:' NOT configured  -> rclone config"; fi; fi
	@printf '  reference.docx  : '; if [ -f $(REFDOC) ]; then echo "present (will be used for styling)"; else echo "absent (pandoc default styling)  -> make reference-docx"; fi

clean:
	@rm -rf $(BUILD)
	@echo "Removed $(BUILD)/"

help:
	@echo "make docx                     build the whole thesis  -> $(BUILD)/$(THESIS).docx"
	@echo "make chapter CH=02-litreview  build one chapter       -> $(BUILD)/02-litreview.docx"
	@echo "make push    CH=02-litreview  build that chapter, upload as a Google Doc"
	@echo "make push    CH=$(THESIS)        build + upload the whole thesis"
	@echo "make reference-docx           create a starter reference.docx (font: $(FONT))"
	@echo "make list                     list chapter names usable as CH="
	@echo "make doctor                   report missing dependencies / config"
	@echo "make clean                    delete $(BUILD)/"
