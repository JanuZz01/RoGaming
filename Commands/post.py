import discord
from discord.ext import commands
import json
import requests

class CATEGORY(commands.Cog):
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
            return context.author == ctx.author
        
        try:
            with open(self.schema_path, "r") as f:
                data = json.loads(f.read())
                
                post = {}

                # Big boss didn't like this one
                await ctx.author.send("Hey! follow the steps below to start posting about your game")

                for x in range(len(list(data["Questions"]))):
                    question = list(data["Questions"])[x]
                    await ctx.author.send(question["Question"])
                    answer = await self.client.wait_for("message", check=Check, timeout=60)
                    post[question["Name"]] = answer.content

                print(post)

        except FileNotFoundError:
            await ctx.send("The schema for this question could not be found. Please contact a Moderator and show them this message")


    ## ____________ Events ____________ ##

    # Event
    # @commands.Cog.listener()


def setup(client):
    client.add_cog(CATEGORY(client))