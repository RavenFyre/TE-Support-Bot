# Libraries to import:

import discord
from discord import Client, Intents, Embed, app_commands

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Templates for messages + embeds

# name_message_content = f""
# name_embed = discord.Embed(title="", description="", color=0x00FF00)

# Colours

# Nice green: #388e3c
# Blurple: #738adb
# Nice bright blue: #1da0f2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Posting the Multi-Language (English, Spanish, Portuguese & Arabic) Support Panel

multi_lang_message_content = f"**TLOU Esports - Support**\n\nIf you require support on the website or Discord server, please select one of the language options below, type in your username + reason for contacting support, and a new ticket will be created for you. This will allow you to communicate directly with a member of staff in a separate channel.\n\nTry to be patient when creating a new ticket. Note that staff are volunteers and may not always be available.\n\nPlease use this for genuine enquiries/problems. Our support team reserves the right to prohibit any person from using this service if it is used to repeatedly spam staff or violate our rules.\n\nDiscussions within such ticket sessions will remain confidential among staff. Tickets may be closed or deleted at any time at the discretion of support staff.\n\n**Spanish and Portuguese support are not currently available. We are sorry for the inconvenience.**"
multi_lang_embed = discord.Embed(title="Create a Support Ticket", description="**English Support**\nWhat language do you require support in?\n\n**Soporte Español**\n¿En qué idioma necesita soporte?\n\n**Suporte Português**\nEm que idioma você precisa de suporte?\n\n**الدعم العربي**\nبأي لغة تحتاج إلى الدعم؟", color=0x388e3c)

# Posting the English support panel with select drop-down menu to select a support category

english_support_message_content = f"**TLOU Esports - Support**\n\nIf you require assistance, have encountered a problem or simply wish to ask us a question regarding the TLOU Esports website or Discord server, we are here to help.\n\nPlease select one of the options from the drop-down menu below this message to get started!"
english_support_embed = discord.Embed(description="This service is intended to provide a smooth support experience and mis-use will not be tolerated. Please use this for genuine enquiries/problems and only select the options that apply the most. If none of the options apply, feel free to select 'Miscellaneous'.", color=0x388e3c)