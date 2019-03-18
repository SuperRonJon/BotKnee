from secret import token
import discord

client = discord.Client()
sub_channel = None

current_queue = list()
is_open = True
num_to_remove = 3

swap_dict = dict()


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
            print('listening in {}'.format(channel.name))
            sub_channel = channel


@client.event
async def on_message(message):
    global current_queue
    global num_to_remove
    global sub_channel
    global swap_dict
    global is_open

    if message.author == client.user:
        return

    if message.channel.name == 'sub-games':
        if message.content.startswith('!q') or message.content.startswith('!Q') or message.content.startswith(
                '!queue') or message.content.startswith('!Queue'):
            if is_open:
                if message.author not in current_queue:
                    current_queue.append(message.author)
                    await client.send_message(message.channel, "Added {} to the queue".format(message.author.mention))
                    print('{}#{} added self to queue'.format(message.author.name, message.author.discriminator))
                else:
                    await client.send_message(message.channel,
                                              "{} is already in the queue".format(message.author.mention))
            else:
                await client.send_message(message.channel, "Sorry, the queue is currently closed.")

        if message.content.startswith('!adduser'):
            if is_moderator(message.author):
                if len(message.mentions) != 1:
                    await client.send_message(message.channel, "Invalid number of users mentioned, must be just 1")
                else:
                    player_to_add = message.mentions[0]
                    if player_to_add not in current_queue:
                        current_queue.append(player_to_add)
                        await client.send_message(message.channel,
                                                  "Added {} to the queue".format(player_to_add.mention))
                        print('{}#{} added {}#{} to queue'.format(message.author.name, message.author.discriminator,
                                                                  player_to_add.name, player_to_add.discriminator))
                    else:
                        await client.send_message(message.channel, "Player is already in the queue")
            else:
                await client.send_message(message.channel, "Only moderators can use this command")

        if message.content.startswith('!removeuser'):
            if is_moderator(message.author):
                if len(message.mentions) != 1:
                    await client.send_message(message.channel, "Invalid number of users mentioned")
                else:
                    player_to_remove = message.mentions[0]
                    if player_to_remove in current_queue:
                        current_queue.remove(player_to_remove)
                        await client.send_message(message.channel,
                                                  "{} has been removed from the queue".format(player_to_remove.mention))
                        print('{}#{} removed {}#{} from the queue'.format(message.author.name,
                                                                          message.author.discriminator,
                                                                          player_to_remove.name,
                                                                          player_to_remove.discriminator))
                    else:
                        await client.send_message(message.channel, "Player not in current queue, cannot remove")

        if message.content.startswith('!tofront'):
            if is_moderator(message.author):
                if len(message.mentions) != 1:
                    await client.send_message(message.channel, "Too many people mentioned")
                else:
                    # TODO: Make sure someone is mentioned
                    player_to_move = message.mentions[0]
                    if player_to_move in current_queue:
                        current_queue.remove(player_to_move)
                        current_queue.insert(0, player_to_move)
                        await client.send_message(message.channel, "{} has been moved to the front of the queue".format(
                            player_to_move.mention))
                        print('{}#{} moved {}#{} to the front of the queue'.format(message.author.name,
                                                                                   message.author.discriminator,
                                                                                   player_to_move.name,
                                                                                   player_to_move.discriminator))
                    else:
                        await client.send_message(message.channel, "Player not in queue")

        if message.content.startswith('!remove '):
            if message.author in current_queue:
                current_queue.remove(message.author)
                await client.send_message(message.channel, "Removed {} from the queue".format(message.author.mention))
                print('{}#{} removed self from the queue'.format(message.author.name, message.author.discriminator))
            else:
                await client.send_message(message.channel,
                                          "You can only remove yourself from the queue if you are in the queue...")

        if message.content.startswith('!swap '):
            if message.author in current_queue:
                if len(message.mentions) > 0:
                    swap_with = message.mentions[0]
                    if swap_with in current_queue:
                        if swap_with.name in swap_dict and swap_dict[swap_with.name] == message.author.name:
                            a, b = current_queue.index(message.author), current_queue.index(swap_with)
                            current_queue[b], current_queue[a] = current_queue[a], current_queue[b]
                            await client.send_message(message.channel,
                                                      "Successfully swapped {} and {}".format(message.author.mention,
                                                                                              swap_with.mention))
                            print("{} has swapped with {}".format(message.author, swap_with))
                            del swap_dict[swap_with.name]
                            if message.author.name in swap_dict:
                                del swap_dict[message.author.name]
                        else:
                            swap_dict[message.author.name] = swap_with.name
                            await client.send_message(message.channel,
                                                      "Initiating swap with {}".format(swap_with.mention))
                            print("{} initiating swap with {}".format(message.author, swap_with))
                    else:
                        await client.send_message(message.channel, "That user is not in the queue")

                else:
                    await client.send_message(message.channel, "Nobody mentioned to swap")
            else:
                await client.send_message(message.channel, "You must be in the queue to swap")

        if message.content.startswith('!swapusers'):
            if is_moderator(message.author):
                if len(message.mentions) == 2 and message.mentions[0] in current_queue and message.mentions[
                    1] in current_queue:
                    swap1 = message.mentions[0]
                    swap2 = message.mentions[1]

                    a, b = current_queue.index(swap1), current_queue.index(swap2)
                    current_queue[b], current_queue[a] = current_queue[a], current_queue[b]
                    await client.send_message(message.channel,
                                              "Successfully swapped {} and {}".format(swap1.mention, swap2.mention))
                else:
                    await client.send_message(message.channel, "Error swapping users")
            else:
                await client.send_message(message.channel, "You must be a moderator to swap other users")

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
            if is_moderator(message.author):
                content_split = message.content.split(' ')
                if len(content_split) == 2:
                    num_to_remove = int(content_split[1])
                    await client.send_message(message.channel,
                                              "Number of players per match changed to {}".format(content_split[1]))
                    print('{}#{} changed number of players to {}'.format(message.author.name,
                                                                         message.author.discriminator,
                                                                         content_split[1]))
                else:
                    await client.send_message(message.channel, "Error, invalid input for !number command")
            else:
                await client.send_message(message.channel, 'You must be a moderator to change this value')

        if message.content.startswith('!next'):
            if is_moderator(message.author):
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
            if is_moderator(message.author):
                current_queue = list()
                await client.send_message(message.channel, 'Queue reset')
                print('{}#{} reset the queue'.format(message.author.name, message.author.discriminator))
            else:
                await client.send_message(message.channel, 'Only moderators can reset the queue')

        if message.content.startswith('!close'):
            if is_moderator(message.author):
                is_open = False
                await client.send_message(message.channel, 'The queue is now CLOSED! You may no longer join the queue.')
            else:
                await client.send_message(message.channel, 'You must be a moderator to use this command')

        if message.content.startswith('!open'):
            if is_moderator(message.author):
                is_open = True
                await client.send_message(message.channel, 'The queue is now OPEN! You may join the queue again.')
            else:
                await client.send_message(message.channel, 'You must be a moderator to use this command')

        if message.content.startswith('!logout'):
            if is_moderator(message.author):
                print('Closing....')
                await client.logout()
    else:
        return


def is_moderator(user):
    user_roles = [str(role).lower() for role in user.roles]
    return 'moderator' in user_roles


client.run(token)
