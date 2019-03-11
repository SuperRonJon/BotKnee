from secret import token
import discord

client = discord.Client()
sub_channel = None

current_queue = list()
num_to_remove = 3


@client.event
async def on_ready():
    global sub_channel
    global admins
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    channels = client.get_all_channels()
    for channel in channels:
        if 'sub-games' in channel.name:
            print('Found sub channel...')
            sub_channel = channel


@client.event
async def on_message(message):
    global current_queue
    global num_to_remove
    global sub_channel

    if message.author == client.user:
        return

    if message.channel == sub_channel:
        print('Got message from {}#{}'.format(message.author.name, message.author.discriminator))

        if message.content.startswith('!q') or message.content.startswith('!Q') or message.content.startswith('!queue') or message.content.startswith('!Queue'):
            if message.author not in current_queue:
                current_queue.append(message.author)
                await client.send_message(message.channel, "Added {} to the queue".format(message.author.mention))
            else:
                await client.send_message(message.channel, "{} is already in the queue".format(message.author.mention))
        
        if message.content.startswith('!adduser'):
            user_roles = [str(role).lower() for role in message.author.roles]
            if 'moderator' in user_roles:
                if len(message.mentions) != 1:
                    await client.send_message(message.channel, "Invalid number of users mentioned, must be just 1")
                else:
                    player_to_add = message.mentions[0]
                    if player_to_add not in current_queue:
                        current_queue.append(player_to_add)
                        await client.send_message(message.channel, "Added {} to the queue".format(player_to_add.mention))
                    else:
                        await client.send_message(message.channel, "Player is already in the queue")
            else:
                await client.send_message(message.channel, "Only moderators can use this command")

        if message.content.startswith('!tofront'):
            user_roles = [str(role).lower() for role in message.author.roles]
            if 'moderator' in user_roles:
                if len(message.mentions) > 1:
                    await client.send_message(message.channel, "Too many people mentioned")
                else:
                    player_to_move = message.mentions[0]
                    if player_to_move in current_queue:
                        current_queue.remove(player_to_move)
                        current_queue.insert(0, player_to_move)
                        await client.send_message(message.channel, "{} has been moved to the front of the queue".format(player_to_move.mention))
                    else:
                        await client.send_message(message.channel, "Player not in queue")


        if message.content.startswith('!remove'):
            if message.author in current_queue:
                current_queue.remove(message.author)
                await client.send_message(message.channel, "Removed {} from the queue".format(message.author.mention))
            else:
                await client.send_message(message.channel, "You can only remove yourself from the queue if you are in the queue...")

        if message.content.startswith('!list'):
            user_mentions = ''
            in_queue = len(current_queue)

            if in_queue > 0:
                for user in current_queue:
                    user_mentions += user.name + ', '
                await client.send_message(message.channel, 'There are currently {} users in queue'.format(in_queue))
                await client.send_message(message.channel, user_mentions)
            else:
                await client.send_message(message.channel, 'The queue is currently empty')

        if message.content.startswith('!number'):
            user_roles = [str(role).lower() for role in message.author.roles]
            if 'moderator' in user_roles:
                content_split = message.content.split(' ')
                if len(content_split) == 2:
                    num_to_remove = int(content_split[1])
                    await client.send_message(message.channel, "Number of players per match changed to {}".format(content_split[1]))
                else:
                    await client.send_message(message.channel, "Error, invalid input for !number command")
            else:
                await client.send_message(message.channel, 'You must be a moderator to change this value')

        if message.content.startswith('!next'):
            user_roles = [str(role).lower() for role in message.author.roles]
            if 'moderator' in user_roles:
                next_users = list()
                for x in range(num_to_remove):
                    if len(current_queue) > 0:
                        next_users.append(current_queue.pop(0))
                user_mentions = ""
                for user in next_users:
                    user_mentions += user.mention + " "
                if user_mentions == "":
                    await client.send_message(message.channel, "There is nobody in the Queue!")
                else:
                    await client.send_message(message.channel, "Next up: {}".format(user_mentions))
            else:
                await client.send_message(message.channel, 'You must be a moderator to get the next users')

        if message.content.startswith('!reset'):
            user_roles = [str(role).lower() for role in message.author.roles]
            if 'moderator' in user_roles:
                current_queue = list()
                await client.send_message(message.channel, 'Queue reset')
            else:
                await client.send_message(message.channel, 'Only moderators can reset the queue')
        
        if message.content.startswith('!close'):
            user_roles = [str(role).lower() for role in message.author.roles]
            if 'moderator' in user_roles:
                client.close()
    else:
        return


client.run(token)
