# Quick Start: Publishing to PyPI

## Before First Publish

1. **Update your email in `pyproject.toml`**:
   ```toml
   authors = [
       {name = "Jorge Botas", email = "your.real.email@example.com"}
   ]
   ```

2. **Review and update `CHANGELOG.md`** with your changes

3. **Test the build locally**:
   ```bash
   # Clean previous builds
   rm -rf dist/

   # Build the package
   uv build

   # Inspect what was built
   ls -lh dist/
   ```

4. **Test install locally**:
   ```bash
   uv pip install dist/prettyplots-*.whl
   python -c "import prettyplots as pp; print(pp.__version__)"
   ```

## Option 1: Automated Publishing (Recommended)

### One-time Setup
1. Go to https://pypi.org/manage/account/publishing/
2. Add a pending publisher with:
   - **PyPI Project Name**: `prettyplots`
   - **Owner**: `jorgebotas`
   - **Repository name**: `prettyplots`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

### Publishing
1. Update version in `pyproject.toml`
2. Commit and push
3. Create a GitHub release with tag `vX.Y.Z`
4. GitHub Actions will automatically publish to PyPI

## Option 2: Manual Publishing with uv

```bash
# 1. Clean and build
rm -rf dist/
uv build

# 2. Test on TestPyPI first (optional but recommended)
uv publish --publish-url https://test.pypi.org/legacy/

# 3. Publish to PyPI
uv publish
```

You'll need a PyPI API token - get one at https://pypi.org/manage/account/token/

## After Publishing

- Verify at https://pypi.org/project/prettyplots/
- Test installation: `pip install prettyplots`
- Update README.md if needed

## Need More Details?

See `PUBLISHING.md` for comprehensive documentation.
