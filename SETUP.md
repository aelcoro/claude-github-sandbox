# Setup guide: push to GitHub & connect Claude

This guide walks through getting the sandbox onto GitHub and wiring Claude up to it.

## 1. Initialize the local repo

From inside the `claude-github-sandbox/` folder:

```bash
git init
git add .
git commit -m "Initial commit: Python sandbox for Claude + GitHub"
git branch -M main
```

## 2. Create the GitHub repository

Pick **one** of the options below.

### Option A — GitHub CLI (fastest)

Requires [`gh`](https://cli.github.com/) and a logged-in session (`gh auth login`).

```bash
gh repo create claude-github-sandbox --public --source=. --remote=origin --push
```

That single command creates the remote repo and pushes `main` to it.

### Option B — GitHub web UI

1. Visit https://github.com/new
2. Repository name: `claude-github-sandbox`
3. Keep it **empty** (no README, .gitignore, or license — you already have them locally)
4. Click **Create repository**
5. On your terminal, wire up the remote and push:

   ```bash
   git remote add origin https://github.com/<your-username>/claude-github-sandbox.git
   git push -u origin main
   ```

## 3. Verify

```bash
gh repo view --web     # opens the new repo in your browser
# or just visit https://github.com/<your-username>/claude-github-sandbox
```

You should see `src/`, `tests/`, the README, etc.

## 4. Connect Claude to the repository

Since this is a sandbox repo, here are the main ways to get Claude involved.

### a) Add the Claude GitHub connector (simplest)

From claude.ai or the Claude desktop app:

1. Open **Settings → Connectors** (or **Settings → Integrations**, depending on your plan)
2. Add the **GitHub** connector and authorize it for your account / the repo's owning org
3. Grant access to `claude-github-sandbox` (or all repos)
4. In a new Claude conversation, mention the repo by name or URL and ask things like:
   - "Summarize the structure of `claude-github-sandbox`."
   - "List the open issues."
   - "Suggest improvements to `src/calculator.py`."

### b) Install the Claude Code GitHub App (for `@claude` mentions)

If you want to test the `@claude` bot pattern (Claude responding on issues / PRs):

1. Install the Claude Code app from the GitHub Marketplace and grant it access to `claude-github-sandbox`
2. In the repo, add your `ANTHROPIC_API_KEY` as a repository secret (`Settings → Secrets and variables → Actions`)
3. Add a workflow file at `.github/workflows/claude.yml` that runs the official action on issue/PR comments — the app's setup flow will typically offer to commit this for you
4. Open an issue and comment `@claude please add a docstring to the average() function` to verify it works

Exact instructions can change — use Anthropic's current docs at https://docs.claude.com as the source of truth.

### c) Just chat with Claude locally about the code

No integration required. Open Cowork mode (or Claude Code in a terminal), point it at the cloned folder, and iterate. This is the lowest-friction way to test Claude against the repo.

## 5. Suggested test exercises

Once connected, try these to cover a range of capabilities:

- **Bug hunt**: `average([])` crashes — ask Claude to reproduce, diagnose, and fix with a test.
- **Feature add**: ask Claude to add `power(base, exp)` + tests and open a PR.
- **Code review**: make a small change yourself, open a PR, and ask Claude to review it.
- **Docs**: ask Claude to generate a proper `CONTRIBUTING.md`.
- **CI**: ask Claude to add a GitHub Actions workflow that runs `pytest` on every push.

Happy testing.
