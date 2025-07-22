# AO3 RSS Feed Discord Bot

A lightweight, automated Discord bot that monitors one or multiple Archive of Our Own (AO3) RSS feeds and posts new fics in a designated channel. Includes automatic content filtering and moderator approval features.

---

## 📦 Features

- Automatically checks AO3 RSS feeds at set intervals (default: every 1 hour).
- Posts fanfics in a designated Discord channel using rich embeds.
- Color-coded embeds based on fic rating.
- Displays fic metadata: author, series (if any), summary, words, chapters, ratings, warnings, fandoms, relationships, characters, and tags.
- Supports content filtering via:
  - **Hard-blocked warnings** (automatic block).
  - **Soft-blocked tags** (requires moderator review and approval).
- Interactive Approve/Deny buttons in the mod/admin review channel.
- Persistent log of posted and denied fics to prevent reposts.
- Persistent blocked tags list across restarts.
- Simple slash commands for moderators to manage blocked tags.

---

## 🚀 Setup Instructions

### 1. Dependencies

Ensure `requirements.txt` includes:

```
discord.py
feedparser
beautifulsoup4
```

Install with:

```bash
pip install -r requirements.txt
```

### 2. Configuration

In `main.py`, configure:

- `DISCORD_TOKEN`: Provided as an environment variable.
- `CHANNEL_ID`: Discord channel ID where fics are publicly posted.
- `ADMIN_CHANNEL_ID`: Private admin/mod channel for approvals and logs.
- `MOD_ROLE_IDS`: Set of role IDs allowed to approve/deny fics and manage tags.
- `FEED_URLS`: List of AO3 feed URLs to monitor.
- `BLOCKED_WARNINGS`: List of warnings that result in automatic blocking.

### 3. Persistent Files

- `blocked_tags.json`: Stores current blocked tags persistently.
- `posted_fics.json`: Tracks posted fic IDs to avoid reposting.
- `denied_fics.json`: Tracks denied fic IDs to avoid re-reviewing.

Ensure these files exist and contain valid JSON (use empty lists as initial content).

---

## 🛠️ Slash Commands (Mods Only)

- `/blocktag <tag>`: Adds a tag to the blocked tags list.
- `/unblocktag <tag>`: Removes a tag from the blocked tags list.
- `/showblockedtags`: Displays the current list of blocked tags.

All tag changes persist automatically across bot restarts.

---

## 🔐 Security & Permissions

- Use environment variables to store your `DISCORD_TOKEN` securely.
- Restrict slash commands using `MOD_ROLE_IDS`.
- Bot requires only essential Discord permissions:
  - Send Messages
  - Embed Links
  - Use Slash Commands

---

## 📈 Planned Improvements

- Command to add or remove feed (for events).
- Multi-feed/channel support (for easier testing and debbuging).
- Persistent blocked warnings management.

---

## 📄 License

Licensed under the GNU General Public License v3.0 (GPL-3.0).

---

_Last updated: [2025-07-21]_
_By: [NessaC]_
