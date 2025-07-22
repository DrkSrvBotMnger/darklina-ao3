# AO3 RSS Discord Bot

A lightweight, PostgreSQL-backed Discord bot that monitors one or more Archive of Our Own (AO3) RSS feeds and posts new fics in a Discord channel. Designed for fandom communities with dynamic content filtering and moderator control.

---

## 📦 Features

- **AO3 RSS Feed Parsing**: Monitors AO3 feeds and posts new fics as embeds.
- **Color-Coded Embeds**: Rating-based color system for embeds.
- **Detailed Metadata Display**: Author, series, summary, words, chapters, warnings, fandoms, relationships, characters, and tags.
- **Hard-Blocked Warnings**: Fics with blocked warnings (like Underage) are automatically denied.
- **Soft-Blocked Tags with Mod Review**: Fics tagged with soft-blocked tags are sent to an admin channel for manual review.
- **Persistent Storage (PostgreSQL)**:
  - Logged posted and denied fics.
  - Dynamic blocked tags stored and managed in the database.
- **Slash Commands**:
  - `/blocktag <tag>`
  - `/unblocktag <tag>`
  - `/showblockedtags`

---

## 🚀 Deployment Instructions

### 1️⃣ Requirements

- Python 3.10+
- PostgreSQL database
- Required Python packages (in `requirements.txt`):

```
discord.py
feedparser
beautifulsoup4
sqlalchemy
psycopg2-binary
```

### 2️⃣ Environment Variables

- `DISCORD_TOKEN`: Your bot's secret token.
- `DATABASE_URL`: Your PostgreSQL connection string.

### 3️⃣ Setup & Initialization

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your PostgreSQL database and export your connection string as `DATABASE_URL`.
4. Run the database initialization once:
   ```bash
   python init_db.py
   ```
5. Launch the bot:
   ```bash
   python main.py
   ```

### 4️⃣ Hosting

- Optimized for Railway.app (Hobby Paid Plan recommended).
- Can be hosted on any platform supporting persistent PostgreSQL and Python.

---

## 📂 Project Structure

```
/requirements.txt
/init_db.py           # One-time table creation
/main.py              # Main bot code
/models.py            # SQLAlchemy table definitions
/database.py          # Database connection setup
/crud.py              # Database helper functions
```

---

## 🔐 Security Notes

- Keep your `DISCORD_TOKEN` and `DATABASE_URL` secure.
- Restrict slash command access using Discord role IDs.

---

## 📄 License

GNU General Public License v3.0 (GPL-3.0)

---

_Developed for fandom communities needing safe and automated fic updates with mod oversight._
_Last updated: [2025-07-21]_
_By: [NessaC]_
