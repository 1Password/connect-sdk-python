export MAIN_BRANCH ?= main

.DEFAULT_GOAL := help
.PHONY: test build release/prepare release/tag .check_git_clean help

GIT_BRANCH := $(shell git symbolic-ref --short HEAD)
WORKTREE_CLEAN := $(shell git status --porcelain 1>/dev/null 2>&1; echo $$?)
SCRIPTS_DIR := $(CURDIR)/scripts

POETRY := $(shell command -v poetry 2>/dev/null)
ifndef POETRY
	$(error "poetry not found on system. Install 'poetry' before continuing.")
endif

curVersion = $(shell poetry version -s)

test:	## Run test suite
	@poetry run pytest


build: clean	## Build project
	@poetry build --format sdist

clean:	## Remove build artifacts
	@rm -rf dist .eggs *.egg-info

help:	## Prints this help message
	@grep -E '^[\/a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


## Release functions =====================

release/prepare: ##.check_git_clean	## Bumps version and creates release branch (call with 'release/prepare version=<semver>')

	@test $(version) || (echo "[ERROR] version argument not set."; exit 1)
	@git fetch --quiet origin $(MAIN_BRANCH)

	@poetry version $(shell echo $(version) | sed "s/^v//")

	@NEW_VERSION=$(version) $(SCRIPTS_DIR)/prepare-release.sh


release/tag: .check_git_clean	## Creates git tag using version from package.json
	@git pull --ff-only
	@echo "Applying tag 'v$(curVersion)' to HEAD..."
	@git tag --sign "v$(curVersion)" -m "Release v$(curVersion)"
	@echo "[OK] Success!"
	@echo "Remember to call 'git push --tags' to persist the tag."

## Helper functions =====================

.check_git_clean:
ifneq ($(GIT_BRANCH), $(MAIN_BRANCH))
	@echo "[ERROR] Please checkout default branch '$(MAIN_BRANCH)' and re-run this command."; exit 1;
endif
ifneq ($(WORKTREE_CLEAN), 0)
	@echo "[ERROR] Uncommitted changes found in worktree. Address them and try again."; exit 1;
endif

