# Arda Tech — Central APT PPA & Flatpak Repository

Official centralized **Debian/Ubuntu APT PPA** and **Flatpak** repository hosting applications built and packaged by [Antux912012](https://github.com/Antux912012) (Arda Tech).

- **APT PPA Repository:** **[https://antux912012.github.io/arda-tech-ppa](https://antux912012.github.io/arda-tech-ppa)** ([`Antux912012/arda-tech-ppa`](https://github.com/Antux912012/arda-tech-ppa))
- **Flatpak & Unified Portal:** **[https://Antux912012.github.io/arda-tech](https://Antux912012.github.io/arda-tech)**

---

## ⚡ 1. Arda-Tech PPA (Debian / Ubuntu / Mint APT Repository)

Add the **Arda-Tech PPA** with a single command:

```bash
curl -fsSL https://antux912012.github.io/arda-tech-ppa/setup.sh | sudo bash
```

Or configure manually:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://antux912012.github.io/arda-tech-ppa/KEY.gpg | sudo tee /etc/apt/keyrings/arda-tech.gpg >/dev/null
echo "deb [signed-by=/etc/apt/keyrings/arda-tech.gpg] https://antux912012.github.io/arda-tech-ppa stable main" | sudo tee /etc/apt/sources.list.d/arda-tech.list
sudo apt update
```

### APT Packages Available (`sudo apt install ...`)

| Package | Version | Arch | APT Install Command |
| :--- | :--- | :--- | :--- |
| **Mithrandir** | `0.4.1` | `all` | `sudo apt install mithrandir` |
| **Mithrandir-RS (Rust)** | `0.4.1` | `amd64` | `sudo apt install mithrandir-rs` |
| **Vingilot Browser** | `0.1.6-1` | `amd64` | `sudo apt install vingilot` |
| **Vingilot Estel** | `0.1.0-alpha-1` | `amd64` | `sudo apt install vingilot-estel` |
| **Imladris Studio** | `0.4.0` | `amd64` | `sudo apt install imladris` |
| **CachyOS Kernel Updater** | `1.1.2` | `all` | `sudo apt install cachy-kernel-updater` |
| **YouTube Comment Extractor** | `0.6` | `all` | `sudo apt install yt-comment-extractor` |
| **YouTube Comment Extractor Service** | `0.6` | `all` | `sudo apt install yt-comment-extractor-service` |
| **Súlimo (Arda's Breath)** | `0.3.0` | `amd64` | `sudo apt install sulimo` |
| **Validity VFS5011 Linux Fix** | `1.0.0` | `all` | `sudo apt install vfs5011-linux-fix` |

---

## 🚀 2. Arda-Tech Flatpak Repository

Add the **Arda Tech** Flatpak repository with a single terminal command:

```bash
flatpak remote-add --if-not-exists arda-tech https://Antux912012.github.io/arda-tech/arda-tech.flatpakrepo
```

Or download the repository definition file:
- **[.flatpakrepo File](https://Antux912012.github.io/arda-tech/arda-tech.flatpakrepo)**
- **[GPG Public Key](https://Antux912012.github.io/arda-tech/arda-tech.gpg)**

---

## 📦 Hosted Flatpak Applications

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
