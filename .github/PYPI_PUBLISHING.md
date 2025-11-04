# PyPI Publishing Guide

This guide explains how to publish the `prettyplot` package to PyPI using GitHub Actions and `uv`.

## Overview

The project includes two GitHub Actions workflows:

1. **`publish-to-pypi.yml`**: Publishes to production PyPI when a release is created
2. **`publish-to-test-pypi.yml`**: Publishes to Test PyPI for testing (manual trigger or test tags)

Both workflows use `uv` for building the package and the official PyPI publish action.

## Setup Instructions

### Option 1: Trusted Publishing (Recommended)

Trusted publishing is the modern, secure way to publish to PyPI without managing API tokens.

#### Steps:

1. **Create a PyPI account** (if you don't have one):
   - Go to https://pypi.org/account/register/

2. **Configure Trusted Publisher on PyPI**:
   - Go to https://pypi.org/manage/account/publishing/
   - Click "Add a new pending publisher"
   - Fill in the form:
     - **PyPI Project Name**: `prettyplot`
     - **Owner**: `jorgebotas`
     - **Repository name**: `prettyplot`
     - **Workflow name**: `publish-to-pypi.yml`
     - **Environment name**: (leave blank or use `release`)
   - Click "Add"

3. **Configure Test PyPI (optional but recommended)**:
   - Go to https://test.pypi.org/manage/account/publishing/
   - Repeat the same process with workflow name: `publish-to-test-pypi.yml`

That's it! No API tokens needed.

### Option 2: API Token (Alternative)

If you prefer using API tokens:

1. **Create a PyPI API token**:
   - Go to https://pypi.org/manage/account/token/
   - Create a token with "Entire account" scope (or project scope after first upload)
   - Copy the token (starts with `pypi-`)

2. **Add token to GitHub Secrets**:
   - Go to your GitHub repository settings
   - Navigate to: Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token
   - Click "Add secret"

3. **Update the workflow**:
   - Modify `.github/workflows/publish-to-pypi.yml`
   - Replace the publish step with:
     ```yaml
     - name: Publish to PyPI
       uses: pypa/gh-action-pypi-publish@release/v1
       with:
         password: ${{ secrets.PYPI_API_TOKEN }}
         packages-dir: dist/
     ```

## Publishing a New Version

### 1. Update the Version Number

Edit `pyproject.toml` and update the version:

```toml
[project]
name = "prettyplot"
version = "0.1.0"  # Change this to your new version
```

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.2.0): New functionality, backwards-compatible
- **PATCH** version (0.1.1): Backwards-compatible bug fixes

### 2. Commit and Push Changes

```bash
git add pyproject.toml
git commit -m "Bump version to 0.1.0"
git push origin main
```

### 3. Create a GitHub Release

#### Option A: Via GitHub Web Interface

1. Go to your repository on GitHub
2. Click on "Releases" (right sidebar)
3. Click "Create a new release"
4. Click "Choose a tag" and type a new tag (e.g., `v0.1.0`)
5. Click "Create new tag: v0.1.0 on publish"
6. Fill in:
   - **Release title**: `v0.1.0`
   - **Description**: Describe what's new
7. Click "Publish release"

#### Option B: Via Git Command Line

```bash
# Create and push a tag
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# Then create the release on GitHub
```

### 4. Monitor the Workflow

1. Go to the "Actions" tab in your GitHub repository
2. Watch the "Publish to PyPI" workflow run
3. If successful, your package will be live on PyPI!

## Testing Before Publishing

### Test on Test PyPI First

Before publishing to production PyPI, test on Test PyPI:

1. **Create a test tag**:
   ```bash
   git tag -a v0.1.0-test -m "Test release"
   git push origin v0.1.0-test
   ```

2. **Or trigger manually**:
   - Go to Actions → "Publish to Test PyPI" → "Run workflow"

3. **Install from Test PyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ prettyplot
   ```

4. **Test the installation** to make sure everything works

### Local Testing

Test building the package locally:

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Build the package
uv build

# Check the dist/ directory
ls -lh dist/

# Install locally and test
uv pip install dist/prettyplot-0.1.0-py3-none-any.whl
```

## Workflow Features

### What the Workflows Do

Both workflows:
1. ✅ Checkout the code
2. ✅ Install `uv` (fast Python package manager)
3. ✅ Set up Python 3.11
4. ✅ Install dependencies (including test dependencies)
5. ✅ Run tests with coverage
6. ✅ Build the package using `uv build`
7. ✅ Publish to PyPI/Test PyPI

### Triggers

- **Production workflow**: Runs when you publish a GitHub release
- **Test workflow**: Runs on tags like `v*-test` or manual trigger
- Both support **manual trigger** via workflow_dispatch

### Manual Trigger

To manually trigger a workflow:
1. Go to Actions tab
2. Select the workflow
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

## Troubleshooting

### "Invalid or non-existent authentication information"

- Make sure trusted publishing is set up correctly on PyPI
- Or ensure your API token is valid and added to GitHub secrets

### "Project name already exists"

- The package name might be taken on PyPI
- Check https://pypi.org/project/prettyplot/
- Consider a different name in `pyproject.toml`

### Tests failing

- The workflow won't publish if tests fail
- Check the test output in the Actions log
- Fix tests and try again

### Build fails

- Check that `pyproject.toml` is valid
- Ensure all required files are committed
- Check the build log for details

## Version Management Best Practices

1. **Keep `pyproject.toml` version in sync** with your Git tags
2. **Document changes** in the GitHub release notes
3. **Test on Test PyPI first** for major releases
4. **Use pre-release versions** for testing: `0.1.0-alpha`, `0.1.0-beta`, `0.1.0-rc1`
5. **Never delete releases** from PyPI (they're permanent)

## Resources

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Semantic Versioning](https://semver.org/)
- [Python Packaging Guide](https://packaging.python.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Quick Reference

```bash
# Update version in pyproject.toml, then:

# Commit changes
git add pyproject.toml
git commit -m "Bump version to X.Y.Z"
git push origin main

# Create release tag
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z

# Or create release on GitHub web interface
# → GitHub Actions will automatically publish to PyPI
```
