# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# Frequently Used Code:

# To save a channel as a variable & send a message in that channel:
# channel_name = bot.get_channel(id)
# await channel_name.send()

# To link a channel in a message/embed:
# {channel_name.mention}

# To link a member and also display their name in text in a message/embed:
# {interaction.user.mention} *({interaction.user})*

# Creating and sending embedded messages with reactions & a View (button/select)
# embed = discord.Embed(description=f"**Title**\n\nDescription here.", timestamp=datetime.datetime.now(), color=0xFFA500)
# author = interaction.user
# pfp = author.display_avatar
# embed.set_thumbnail(url=pfp)
# bot_message = await channel_name.send(f"{interaction.user.mention}, here is your example embed, reaction buttons and a View!", embed=embed, view=NameOfViewClass())
# time.sleep(1)
# await bot_message.add_reaction("✅")
# await bot_message.add_reaction("❌")
# time.sleep(1)
# embed.set_footer(text=f"{bot.user.display_name} • Suggestion ID: {bot_message.id}")
# await bot_message.edit(f"{interaction.user.mention}, here is your example embed, reaction buttons and a View!", embed=embed, view=NameOfViewClass())

# To save a permissions overwrite
# Permissions Overwrite to View Pages
# see_the_page_overwrite = discord.PermissionOverwrite()
# see_the_page_overwrite.view_channel = True
# see_the_page_overwrite.send_messages = False
# see_the_page_overwrite.read_messages = True
# see_the_page_overwrite.read_message_history = True
# see_the_page_overwrite.add_reactions = False

# To set permissions:
# await channel_name.set_permissions(interaction.user, overwrite=see_the_page_overwrite, reason="Type a reason for the audit log here")

# To delay the bot
# time.sleep(5) # number of seconds

# To save a role as a variable:
# role_name = interaction.guild.get_role(id)

# To check if a member has a role:
# if role_name in interaction.user.roles:
    # enter code

# To add a role to a member:
# await interaction.user.add_roles(role_name)

# To edit a button after clicked:
# button.disabled = True
# button.label = "Type a new label here!"
# await interaction.response.edit_message(view=self)

# To edit / delete bot messages immediately after sent
# bot_message = await channel_name.send(embed=embed)
# await bot_message.edit(embed=embed)

# FILES FAQs

# How to record message IDs that the bot sends:
# example_msg = await interaction.channel.send("Example message")
# print(f"Message ID: {example_msg.id}")
# example_msg_id_doc = open(f"/home/container/Folder Name/Message_ID.txt", "w+")
# example_msg_id_doc.write(f"{example_msg.id}")
# example_msg_id_doc.close
# print(f"Message ID successfully updated in document!")

# How to check for specific message by an ID previously recorded:
# suggestion_panel_id_doc = open(f"/home/container/TE Suggestions/Suggestion_Panel_ID.txt", "r")
# suggestion_panel_id = suggestion_panel_id_doc.read()
# suggestion_panel = await channel_name.fetch_message(suggestion_panel_id)
# suggestion_panel_id_doc.close

# How to send a picture:
# with open('Sample.png', 'rb') as f:
#     picture = discord.File(f)
#     await channel_name.send(file=picture)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
