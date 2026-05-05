# Contributing to Ansible for OpenShift Virtualization Migration

Thank you for your interest in contributing! Please check our [main documentation repository](https://github.com/redhat-cop/openshift-virtualization-migration-documentation) for comprehensive guides, deployment instructions, and additional resources.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Pull Request Guidelines](#pull-request-guidelines)
3. [Commit Message Format](#commit-message-format)
4. [PR Title Requirements](#pr-title-requirements)
5. [Changelog Fragments](#changelog-fragments)
6. [Development Workflow](#development-workflow)
7. [Release Process (Maintainers Only)](#release-process-maintainers-only)

## Getting Started

### Using Red Hat Developer Sandbox

Please perform the steps in the contribution guide [Using Red Hat Developer Sandbox](https://github.com/redhat-cop/openshift-virtualization-migration-documentation/blob/main/CONTRIBUTING.md#contribute-using-red-hat-developer-sandbox) section.

Click the link below to launch your IDE hosted in the Developer Sandbox:

[![Contribute](https://www.eclipse.org/che/contribute.svg)](https://workspaces.openshift.com/f?url=https://github.com/redhat-cop/openshift_virtualization_migration/openshift_virtualization_migration.git)

## Pull Request Guidelines

### External Contributors

All pull requests from forks require manual approval from a maintainer before CI runs. This is a security measure to protect against malicious code execution. A maintainer will review and approve your PR, after which automated tests will run.

### Internal Contributors

Pull requests from branches within the main repository run CI automatically.

### PR Checklist

Before submitting your pull request:

- [ ] PR title follows Conventional Commits format (see below)
- [ ] Changes are tested locally
- [ ] Documentation is updated if needed
- [ ] Changelog fragment added for significant changes (see below)
- [ ] All pre-commit hooks pass

## Commit Message Format

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages and PR titles. This standard enables:

- Automated changelog generation
- Semantic versioning
- Clear and scannable project history

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat**: A new feature (triggers minor version bump)
- **fix**: A bug fix (triggers patch version bump)
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or correcting tests
- **chore**: Changes to build process or auxiliary tools
- **ci**: Changes to CI configuration files and scripts
- **build**: Changes that affect the build system or dependencies

### Scope (Optional)

The scope provides additional context about what part of the codebase is affected:

- `roles`: Changes to Ansible roles
- `playbooks`: Changes to playbooks
- `modules`: Changes to modules
- `ci`: CI/CD changes
- `deps`: Dependency updates

### Examples

```
feat(roles): add VM snapshot management role
fix(mtv_management): handle missing provider credentials
docs: update installation instructions for AAP 2.5
chore(deps): update kubernetes.core to 5.3.0
refactor(validate_migration): simplify validation logic
test(mtv_management): add provider connection tests
```

### Breaking Changes

For changes that break backward compatibility, add `!` after the type/scope or include `BREAKING CHANGE:` in the footer:

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: The /v1/legacy endpoint has been removed. Use /v2/resources instead.
```

Breaking changes trigger a major version bump.

## PR Title Requirements

**CRITICAL**: Your PR title MUST follow Conventional Commits format. When your PR is merged (via squash merge), the PR title becomes the commit message, which is used for:

1. Generating the CHANGELOG
2. Determining the next version number
3. Creating release notes

### Format Rules

- Maximum length: **72 characters**
- Must match: `<type>(<scope>): <description>`
- Type must be one of: feat, fix, docs, style, refactor, perf, test, chore, ci, build
- Description must be lowercase and concise

### Examples

✅ **GOOD**:
- `feat: add VM backup role`
- `fix(mtv_management): correct provider validation`
- `docs: update README with new requirements`
- `chore(deps): bump ansible-core to 2.20.0`

❌ **BAD**:
- `Update files` (no type)
- `feat Add new feature` (missing colon)
- `FEAT: ADD NEW FEATURE` (wrong case)
- `feat: This is a very long PR title that exceeds the maximum character limit and will fail validation` (too long)

### Validation

A [GitHub Action](.github/workflows/pr-title-validation.yml) automatically validates PR titles. If your title doesn't match the format, the check will fail and you must update it before merging.

## Changelog Fragments

Changelog fragments are automatically generated based on the conventional commit messages. However, contributors may add additional information by crafting their own changelog fragment to help generate release notes.

### When to Add Fragments [optional]

Add a fragment for:
- New features (`feat`)
- Bug fixes (`fix`)
- Breaking changes
- Security fixes
- Significant refactoring
- Important documentation updates

### When to Skip Fragments

Small changes don't need fragments:
- Typo fixes
- CI configuration tweaks
- Minor README updates
- Code formatting
- Test-only changes

### Creating Fragments

Create a new YAML file in `changelogs/fragments/`:

```bash
# Filename format: <issue_or_pr_number>-<short_description>.yml
cat > changelogs/fragments/123-add-vm-snapshot.yml <<EOF
---
minor_changes:
  - "Add VM snapshot management role with create, list, restore, and delete capabilities"
EOF
```

### Fragment Types

Available fragment types (from [changelogs/config.yaml](changelogs/config.yaml)):

- `major_changes`: Significant new features or changes
- `minor_changes`: New features, enhancements
- `breaking_changes`: Changes that break compatibility (requires major version bump)
- `deprecated_features`: Features marked for removal
- `removed_features`: Previously deprecated features now removed
- `security_fixes`: Security-related fixes
- `bugfixes`: Bug fixes
- `known_issues`: Documented issues or limitations
- `doc_changes`: Significant documentation updates

### Fragment Examples

Bug fix fragment:
```yaml
---
bugfixes:
  - "mtv_management - fix credential validation for password-protected providers"
```

Feature fragment with multiple entries:
```yaml
---
minor_changes:
  - "Add support for hot-plugging CPU and memory to VMs"
  - "Implement VM template management role"
```

Breaking change fragment:
```yaml
---
breaking_changes:
  - "Remove support for VMware vSphere 6.5. Minimum version is now 6.7."
```

## Development Workflow

### Setting Up Your Environment

1. Fork the repository (external contributors) or create a branch (internal contributors)
2. Clone your fork or the main repository
3. Install development dependencies:

```bash
# Install Ansible collection dependencies
ansible-galaxy collection install -r requirements.yml

# Install Python development dependencies
pip install -r requirements-dev.txt
```

### Running Tests Locally

```bash
# Run ansible-lint
ansible-lint

# Run YAML linting
yamllint .

# Run molecule tests for a specific role (if applicable)
cd roles/<role-name>
molecule test

# Run all pre-commit hooks
pre-commit run --all-files
```

### Pre-commit Hooks

This repository uses pre-commit hooks for code quality. Install them to run checks automatically before each commit:

```bash
pip install pre-commit
pre-commit install
```

The hooks will:
- Lint YAML files with yamllint
- Check for secrets with gitleaks
- Validate Ansible syntax with ansible-lint
- Check for merge conflict markers
- Detect broken symlinks
- Remove trailing whitespace

If a hook fails, fix the issue and commit again. Some hooks can auto-fix issues (like trailing whitespace).

### Making Changes

1. Create a feature branch: `git checkout -b feat/my-feature`
2. Make your changes
3. Run tests locally
4. Commit with conventional commit messages
5. Push to your fork/branch
6. Create a pull request with a conventional commit title

## Release Process (Maintainers Only)

This section is for repository maintainers with release permissions.

### Overview

This project uses automated releases via GitHub Actions. The release workflow:

1. Creates a release PR with updated version and CHANGELOG
2. Runs all tests on the release PR
3. Publishes to Ansible Galaxy and Red Hat Automation Hub when merged
4. Creates a GitHub release with collection artifacts

### Prerequisites

To trigger releases, you must have:

- Access to the `release` GitHub Environment (configured in repository settings)
- Red Hat Automation Hub credentials (AUTOMATION_HUB_TOKEN secret)
- GitHub App credentials for releases (RELEASE_APP_ID, RELEASE_APP_PRIVATE_KEY secrets)

### Version Determination

The collection uses [Semantic Versioning (SemVer)](https://semver.org/):

- **Major (X.0.0)**: Breaking changes (incompatible API changes)
- **Minor (0.X.0)**: New features (backward compatible)
- **Patch (0.0.X)**: Bug fixes (backward compatible)

Version bumps are determined **automatically** from Conventional Commit messages in the changelog:

- Commits with `BREAKING CHANGE:` or `!` → major bump
- Commits with `feat:` → minor bump
- Commits with `fix:` → patch bump

### Triggering a Release

#### Step 1: Verify Main Branch is Ready

Before triggering a release:

- [ ] All intended PRs for the release are merged to `main`
- [ ] CI is green on `main` branch
- [ ] No known critical bugs or regressions
- [ ] Documentation is up to date

#### Step 2: Trigger Workflow

1. Navigate to **Actions** → **CI** workflow
2. Click **Run workflow** (top right)
3. Configure inputs:
   - **Branch**: `main` (required)
   - **trigger_release**: ✅ Check this box
   - **auto_merge**: ⬜ Leave unchecked (recommended for safety)
4. Click **Run workflow**

#### Step 3: Approve Release (Environment Gate)

1. The workflow will pause and wait for approval in the `release` environment
2. Navigate to the workflow run and click **Review deployments**
3. Review the approval request details:
   - Who triggered the release
   - What inputs were provided
   - Current branch and commit
4. Approve or reject based on:
   - Is `main` branch in a good state?
   - Are all tests passing?
   - Is this the right time for a release?
5. Click **Approve and deploy** if everything looks good

#### Step 4: Review Release PR

After approval, the workflow will:

1. Calculate the new version based on commit messages
2. Generate updated CHANGELOG
3. Create a release PR titled `chore(release): X.Y.Z`

Review the release PR carefully:

- Check the version number is correct
- Review CHANGELOG entries for accuracy
- Ensure all expected changes are documented
- Verify CI passes on the release PR

If the release PR has issues:
- Close the PR
- Fix issues on `main`
- Re-trigger the release workflow

#### Step 5: Merge Release PR

Once CI passes on the release PR:

1. Review and approve the PR
2. Merge using **squash merge** (default)
3. The workflow automatically:
   - Builds the collection artifact (.tar.gz)
   - Publishes to Red Hat Automation Hub
   - Publishes to Ansible Galaxy (if configured)
   - Creates a GitHub release with the artifact attached
   - Tags the release commit

#### Auto-merge Option (Advanced)

For experienced maintainers, you can enable auto-merge:

1. When triggering the workflow, check **auto_merge: true**
2. The release PR will merge automatically if CI passes
3. **Use with caution** - you won't get a chance to review the PR before merge

### Troubleshooting Releases

#### Release PR Not Created

**Symptoms**: Workflow runs but no PR appears

**Solutions**:
- Check Actions logs for errors
- Verify you have permissions in the `release` environment
- Ensure `main` branch is up to date
- Check GitHub App credentials are configured

#### Publishing Failed

**Automation Hub**:
- Verify AUTOMATION_HUB_TOKEN secret is valid
- Check token has not expired
- Verify namespace and collection name match

**Galaxy**:
- Verify galaxy.yml metadata is correct
- Check API token is configured

#### Wrong Version Number

**Symptoms**: Version calculated incorrectly

**Cause**: Version is calculated from commit messages since last release

**Solutions**:
1. Close the release PR
2. Manually update `galaxy.yml` version on `main`
3. Commit with message: `chore(release): X.Y.Z`
4. Re-run release workflow

#### Tests Failing on Release PR

**Solutions**:
1. Do NOT merge the release PR
2. Close the release PR
3. Fix the failing tests on `main`
4. Wait for CI to pass on `main`
5. Re-trigger the release workflow

### Release Checklist

Before triggering a release:

- [ ] All planned PRs are merged to `main`
- [ ] CI is green on `main` branch
- [ ] No known critical bugs
- [ ] Documentation is current
- [ ] Dependencies are up to date
- [ ] Pre-commit hooks pass
- [ ] You have release environment access

After triggering:

- [ ] Review approval request details
- [ ] Approve release in GitHub environment
- [ ] Review release PR for correctness
- [ ] Verify CI passes on release PR
- [ ] Merge release PR
- [ ] Verify publication to Automation Hub
- [ ] Check GitHub release was created
- [ ] Announce release (if needed)

### Release Schedule

Releases are created **on-demand** by maintainers. Consider releasing when:

- Critical bug fixes are merged
- Significant new features are ready
- Security fixes are available
- Monthly maintenance window (1st and 15th - when scheduled CI runs)
- User requests for specific fixes/features

There is no fixed release schedule - releases happen when needed.

### Security Considerations

The release workflow includes multiple security controls:

1. **Environment approval**: Only authorized maintainers can approve releases
2. **Branch restriction**: Releases can only be triggered from `main` branch
3. **Audit logging**: All release triggers are logged with actor information
4. **Secret protection**: Secrets are only exposed after approval
5. **Concurrency control**: Releases run sequentially, never in parallel

Never share release credentials or bypass the approval process.

## Questions?

- **General questions**: Check the [documentation repository](https://github.com/redhat-cop/openshift-virtualization-migration-documentation)
- **Bug reports**: Open an issue with details and steps to reproduce
- **Feature requests**: Open an issue describing the use case
- **Security issues**: See CODE_OF_CONDUCT.md for reporting instructions

Thank you for contributing to OpenShift Virtualization Migration!
