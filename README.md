# Arda Tech — Central Flatpak Repository

Official centralized Flatpak repository hosting applications built and packaged by [Antux912012](https://github.com/Antux912012) (Arda Tech).

Hosted on GitHub Pages at: **[https://Antux912012.github.io/arda-tech](https://Antux912012.github.io/arda-tech)**

---

## 🚀 Quick Setup

Add the **Arda Tech** Flatpak repository with a single terminal command:

```bash
flatpak remote-add --if-not-exists arda-tech https://Antux912012.github.io/arda-tech/arda-tech.flatpakrepo
```

Or download the repository definition file:
- **[.flatpakrepo File](https://Antux912012.github.io/arda-tech/arda-tech.flatpakrepo)**
- **[GPG Public Key](https://Antux912012.github.io/arda-tech/arda-tech.gpg)**

---

## 📦 Hosted Applications

| Application | App ID | Install Command | .flatpakref |
| :--- | :--- | :--- | :--- |
| **CachyOS Kernel Updater** | `org.cachyos.debian.kernelupdater` | `flatpak install arda-tech org.cachyos.debian.kernelupdater` | [Download](https://Antux912012.github.io/arda-tech/org.cachyos.debian.kernelupdater.flatpakref) |
| **Imladris Markdown Editor** | `org.gnome.Imladris` | `flatpak install arda-tech org.gnome.Imladris` | [Download](https://Antux912012.github.io/arda-tech/org.gnome.Imladris.flatpakref) |
| **Mithrandir** | `io.github.antonio.Mithrandir` | `flatpak install arda-tech io.github.antonio.Mithrandir` | [Download](https://Antux912012.github.io/arda-tech/io.github.antonio.Mithrandir.flatpakref) |
| **Mithrandir (Rust)** | `io.github.antonio.MithrandirRS` | `flatpak install arda-tech io.github.antonio.MithrandirRS` | [Download](https://Antux912012.github.io/arda-tech/io.github.antonio.MithrandirRS.flatpakref) |
| **Vingilot Browser** | `io.github.antux912012.Vingilot` | `flatpak install arda-tech io.github.antux912012.Vingilot` | [Download](https://Antux912012.github.io/arda-tech/io.github.antux912012.Vingilot.flatpakref) |
| **YouTube Comment Extractor** | `io.github.antux912012.YTCommentExtractor` | `flatpak install arda-tech io.github.antux912012.YTCommentExtractor` | [Download](https://Antux912012.github.io/arda-tech/io.github.antux912012.YTCommentExtractor.flatpakref) |
| **YouTube Comment Extractor Service** | `io.github.antux912012.YTCommentExtractor.Service` | `flatpak install arda-tech io.github.antux912012.YTCommentExtractor.Service` | [Download](https://Antux912012.github.io/arda-tech/io.github.antux912012.YTCommentExtractor.Service.flatpakref) |

---

## 🔒 Security & Verification

All OSTree commits, deltas, and repo summaries in `arda-tech` are signed using a dedicated 4096-bit RSA GPG key:

- **Key ID:** `CF9DC18F75B6C72B`
- **Fingerprint:** `4C4C 7DAF 16CE 9706 0FAF  10AE CF9D C18F 75B6 C72B`
- **User ID:** `Arda Tech Flatpak Repo <antux912012@users.noreply.github.com>`

---

## 🛠 CI/CD Infrastructure

The repository is built and maintained automatically through GitHub Actions (`.github/workflows/build-repo.yml`):
- Container runtime: `ghcr.io/flathub-infra/flatpak-github-actions:freedesktop-25.08`
- Pulls existing OSTree commits from `gh-pages` branch for incremental builds.
- Builds all application manifests using `flatpak-builder` and Flathub dependencies.
- Generates static deltas using `flatpak build-update-repo --generate-static-deltas --prune`.
- Signs commits and summaries with GPG.
- Deploys repository, single-file bundles, `.flatpakrepo`, and `.flatpakref` files to GitHub Pages.
