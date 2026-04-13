Random Role Bot — version with slash commands

What changed:
- Token is read only from .env
- Guild ID is already hardcoded in bot.py
- Role list is stored in roles.json
- New slash commands:
  /addrole id-role
  /delrole id-role
  /checkid @role
  /allrole

Setup:
1. Create a .env file next to bot.py
2. Put this inside:
   DISCORD_TOKEN=YOUR_NEW_BOT_TOKEN
3. Install packages:
   py -m pip install -r requirements.txt
4. Start:
   py bot.py

Important:
- Enable SERVER MEMBERS INTENT in Discord Developer Portal
- The bot needs Manage Roles permission
- The bot's highest role must be above the roles it gives out
- Slash commands can take a short moment to appear after startup
