# 📝 Release Notes Template

**Release Notes Writing Guide for DataBrew Lab**  
**Last Updated**: November 15, 2025

---

## 📋 Table of Contents

1. [Release Notes Overview](#release-notes-overview)
2. [When to Write Release Notes](#when-to-write-release-notes)
3. [Release Notes Template](#release-notes-template)
4. [Writing Guidelines](#writing-guidelines)
5. [Examples](#examples)
6. [Distribution Checklist](#distribution-checklist)

---

## 📖 Release Notes Overview

### Purpose
Release notes communicate what changed in a new version to:
- **Users**: What new features they can use
- **Developers**: What changed technically
- **Stakeholders**: Project progress and value delivered
- **Support Teams**: What to expect in support tickets

### Types of Releases
| Type | Version | Example | When |
|------|---------|---------|------|
| **Major** | X.0.0 | 1.0.0 | Major features, breaking changes |
| **Minor** | 0.X.0 | 0.2.0 | New features, backwards compatible |
| **Patch** | 0.0.X | 0.1.1 | Bug fixes, minor improvements |
| **Pre-release** | 0.X.0-beta | 0.2.0-beta.1 | Testing releases |

---

## ⏰ When to Write Release Notes

### Required for ALL:
- ✅ Major releases (X.0.0)
- ✅ Minor releases (0.X.0)
- ✅ Patch releases with user-visible changes
- ✅ Beta/pre-releases for early adopters

### Optional but Recommended:
- 🟡 Internal development builds
- 🟡 Hot fixes
- 🟡 Sprint completions (internal)

### Not Required:
- ❌ Local development builds
- ❌ Test releases
- ❌ Incomplete features

---

## 📄 Release Notes Template

```markdown
# DataBrew Lab - Release v[VERSION]

**Release Date**: [Date]  
**Version**: [X.Y.Z]  
**Type**: [Major/Minor/Patch]  
**Status**: [Stable/Beta/RC]

---

## 🎯 Release Highlights

[2-3 sentences summarizing the most important changes]

**Key Improvements**:
- **[Feature 1]**: [Brief description of value]
- **[Feature 2]**: [Brief description of value]
- **[Feature 3]**: [Brief description of value]

---

## ✨ New Features

### [Feature Category 1]

#### [Feature Name]
**Description**: [What it does]  
**Benefits**: [Why users care]  
**How to Use**: [Quick guide or link]

```[optional code example or screenshot reference]```

**Related**: Issue #XXX, PR #XXX

---

### [Feature Category 2]

#### [Feature Name]
[Same structure as above]

---

## 🔧 Improvements

### [Area 1]
- **[Improvement]**: [Description]
- **[Improvement]**: [Description]

### [Area 2]
- **[Improvement]**: [Description]

---

## 🐛 Bug Fixes

### Critical Fixes
- **[Bug]**: [What was wrong, what's fixed]  
  *Impact*: [Who was affected]  
  *Closes*: #XXX

### Major Fixes
- **[Bug]**: [Description]
- **[Bug]**: [Description]

### Minor Fixes
- **[Bug]**: [Description]
- **[Bug]**: [Description]

---

## 🚨 Breaking Changes

⚠️ **IMPORTANT: This release contains breaking changes**

### [Change 1]
**What Changed**: [Description]  
**Why**: [Reason for change]  
**Migration Guide**: [How to update]  
**Example**:
```[before/after code]```

### [Change 2]
[Same structure]

---

## 📊 Performance Improvements

- **[Area]**: [Improvement metrics]  
  Example: "Search response time reduced by 40% (500ms → 300ms)"
- **[Area]**: [Improvement metrics]

---

## 🔒 Security Updates

### High Priority
- **[Security Issue]**: [Description of fix]  
  *CVE*: [If applicable]  
  *Severity*: Critical/High/Medium/Low

### General Security Improvements
- [Improvement 1]
- [Improvement 2]

---

## 📚 Documentation Updates

- **[Doc]**: [What's new or updated]
- **[Doc]**: [What's new or updated]
- **New Guides**: [List new documentation]

---

## 🔄 Deprecations

⚠️ **The following features are deprecated and will be removed in v[VERSION]**

- **[Feature/API]**: [Reason] - Use [Alternative] instead
- **[Feature/API]**: [Reason] - Use [Alternative] instead

---

## 🛠️ Technical Changes

### Backend
- [Technical change 1]
- [Technical change 2]

### Frontend
- [Technical change 1]
- [Technical change 2]

### Infrastructure
- [Technical change 1]
- [Technical change 2]

### Dependencies
- Updated [Package] from vX.Y to vX.Z
- Added [Package] for [Reason]
- Removed [Package] (no longer needed)

---

## 📦 Installation & Upgrade

### New Installation
```bash
# For cloud deployment
npm install
cd backend && npm install
npm run build

# For desktop
npm run build:desktop
```

### Upgrading from v[PREVIOUS VERSION]

#### Cloud Deployment
```bash
git pull origin main
npm install
cd backend && npm install
npm run build
npm run migrate # If database changes
npm run start
```

#### Desktop Application
- Download installer from [releases page](link)
- Auto-update will prompt (if enabled)
- Or manually install over existing version

**Migration Notes**:
- [Any special migration steps]
- [Database migrations required?]
- [Configuration changes needed?]

---

## 📋 Testing

This release has been tested with:
- ✅ [X] unit tests passing
- ✅ [X] integration tests passing
- ✅ E2E tests on [platforms]
- ✅ Performance benchmarks met
- ✅ Security audit completed

**Test Coverage**: [X]%  
**Platforms Tested**: Windows, macOS, Linux

---

## 🙏 Contributors

Thank you to everyone who contributed to this release:

- [@username](link) - [Contribution]
- [@username](link) - [Contribution]
- [@username](link) - [Contribution]

**Statistics**:
- [X] commits
- [X] files changed
- [X] PRs merged
- [X] issues closed

---

## 🐛 Known Issues

### Minor Issues
- **[Issue]**: [Description]  
  *Workaround*: [Temporary solution]  
  *Tracking*: #XXX

### Limitations
- [Known limitation 1]
- [Known limitation 2]

---

## 🔮 What's Next?

**Coming in v[NEXT VERSION]**:
- [Planned feature 1]
- [Planned feature 2]
- [Planned improvement 1]

See [Roadmap](../PENDING_WORK.md) for full details.

---

## 📞 Support & Feedback

**Having Issues?**
- 🐛 **Bug Reports**: [GitHub Issues](link)
- 💬 **Questions**: [GitHub Discussions](link)
- 📧 **Email**: support@databrew-lab.com
- 📖 **Documentation**: [docs/](link)

**Share Feedback**:
- 🌟 Star us on [GitHub](link)
- 🐦 Follow on [Twitter](link)
- 💼 Join on [LinkedIn](link)

---

## 📄 Full Changelog

See [CHANGELOG.md](../../CHANGELOG.md) for complete version history.

---

**Released by**: [Team Name]  
**Release Manager**: [Name]  
**Build**: [Build Number]  
**Git Tag**: [vX.Y.Z](link to tag)  
**Download**: [Release Page](link)

---

<div align="center">

**Happy Using! 🚀**

*We appreciate your continued support!*

</div>
```

---

## ✍️ Writing Guidelines

### General Principles

**Do**:
- ✅ Write for your audience (users first, then developers)
- ✅ Use simple, clear language
- ✅ Focus on value and benefits, not just features
- ✅ Include examples and visuals where helpful
- ✅ Link to detailed documentation
- ✅ Be honest about known issues
- ✅ Thank contributors

**Don't**:
- ❌ Use jargon without explanation
- ❌ List technical details without context
- ❌ Hide breaking changes or issues
- ❌ Make it too long (users won't read it)
- ❌ Forget to proofread
- ❌ Skip testing notes

### Tone & Style

**Tone**:
- Professional but friendly
- Exciting for new features
- Clear and direct for breaking changes
- Apologetic for major bugs
- Grateful to contributors

**Style**:
- Active voice: "We added" not "Feature was added"
- Present tense for current state
- Bullet points over paragraphs
- Headers for scanning
- Emojis for visual interest (but don't overdo it)

### Sections Guide

#### Release Highlights
- **Length**: 2-3 sentences + 3-5 key points
- **Purpose**: Executive summary for busy readers
- **What to include**: Most important/exciting changes only

#### New Features
- **For each feature**:
  - What it is (1 sentence)
  - Why it matters (1 sentence)
  - How to use it (1-2 sentences or link)
- **Group by category** (e.g., UI, API, Performance)
- **Use screenshots/GIFs** for UI changes

#### Bug Fixes
- **Priority order**: Critical → Major → Minor
- **Format**: "[What] - [Impact]"
- **Example**: "Fixed data loss on logout - Users' work now saves correctly"
- **Don't**: List internal bug IDs without context

#### Breaking Changes
- **Always call them out** with ⚠️ warning
- **Explain why** the change was necessary
- **Provide migration path** with examples
- **Link to migration guide** if complex

#### Performance Improvements
- **Use numbers**: "40% faster" not "much faster"
- **Show before/after**: "500ms → 300ms"
- **Explain impact**: What users will notice

#### Known Issues
- **Be upfront** about problems
- **Provide workarounds** if available
- **Link to tracking issue**
- **Set expectations** for fix timeline

---

## 💡 Examples

### Example 1: Major Release (v1.0.0)

<details>
<summary>Click to expand example</summary>

```markdown
# DataBrew Lab - Release v1.0.0 🎉

**Release Date**: December 15, 2025  
**Version**: 1.0.0  
**Type**: Major Release  
**Status**: Stable

---

## 🎯 Release Highlights

We're thrilled to announce DataBrew Lab v1.0.0, our first stable release! This milestone brings complete context system implementation, enhanced AI capabilities, and production-ready desktop applications for all major platforms.

**Key Improvements**:
- **Complete Context System**: Full processing pipeline from capture to consumption
- **Enhanced AI Analysis**: 60% faster with new caching and optimization
- **Production Desktop Apps**: Native installers for Windows, macOS, and Linux
- **Advanced Search**: Hybrid search with 40% better relevance
- **Mobile Support**: Fully responsive design for tablets and phones

---

## ✨ New Features

### Context System
#### Intelligent Document Processing
**Description**: Automatically chunks, analyzes, and indexes documents with AI  
**Benefits**: 10x faster research with semantic search and instant insights  
**How to Use**: Upload any document and watch the magic happen

---

### AI & Analytics
#### Multi-Model AI Support
**Description**: Choose between Gemini, GPT-4, Claude, or custom models  
**Benefits**: Best AI for your use case, avoid vendor lock-in  
**How to Use**: Settings → AI Models → Select preferred provider

[Continue with more features...]
```

</details>

### Example 2: Bug Fix Release (v0.1.2)

<details>
<summary>Click to expand example</summary>

```markdown
# DataBrew Lab - Release v0.1.2

**Release Date**: November 20, 2025  
**Version**: 0.1.2  
**Type**: Patch Release  
**Status**: Stable

---

## 🎯 Release Highlights

This patch release fixes critical issues with relationship graphs and improves overall stability.

---

## 🐛 Bug Fixes

### Critical Fixes
- **Relationship Graph Loading**: Fixed crash when loading large graphs with >1000 nodes  
  *Impact*: All users attempting to visualize complex relationships  
  *Closes*: #145, #152, #158

### Major Fixes
- **Podcast Transcription**: Fixed API URL issues with Spotify podcasts  
  *Impact*: Users transcribing Spotify content  
  *Closes*: #149
  
- **Repository Files**: Files now appear immediately after upload (no refresh needed)  
  *Impact*: All users uploading documents  
  *Closes*: #151

### Minor Fixes
- Fixed typo in error message
- Improved loading indicator timing
- Updated icon alignment in sidebar

---

[Continue with rest of release notes...]
```

</details>

### Example 3: Feature Release (v0.2.0)

<details>
<summary>Click to expand example</summary>

```markdown
# DataBrew Lab - Release v0.2.0

**Release Date**: January 15, 2026  
**Version**: 0.2.0  
**Type**: Minor Release  
**Status**: Stable

---

## 🎯 Release Highlights

Introducing mobile apps, collaborative features, and plugin architecture!

**Key Improvements**:
- **Mobile Apps**: Native iOS and Android apps now available
- **Real-time Collaboration**: Work together in shared workspaces
- **Plugin Marketplace**: Extend functionality with community plugins

---

## ✨ New Features

### Mobile Applications
#### iOS & Android Apps
**Description**: Full-featured mobile apps for research on the go  
**Benefits**: Access your research anywhere, offline support  
**Download**: [App Store](link) | [Google Play](link)

**Features**:
- All core features available
- Offline mode with sync
- Native camera integration for screenshots
- Voice recording for transcription

---

### Collaboration
#### Team Workspaces
**Description**: Shared spaces for team research projects  
**Benefits**: Real-time collaboration, no email chains  
**How to Use**: Create workspace → Invite team → Start collaborating

**Features**:
- Real-time document editing
- Comment threads
- Activity feed
- Permission management

---

[Continue...]
```

</details>

---

## ✅ Distribution Checklist

### Before Release

#### Code & Build
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code reviewed and approved
- [ ] Version number updated (package.json, etc.)
- [ ] Git tag created (vX.Y.Z)
- [ ] Build artifacts created and tested
- [ ] Desktop installers signed (if applicable)

#### Documentation
- [ ] Release notes written (this template)
- [ ] CHANGELOG.md updated
- [ ] API documentation updated (if changes)
- [ ] User guides updated (if UI changes)
- [ ] Migration guide written (if breaking changes)

#### Testing
- [ ] Smoke tests on production build
- [ ] Installation tested on all platforms
- [ ] Upgrade tested from previous version
- [ ] Breaking changes verified in test environment

### During Release

#### GitHub Release
- [ ] Create release on GitHub
- [ ] Upload release notes
- [ ] Attach build artifacts
- [ ] Tag release properly
- [ ] Set as latest release (or pre-release)

#### Distribution
- [ ] Deploy to production (cloud)
- [ ] Publish desktop installers
- [ ] Update mobile app stores (if applicable)
- [ ] Update download links on website

#### Communication
- [ ] Post announcement on GitHub Discussions
- [ ] Send email to users (if applicable)
- [ ] Post on social media
- [ ] Update documentation site
- [ ] Notify support team

### After Release

#### Monitoring
- [ ] Monitor error logs
- [ ] Watch for user reports
- [ ] Check analytics/metrics
- [ ] Verify auto-updates working (desktop)

#### Follow-up
- [ ] Respond to feedback
- [ ] Address urgent issues quickly
- [ ] Plan patch release if needed
- [ ] Update roadmap based on feedback
- [ ] Thank contributors publicly

---

## 📞 Release Management Contacts

**Release Manager**: [Name]  
**Technical Lead**: [Name]  
**Product Owner**: [Name]  
**Support Lead**: [Name]

**Emergency Contact**: [For critical post-release issues]

---

## 📚 Additional Resources

- [Semantic Versioning](https://semver.org/) - Version numbering guide
- [Keep a Changelog](https://keepachangelog.com/) - Changelog format
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github) - GitHub release guide

---

**Last Updated**: November 15, 2025  
**Template Version**: 1.0  
**Maintained By**: Release Management Team

---

<div align="center">

**Clear Communication, Smooth Releases! 🚀**

</div>
