# AO3 RSS Feed Discord Bot

A lightweight Python bot that monitors Archive of Our Own (AO3) RSS feeds and posts new fics in a Discord channel. Supports dynamic content filtering and moderator review.

---

## 📦 Features

- Automatically posts AO3 fics in a designated Discord channel.
- Color-coded embeds based on fic rating.
- Displays fic metadata: author, series (if any), summary, words, chapters, and tags (all clickable).
- Filters based on:
  - **Hard-blocked warnings** (auto-block with no override).
  - **Soft-blocked tags** (requires moderator approval via buttons).
- Slash commands for moderators to:
  - Add/remove blocked tags.
  - View current blocked tags.
- Interactive Approve/Deny buttons for blocked fics.
- Tracks posted and denied fics to prevent reposts.

---

## 🚀 Getting Started

### 1. Enable Keep-Alive (Replit Users Only)

If hosting on Replit, ensure you:
- Create a `keep_alive.py` file with a minimal Flask server.
- Call `keep_alive()` in your `main.py` to prevent the bot from sleeping.
- Set up UptimeRobot (or similar) to ping your Replit URL every 5 minutes.

This will keep your bot online 24/7 on Replit's free plan.

### 2. Clone the Repo

```bash
git clone https://github.com/your-username/your-repo.git
```

### 3. Install Dependencies

```bash
pip install discord.py feedparser beautifulsoup4
```

### 4. Configure the Bot

In `main.py`, update:

- `DISCORD_TOKEN`: Use environment variables to keep it secure.
- `CHANNEL_ID`: ID of your public feed channel.
- `ADMIN_CHANNEL_ID`: ID of your private admin/mod channel.
- `MOD_ROLE_IDS`: Set of role IDs allowed to moderate and manage tags.
- `FEED_URLS`: List of AO3 feed URLs to monitor.

### 5. Run the Bot

```bash
python main.py
```

---

## ⚙️ Slash Commands

- `/blocktag <tag>`: Add a tag to the blocked tags.
- `/unblocktag <tag>`: Remove a tag from the blocked tags.
- `/showblockedtags`: View the current blocked tags list.

> Note: Commands auto-sync at startup.

---

## 📁 Persistent Files

- `posted_fics.json`: Tracks posted fics.
- `denied_fics.json`: Tracks denied fics.

These ensure that fics aren’t reposted even if the bot restarts.

---

## 🔐 Security & Permissions

- Keep the Discord bot token secure using environment variables (e.g., `DISCORD_TOKEN`).
- Use minimal Discord permissions:
  - Send Messages
  - Embed Links
  - Use Slash Commands
  - Read Message History (optional)

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

See the [LICENSE](LICENSE) file for details.

---

_Last updated: [2025-07-21]_
_By: NessaC
