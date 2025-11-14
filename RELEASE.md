# Release Process for Netto

This document describes how to release a new version of Netto to PyPI.

## Prerequisites

### 1. Set up PyPI Trusted Publishing

The project uses PyPI's trusted publishing (OpenID Connect) which is more secure than API tokens. You need to configure this once:

#### For TestPyPI (recommended to test first):

1. Go to https://test.pypi.org and log in (create account if needed)
2. Go to Account Settings → Publishing → Add a new pending publisher
3. Fill in the form:
   - **PyPI Project Name**: `netto`
   - **Owner**: `0-k` (your GitHub username/org)
   - **Repository name**: `netto`
   - **Workflow name**: `publish_test.yml`
   - **Environment name**: `testpypi`
4. Click "Add"

#### For PyPI (production):

1. Go to https://pypi.org and log in
2. Go to Account Settings → Publishing → Add a new pending publisher
3. Fill in the form:
   - **PyPI Project Name**: `netto`
   - **Owner**: `0-k`
   - **Repository name**: `netto`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Click "Add"

### 2. Create GitHub Environments

Create the required environments in your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to Settings → Environments
3. Create two environments:
   - **testpypi** (for test releases)
   - **pypi** (for production releases)
4. (Optional) Add protection rules to require approval before publishing

## Release Process

### Step 1: Update Version

Update the version number in `pyproject.toml`:

```bash
# In pyproject.toml
version = "X.Y.Z"
```

### Step 2: Update CHANGELOG

Add release notes to `CHANGELOG.md` following the existing format (create if it doesn't exist):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Security
- Security fixes
```

### Step 3: Test the Build Locally

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the built package
twine check dist/*

# Optionally, test install locally
pip install dist/netto-X.Y.Z-py3-none-any.whl
```

### Step 4: Commit and Push

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

### Step 5: Test on TestPyPI (Recommended)

1. Go to GitHub Actions
2. Select "Publish to TestPyPI" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for the workflow to complete
5. Test installing from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple netto
   ```

### Step 6: Create a GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Click "Choose a tag" and create a new tag: `vX.Y.Z` (e.g., `v0.1.1`)
4. Set the release title: `vX.Y.Z`
5. Copy the relevant section from CHANGELOG.md into the release description
6. Click "Publish release"

### Step 7: Automatic PyPI Publishing

Once you publish the release, the GitHub Action will automatically:
1. Build the package
2. Publish to PyPI

You can monitor the progress in the "Actions" tab.

### Step 8: Verify the Release

1. Check that the package appears on PyPI: https://pypi.org/project/netto/
2. Test installing the package:
   ```bash
   pip install netto
   ```
3. Verify the version:
   ```bash
   python -c "import netto; print(netto.__version__)"
   ```

## Troubleshooting

### Trusted Publishing Not Set Up

**Error**: `Error: Invalid or non-existent authentication information`

**Solution**: Make sure you've configured trusted publishing on PyPI/TestPyPI (see Prerequisites above).

### Environment Not Found

**Error**: `Environment not found`

**Solution**: Create the required environments in GitHub repository settings.

### Build Fails

**Error**: Build process fails during GitHub Action

**Solution**:
1. Check the GitHub Actions logs
2. Try building locally with `python -m build`
3. Ensure all files are committed and pushed

### Package Already Exists

**Error**: `File already exists`

**Solution**: You cannot re-upload the same version. Increment the version number and try again.

## Version Numbering

Netto follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality, backwards compatible
- **PATCH** version (0.0.X): Bug fixes, backwards compatible

Examples:
- `0.1.0` → `0.1.1`: Bug fix release
- `0.1.0` → `0.2.0`: New features, backwards compatible
- `0.9.0` → `1.0.0`: First stable release with API guarantees
- `1.0.0` → `2.0.0`: Breaking changes to API

## Pre-releases

For alpha/beta releases, append to the version:

```
version = "0.2.0a1"  # Alpha release
version = "0.2.0b1"  # Beta release
version = "0.2.0rc1" # Release candidate
```

## Quick Reference

```bash
# Complete release checklist
1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. python -m build
4. twine check dist/*
5. git commit -am "chore: bump version to X.Y.Z"
6. git push
7. Test on TestPyPI (via GitHub Actions)
8. Create GitHub release with tag vX.Y.Z
9. Automatic PyPI publish
10. Verify on PyPI
```
