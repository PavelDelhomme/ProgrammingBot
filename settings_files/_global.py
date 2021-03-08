import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

DISCORD_BOT_TOKEN = os.getenv("token", False)

# Reddit Configuration
REDDIT_APP_ID = os.getenv("REDDIT_APP_ID", True)
REDDIT_APP_SECRET = os.getenv("REDDIT_APP_SECRET", True)
REDDIT_ENABLE_MEME_SUBREDDITS = [
        "funny",
        "memes",
        "jokes"
]
REDDIT_ENABLED_NSFW_SUBREDDITS = [
        "wtf"
]
REDDIT_ENABLED_SERIOUS_SUBREDDITS = [
        "news",
        "worldnews"
]
REDDIT_ENABLED_OTHER_SUBREDDITS = [
        "pics",
        "movies",
        "aww",
        "todayilearnd",
        "sciences",
        "politics",
        "gamin",
        "minecraft"
]
# Permissions

MODERATOR_ROLE_NAME = "Administrator"
