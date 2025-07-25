import discord
from discord.ext import tasks, commands
from discord import app_commands
import feedparser
import html
from bs4 import BeautifulSoup
import os

from crud import (get_blocked_tags, add_blocked_tag, remove_blocked_tag,
                  fic_already_posted, fic_already_denied,
                  log_posted_fic, log_denied_fic)

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 849836116479180810 # Replace with public feed channel ID
ADMIN_CHANNEL_ID = 1392897816396955759 # Replace with admin review channel ID
MOD_ROLE_IDS = {930538612754382869, 849835131182383145, 1386917677389582427, 1392541137415311410} # Replace with your mod/admin roles ID
FEED_URLS = ["https://archiveofourown.org/tags/31915957/feed.atom"]
BLOCKED_WARNINGS = {"Underage Sex"}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Helper Functions ---

def get_rating_color(ratings):
    if not ratings:
        return discord.Color.blue()
    rating = ratings[0].lower()
    if 'general' in rating:
        return discord.Color.green()
    if 'teen' in rating:
        return discord.Color.yellow()
    if 'mature' in rating:
        return discord.Color.orange()
    if 'explicit' in rating:
        return discord.Color.red()
    return discord.Color.blue()

def extract_links_and_raw(li):
    raw_items = []
    display_items = []
    for a in li.find_all('a'):
        name = a.text.strip()
        href = a.get('href')
        raw_items.append(name)
        if href:
            full_link = f"{href}"
            display_items.append(f"[{name}]({full_link})")
        else:
            display_items.append(name)
    return raw_items, display_items

def parse_fic_metadata(summary_html):
    decoded_html = html.unescape(summary_html)
    soup = BeautifulSoup(decoded_html, 'html.parser')
    metadata = {'ratings': [], 'warnings': [], 'fandoms': [], 'relationships': [],
                'characters': [], 'tags': [], 'words': None, 'chapters': None,
                'summary_text': None, 'series': None,
                'raw_warnings': [], 'raw_tags': []}
    paragraphs = soup.find_all('p')
	
	# Extract summary from second paragraph after author						
    metadata['summary_text'] = paragraphs[1].get_text().strip() if len(paragraphs) >= 2 else "No summary provided."
	
	# Extract series if present						   
    for p in paragraphs:
        if p.text.strip().startswith("Series:"):
            series_link = p.find('a')
            if series_link:
                name = series_link.text.strip()
                href = series_link.get('href')
                metadata['series'] = (name, f"{href}")
            break
    for li in soup.find_all('li'):
        label = li.text.split(':')[0].strip()
        raw_items, display_items = extract_links_and_raw(li)
        if label == "Rating":
            metadata['ratings'].extend(display_items)
        elif label == "Warnings":
            metadata['warnings'].extend(display_items)
            metadata['raw_warnings'].extend(raw_items)
        elif label == "Fandoms":
            metadata['fandoms'].extend(display_items)
        elif label == "Relationships":
            metadata['relationships'].extend(display_items)
        elif label == "Characters":
            metadata['characters'].extend(display_items)
        elif label == "Additional Tags":
            metadata['tags'].extend(display_items)
            metadata['raw_tags'].extend(raw_items)
    for p in soup.find_all('p'):
        text = p.get_text()
        if "Words:" in text:
            metadata['words'] = text.split("Words:")[1].split(",")[0].strip()
        if "Chapters:" in text:
            metadata['chapters'] = text.split("Chapters:")[1].split(",")[0].strip()
    return metadata

def safe_shorten_links(tags_list, limit=1024):
    result = ""
    for tag in tags_list:
        if len(result) + len(tag) + 2 > limit:
            break
        if result:
            result += ", "
        result += tag
    return result or "None"

def build_fic_embed(entry, metadata):
    embed_color = get_rating_color(metadata['ratings'])
    embed = discord.Embed(
        title=entry.title,
        url=entry.link,
        description=metadata['summary_text'] or "No summary provided.",
        color=embed_color
    )
    author_link = f"https://archiveofourown.org/users/{entry.author}".replace(" ", "%20")
    embed.add_field(name="Author", value=f"[{entry.author}]({author_link})", inline=False)
    if metadata.get('series'):
        name, link = metadata['series']
        embed.add_field(name="Series", value=f"[{name}]({link})", inline=False)
    embed.add_field(name="Words", value=metadata['words'] or "?", inline=True)
    embed.add_field(name="Chapters", value=metadata['chapters'] or "?", inline=True)
    embed.add_field(name="Rating(s)", value=safe_shorten_links(metadata['ratings']), inline=False)
    embed.add_field(name="Warning(s)", value=safe_shorten_links(metadata['warnings']), inline=False)
    embed.add_field(name="Fandom(s)", value=safe_shorten_links(metadata['fandoms']), inline=False)
    embed.add_field(name="Relationships", value=safe_shorten_links(metadata['relationships']), inline=False)
    embed.add_field(name="Characters", value=safe_shorten_links(metadata['characters']), inline=False)
    embed.add_field(name="Tags", value=safe_shorten_links(metadata['tags']), inline=False)
    return embed

