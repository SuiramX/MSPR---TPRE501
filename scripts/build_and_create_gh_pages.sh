chmod +x "$ROOT_DIR/scripts/build_and_create_gh_pages.sh" 2>/dev/null || true
#!/usr/bin/env bash
set -euo pipefail

# Build MkDocs site and create a gh-pages worktree with the built site

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f requirements.txt ]; then
  echo "requirements.txt not found; aborting"
  exit 1
fi

python3 -m venv .venv_mkdocs
source .venv_mkdocs/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

mkdocs build -d site

# Use a git worktree for gh-pages to avoid disturbing current branch
WT_DIR="${ROOT_DIR}/site-gh-pages"
if git show-ref --verify --quiet refs/heads/gh-pages; then
  echo "Updating existing gh-pages worktree..."
  rm -rf "$WT_DIR"
  git worktree add -B gh-pages "$WT_DIR"
else
  echo "Creating new gh-pages worktree..."
  git worktree add -B gh-pages "$WT_DIR"
fi

rm -rf "$WT_DIR"/*
cp -r site/* "$WT_DIR/"

cd "$WT_DIR"
git add -A
if git diff --staged --quiet; then
  echo "No changes to commit in gh-pages worktree."
else
  git commit -m "gh-pages: deploy MkDocs site"
fi

cd "$ROOT_DIR"
echo "Done — gh-pages branch available in 'site-gh-pages' worktree." 
