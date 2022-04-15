from nextcord import *
from nextcord.ui import *

info = Embed(title="Image Module", description="Kitsune is the only command that uses the Nekoslife API. The rest are fetched from local storage", color=0x7DF9FF)
info.add_field(name='Available commands',
                 value="• Kitsune\n• Wallpaper\n• Jeanne\n• Saber\n• Neko")
info.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class infohelp(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="Userinfo"), SelectOption(
                label="Serverinfo"), SelectOption(label="Ping"), SelectOption(
                label="Stats"), SelectOption(label="Guild Banner"), SelectOption(
                label="Avatar"), SelectOption(label="Guild Avatar")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0]=="Userinfo":
            await ctx.response.defer(ephemeral=True)
            userinfo = Embed(color=0x7DF9FF)
            userinfo.add_field(
                name="See the information of a member or yourself. It will also show the member's banner if applicable", value="• **Example:** `/userinfo (if yourself)` \ `/userinfo MEMBER` (if member)")
            await ctx.edit_original_message(embed=userinfo, ephemeral=True)
        if self.values[0] == "Serverinfo":
            await ctx.response.defer(ephemeral=True)
            Serverinfo = Embed(color=0x7DF9FF)
            Serverinfo.add_field(
                name="Get information about this server", value="• **Example:** `/serverinfo`")
            await ctx.edit_original_message(embed=Serverinfo, ephemeral=True)
        if self.values[0] == "Ping":
            await ctx.response.defer(ephemeral=True)
            ping = Embed(color=0x7DF9FF)
            ping.add_field(
                name="Check how fast I can respond to commands", value="• **Example:** `/ping`")
            await ctx.edit_original_message(embed=ping, ephemeral=True)
        if self.values[0] == "Stats":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See the bot's status from development to now", value="• **Example:** `/stats`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Guild Banner":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See the server's banner\n• **NOTE:** If the server is not boosted to Level 2, it will return with a `Not boosted to Level 2` error. If the server doesn't have a banner, it will return with a footer text only.", value="• **Example:** `/guildbanner`\n• **Expected failure**: Server not boosted to level 2 error message or the server banner is not applicable")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Avatar":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See your avatar or a member's avatar", value="• **Example:** `/avatar` (if yourself) / `/avatar MEMBER` (if member)")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Guild Avatar":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See your guild avatar or a member's guild avatar\n• **NOTE:** If the member has no guild avatar set, it will return with their normal avatar.", value="• **Example:** `/guildavatar` (if yourself) / `/guildavatar MEMBER` (if member)")
            await ctx.edit_original_message(embed=saber, ephemeral=True)


class infoview(View):
    def __init__(self):
        super().__init__()
        self.add_item(infohelp())

        

