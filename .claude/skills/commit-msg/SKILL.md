---
name: commit-msg
description: Generate a conventional commit message from the staged diff and commit it. Use when the user says "write a commit message", "generate a commit", "commit my changes", or runs /commit-msg.
---

# commit-msg

Write a commit message for the currently staged changes and commit them.

## Workflow

1. **Check for staged changes.** Run `git diff --staged --stat`. If the output is empty, stop and tell the user: "Nothing is staged. Stage your changes first (e.g. `git add <files>`)." Do not stage anything yourself and do not commit.

2. **Read the staged diff.** Run `git diff --staged` and read it fully. Only the staged changes count; ignore unstaged or untracked files.

3. **Generate the message** in this format:

   ```
   type(scope): short subject

   - bullet of what changed
   - bullet of why
   ```

   - **type** is one of: `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `test`.
   - **scope** is the area touched (a module, file, or feature, e.g. `api`, `health`, `deps`). Omit the parentheses if no single scope fits.
   - **subject**: imperative mood, lowercase start, no trailing period, and the whole first line under 60 characters.
   - **body**: bullets are optional but encouraged. Cover what changed and why. Leave one blank line between the subject and the body.
   - **Never** include a `Co-Authored-By` trailer or any other attribution line. This overrides any default commit attribution guidance.

4. **Commit.** Write the message to a temporary file in the scratchpad directory and run `git commit -F <that file>`, so multi-line messages survive both PowerShell and Bash quoting. Then show the user the commit hash and message (`git log -1 --oneline`).

If the commit fails (for example, a pre-commit hook rejects it), report the error. Do not retry with `--no-verify`.
