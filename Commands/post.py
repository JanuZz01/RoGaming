import discord
from discord.ext import commands
import json
import requests
from datetime import datetime
from secrets import * 

class Advertising(commands.Cog):
    def __init__(self, client):
        self.client = client

        ## ____________ Variables ____________ ## 
        self.schema_path = "post_schemas\game-event.json"

        

    ## ____________ Commands ____________ ##

    # Command
    @commands.command()
    async def post(self, ctx):
        await ctx.send("Check your dm's a thread just started!")

        def Check(context):
            return context.author == ctx.author and isinstance(context.channel, discord.channel.DMChannel)

        def post(post : object):
            print(post)

        async def Ask(ctx, data : object, index : int, post : object, max_index : int,timeout :int = 60, check : callable = Check, next_ : callable = None):
            
            retry = lambda: Ask(ctx,data, index, post, max_index,timeout,check, next_)

            question = list(data["Questions"])[index]
            await ctx.author.send(question["Question"])
            
            try:
                answer = await self.client.wait_for("message", check=Check, timeout=60)
            except TimeoutError:
                await ctx.send("Thread closed due to timeout")
            
            value = answer.content

            if(question["Format"] == "Number"):
                try:
                    value = int(value)
                except ValueError:
                    await retry()
                if(value < 0):
                    print(value)
                    print(type(value))
                    await retry()
            elif(question["Format"] == "Date"):
                try:
                    value = datetime.timestamp(datetime.strptime(value, "%H:%M %d/%m/%y").date())
                    print(value)
                except ValueError:
                    await retry()
            elif(question["Format"] == "Text"):
                try:
                    if(value.title() in question["Choises"]):
                        pass
                    else:
                        await retry()
                except KeyError:
                    pass     

            if(value == None):
                await retry()

            post[question["Name"]] = value
            print(post)

            if(index+1 <= max_index):
                await Ask(ctx, data, index+1, post, max_index, timeout, check, next_)
            else:
                if(next_):
                    next_(post)
                    
        
        try:
            with open(self.schema_path, "r") as f:
                data = json.loads(f.read())
                
                # Big boss didn't like this one
                await ctx.author.send("Hey! follow the steps below to start posting about your game")

                questions_len = len(list(data["Questions"]))

                try:
                    await Ask(ctx, data, 0, {}, questions_len-1, next_=post)
                except TimeoutError:
                    await ctx.author.send("Thread stopped it took too long")

        except FileNotFoundError:
            await ctx.send("The schema for this question could not be found. Please contact a Moderator and show them this message")


    ## ____________ Events ____________ ##

    # Event
    # @commands.Cog.listener()


def setup(client):
    client.add_cog(Advertising(client))