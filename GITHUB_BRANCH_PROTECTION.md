# GitHub Branch Protection Configuration Guide

## 📋 How to Set Up Branch Protection Rules

Follow these steps to protect the `main` branch from accidental changes:

### Step 1: Go to Repository Settings
1. Visit: **https://github.com/def-me/vqc-iris-classifier**
2. Click **Settings** (top menu bar)
3. Click **Branches** (left sidebar)

### Step 2: Add Branch Protection Rule
1. Click **Add rule** button
2. In the "Branch name pattern" field, enter: `main`
3. Click **Create**

### Step 3: Configure Protection Settings

#### ✅ Require Pull Request Reviews (Recommended)
- [x] **Require pull request reviews before merging**
  - Number of required reviewers: **1**
  - [x] Require review from code owners
  - [x] Dismiss stale pull request approvals when new commits are pushed

#### ✅ Require Status Checks to Pass (Recommended)
- [x] **Require status checks to pass before merging**
  - [x] Require branches to be up to date before merging
  - Select status checks:
    - `build (3.8)` (Python 3.8)
    - `build (3.9)` (Python 3.9)
    - `build (3.10)` (Python 3.10)
    - `build (3.11)` (Python 3.11)

#### ✅ Require Conversation Resolution (Recommended)
- [x] **Require all conversations on code to be resolved before merging**

#### ✅ Require Code Owner Review (Recommended)
- [x] **Require an approval review from Code Owners**
  - Code owners are defined in: `.github/CODEOWNERS`

#### ✅ Restrict Who Can Push (Optional)
- [x] **Restrict who can push to matching branches**
  - Allow only administrators to push

### Step 4: Save Configuration
1. Scroll down and click **Save changes**
2. You'll see a ✅ indicating the rule is active

## 📊 Expected Configuration

After setup, your `main` branch will have:

```
✅ Require pull requests before merging
   - Require 1 approval
   - Dismiss stale reviews
   - Require code owner review

✅ Require status checks to pass
   - GitHub Actions CI/CD (all Python versions)
   - Require branches to be up to date

✅ Require conversations to be resolved
✅ Restrict pushes to administrators only
```

## 🔄 Workflow with Branch Protection

Once enabled, here's the new workflow:

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes and push**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/my-feature
   ```

3. **Open a Pull Request**
   - Go to GitHub → Pull Requests → New Pull Request
   - Select: `base: main` ← `compare: feature/my-feature`
   - Add description
   - Click **Create Pull Request**

4. **Wait for Checks**
   - GitHub Actions runs automatically
   - Must pass all 4 Python version tests
   - Code owner must approve

5. **Merge to Main**
   - Once all checks pass and approved
   - Click **Merge pull request**
   - Choose merge strategy (usually "Create a merge commit")
   - Delete the feature branch

## 🛡️ Why Branch Protection?

- **Prevents accidental merges** - Requires review before changes reach main
- **Ensures quality** - All CI/CD tests must pass
- **Maintains code owner approval** - Team review required
- **Keeps history clean** - Each merge is a deliberate action
- **Audit trail** - Complete record of who approved what

## ⚙️ Status Check Configuration

Your GitHub Actions workflow (`.github/workflows/ci.yml`) automatically provides:

- ✅ **Python 3.8 tests** - ubuntu-latest
- ✅ **Python 3.9 tests** - ubuntu-latest
- ✅ **Python 3.10 tests** - ubuntu-latest
- ✅ **Python 3.11 tests** - ubuntu-latest
- ✅ **Windows tests** - windows-latest
- ✅ **macOS tests** - macos-latest

All must pass before merging to main.

## 📝 CODEOWNERS File

Located at `.github/CODEOWNERS`:

```
* @def-me
```

This means you (def-me) must approve all PRs. You can modify this to add team members:

```
* @def-me @other-username
tests/ @test-expert
docs/ @doc-writer
```

## 🚀 Quick Reference

| Setting | Value | Purpose |
|---------|-------|---------|
| Pattern | `main` | Protects main branch |
| PR Reviews | 1 | Requires one approval |
| Code Owners | Yes | CODEOWNERS file required |
| Status Checks | All | All CI/CD must pass |
| Stale Reviews | Auto-dismiss | Retest after updates |
| Conversations | Required | Resolve all discussions |
| Push Restriction | Admins only | Only admins can force-push |

## ✅ Verification

After configuring, verify by attempting to push directly to main:

```bash
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test"
git push origin main
```

**Expected result:** ❌ Push fails (not allowed)
**Message:** "Updates were rejected because the push would create a diverging branch"

This confirms branch protection is working!

---

**Next Steps:**
1. Follow the steps above to enable branch protection
2. All future changes go through Pull Requests
3. Keep branch clean and production-ready
4. Enable GitHub Pages for documentation

**Questions?** See [GitHub Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
