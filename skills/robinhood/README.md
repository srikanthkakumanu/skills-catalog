# Robinhood Skill

`robinhood` is a cross-runtime Agent Skill for Antigravity 2.x, Claude Code, and OpenAI Codex. It helps agents find official direct links and lawful access options for named resources such as books, films, videos, songs, albums, audiobooks, papers, and other digital media.

The skill is intentionally access focused. It should route users toward official direct links, public-domain files, open-license resources, creator or publisher pages, library borrowing options, licensed streaming/rental services, purchase options, and citation pages. It must not help with unauthorized direct downloads.

## Structure

```text
skills/robinhood/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
└── references/
    └── legal-source-guide.md
```

## Invocation Examples

- `$robinhood Find lawful direct links for Pride and Prejudice by Jane Austen.`
- `$robinhood Where can I watch the 1957 film 12 Angry Men legally?`
- `$robinhood Find an open-access copy of this paper by title and DOI.`

## Installation

Run the installer from the repository root.

### Install to All Supported Runtimes

```bash
./install.sh --skill robinhood
```

This installs `robinhood` for Antigravity 2.x, Claude Code, and OpenAI Codex using the installer's default symlink mode.

### Install to One Runtime

```bash
# Antigravity 2.x
./install.sh --skill robinhood --target antigravity

# OpenAI Codex
./install.sh --skill robinhood --target codex

# Claude Code
./install.sh --skill robinhood --target claude
```

### Copy Instead of Symlink

```bash
./install.sh --skill robinhood --mode copy
```

### Overwrite an Existing Install

```bash
./install.sh --skill robinhood --force
```

## Running

After installation, invoke the skill by explicit skill name, slash command, or natural language.

```text
$robinhood Find lawful direct links for Pride and Prejudice by Jane Austen.
```

```text
/robinhood Where can I watch 12 Angry Men legally?
```

```text
Use robinhood to find official download or streaming options for this album: [album name].
```

`robinhood` prioritizes official direct links when they are lawful and available. When a direct download is not lawfully available, it returns legitimate access pages such as publisher pages, library borrowing options, public-domain archives, open-access repositories, licensed streaming/rental services, or purchase links.

## Scope Levels

| Scope        | Intended Use                                    |
| :----------- | :---------------------------------------------- |
| `quick`    | A compact list of likely lawful access routes.  |
| `standard` | Verified metadata plus grouped lawful options.  |
| `deep`     | Edition, region, format, license, and source comparison. |

## Safety Boundary

Allowed:

- Official downloads or access pages.
- Public-domain and open-license files.
- Library borrowing, controlled digital lending, rental, streaming, and purchase options.
- Metadata lookup and citation help.

Disallowed:

- Pirated ebooks, ripped movies, leaked screeners, cracked audiobooks, unauthorized music downloads, torrents, magnet links, file-hosting mirrors, paywall bypasses, or DRM circumvention.