# --- Discord UI ---

class FicReviewView(discord.ui.View):
    def __init__(self, entry, metadata, blocked_tags=None):
        super().__init__(timeout=None)
        self.entry = entry
        self.metadata = metadata
        self.blocked_tags = blocked_tags or []

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.id in MOD_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message("❌ You are not authorized to approve.", ephemeral=True)
            return
        log_posted_fic(self.entry.id)
        channel = bot.get_channel(CHANNEL_ID)
        embed = build_fic_embed(self.entry, self.metadata)
        await channel.send(embed=embed)
        await interaction.response.edit_message(
            content=f"📖 [{self.entry.title}]({self.entry.link}) has been posted to the public feed.\n✅ Approved by **{interaction.user.display_name}**.",
            embed=None,
            view=None
        )

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(role.id in MOD_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message("❌ You are not authorized to deny.", ephemeral=True)
            return
        log_denied_fic(self.entry.id)
        await interaction.response.edit_message(
            content=f"📖 [{self.entry.title}]({self.entry.link}) was blocked from public posting.\n❌ Fic denied by **{interaction.user.display_name}**.",
            embed=None,
            view=None
        )

# --- Bot Loop ---

@tasks.loop(hours=1)
async def check_rss_feeds():
    blocked_tags_db = get_blocked_tags()
    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if fic_already_posted(entry.id) or fic_already_denied(entry.id):
                continue
            metadata = parse_fic_metadata(entry.summary)
			# Hard block by warnings						
            if any(tag in BLOCKED_WARNINGS for tag in metadata['raw_warnings']):
                log_denied_fic(entry.id)
                continue
			# Soft block by additional tags							   
            blocked_tags = [tag for tag in metadata['raw_tags'] if tag in blocked_tags_db]
            if blocked_tags:
                admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
                embed = build_fic_embed(entry, metadata)
                embed.description = f"⚠️ Blocked Tag(s): {', '.join(blocked_tags)}\n\n" + (metadata['summary_text'] or "No summary provided.")
                view = FicReviewView(entry, metadata, blocked_tags)
                await admin_channel.send(embed=embed, view=view)
                continue
			# Auto-approve and post if clean								
            log_posted_fic(entry.id)
            channel = bot.get_channel(CHANNEL_ID)
            embed = build_fic_embed(entry, metadata)
            await channel.send(embed=embed)

# --- Slash Commands for Tag Management ---

# /blocktag
@bot.tree.command(name="blocktag", description="Add a tag to the blocked tags filter.")
async def block_tag(interaction: discord.Interaction, tag: str):
    if not any(role.id in MOD_ROLE_IDS for role in interaction.user.roles):
        await interaction.response.send_message("❌ You are not authorized to manage blocked tags.", ephemeral=True)
        return
    add_blocked_tag(tag)
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    await admin_channel.send(f"🚫 **{tag}** was added to the blocked tags by **{interaction.user.display_name}**.")
    await interaction.response.send_message(f"✅ Tag **{tag}** has been added to the blocked list.", ephemeral=True)

# /unblocktag
@bot.tree.command(name="unblocktag", description="Remove a tag from the blocked tags filter.")
async def unblock_tag(interaction: discord.Interaction, tag: str):
    if not any(role.id in MOD_ROLE_IDS for role in interaction.user.roles):
        await interaction.response.send_message("❌ You are not authorized to manage blocked tags.", ephemeral=True)
        return
    remove_blocked_tag(tag)
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    await admin_channel.send(f"✅ **{tag}** was removed from the blocked tags by **{interaction.user.display_name}**.")
    await interaction.response.send_message(f"✅ Tag **{tag}** has been removed from the blocked list.", ephemeral=True)

# /showblockedtags
@bot.tree.command(name="showblockedtags", description="Show the current list of blocked tags.")
async def show_blocked_tags(interaction: discord.Interaction):
    if not any(role.id in MOD_ROLE_IDS for role in interaction.user.roles):
        await interaction.response.send_message("❌ You are not authorized to view blocked tags.", ephemeral=True)
        return
    tags_list = get_blocked_tags()
    tags_text = ", ".join(sorted(tags_list)) if tags_list else "*(None)*"
    await interaction.response.send_message(f"🚫 **Current Blocked Tags:** {tags_text}", ephemeral=False)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    check_rss_feeds.start()

bot.run(TOKEN)
