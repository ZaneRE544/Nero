from assets.components import Confirmation
from functions import (
    AutoCompleteChoices,
    Currency,
    Inventory,
    check_botbanned_app_command,
    check_disabled_app_command,
)
from discord import Color, Embed, File, Interaction, app_commands as Jeanne
from PIL import UnidentifiedImageError
from discord.ext.commands import Bot, GroupCog
from assets.generators.profile_card import Profile
from requests import exceptions
from reactionmenu import ViewButton, ViewMenu


class Shop_Group(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Check all the wallpapers available")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def backgrounds(self, ctx: Interaction):
        await ctx.response.defer()
        wallpapers = Inventory().fetch_wallpapers()
        embed = Embed()
        menu = ViewMenu(
            ctx,
            menu_type=ViewMenu.TypeEmbed,
            disable_items_on_timeout=True,
            style="Page $/&",
        )
        embed.color = Color.random()
        for wallpaper in wallpapers:
            page_embed = Embed(title=f"Item ID: {wallpaper[0]}", color=embed.color)
            page_embed.add_field(name="Name", value=str(wallpaper[1]), inline=True)
            page_embed.add_field(
                name="Price", value="1000 <:quantumpiece:1161010445205905418>"
            )
            page_embed.set_image(url=str(wallpaper[2]))
            menu.add_page(embed=page_embed)
        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()


class Background_Group(GroupCog, name="background"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Buy a background pic for your level card")
    @Jeanne.describe(name="Which background you are buying?")
    @Jeanne.autocomplete(name=AutoCompleteChoices.get_all_wallpapers)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def buy(self, ctx: Interaction, name: str):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if balance == 0:
            nomoney = Embed(
                description="You have no QP.\nPlease get QP by doing `/daily`, `/guess`, `/flip` and/or `/dice`"
            )
            await ctx.followup.send(embed=nomoney)
            return
        if balance < 1000:
            notenough = Embed(
                description="You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess`, `/flip` and/or `/dice`"
            )
            await ctx.followup.send(embed=notenough)
            return
        try:
            Inventory.get_wallpaper(name)
        except:
            await ctx.followup.send(
                embed=Embed(description="Unable to find wallpaper", color=Color.red())
            )
            return
        image_url = Inventory().get_wallpaper(name)[1]
        await ctx.followup.send(
            "Creating preview... This will take some time <a:loading:1161038734620373062>"
        )
        image = await Profile(self.bot).generate_profile(ctx.user, image_url, True)
        file = File(fp=image, filename=f"preview_profile_card.png")
        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.random(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
        )
        view = Confirmation(ctx.user)
        await ctx.edit_original_response(
            content=None, attachments=[file], embed=preview, view=view
        )
        await view.wait()
        if view.value == None:
            await ctx.edit_original_response(
                content="Timeout", view=None, embed=None, attachments=[]
            )
            return
        if view.value == True:
            await Inventory(ctx.user).add_user_wallpaper(name)
            embed1 = Embed(
                description=f"Background wallpaper bought and selected",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None)
        else:
            await ctx.edit_original_response(
                content="Cancelled", view=None, embed=None, attachments=[]
            )

    @buy.error
    async def buy_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already tried to preview this background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(description="Select a wallpaper")
    @Jeanne.autocomplete(name=AutoCompleteChoices.list_all_user_inventory)
    @Jeanne.describe(name="What is the name of the background?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def use(self, ctx: Interaction, name: str):
        await ctx.response.defer()
        try:
            await Inventory(ctx.user).use_wallpaper(name)
            embed = Embed(description=f"{name} has been selected", color=Color.random())
            await ctx.followup.send(embed=embed)
        except:
            embed = Embed(
                description="This background image is not in your inventory",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="buy-custom", description="Buy a custom background pic for your level card"
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.describe(name="What will you name it?", link="Add an image link")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def buycustom(self, ctx: Interaction, name: str, link: str):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if balance is None or balance < 1000:
            nomoney = Embed(description="You do not have enough QP.")
            await ctx.followup.send(embed=nomoney)
            return
        await ctx.followup.send(
            "Creating preview... This will take some time <a:loading:1161038734620373062>"
        )
        image = await Profile(self.bot).generate_profile(ctx.user, link, True)
        if image == False:
            size_error = Embed(
                description="The image is below the 900x500 size.\nPlease enlarge the image and try again"
            )
            await ctx.edit_original_response(content=None, embed=size_error)
            return
        file = File(fp=image, filename=f"preview_profile_card.png")
        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.blue(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
            .set_footer(
                text="Please note that if the custom background violates ToS or is NSFW, it will be removed with NO REFUNDS!"
            )
        )
        view = Confirmation(ctx.user)
        await ctx.edit_original_response(
            content=None, embed=preview, attachments=[file], view=view
        )
        await view.wait()
        if view.value:
            await Inventory(ctx.user).add_user_custom_wallpaper(name, link)
            embed1 = Embed(
                description="Background wallpaper bought and selected",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None, attachments=[])
        else:
            await ctx.edit_original_response(
                content="Cancelled", embed=None, view=None, attachments=[]
            )

    @buycustom.error
    async def buycustom_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already tried to preview this background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.response.send_message(embed=cooldown)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original,
            (
                exceptions.MissingSchema,
                exceptions.ConnectionError,
                UnidentifiedImageError,
            ),
        ):
            embed = Embed(description="Invalid image URL", color=Color.red())
            await ctx.edit_original_response(content=None, embed=embed)

    @Jeanne.command(description="Check which backgrounds you have")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def list(self, ctx: Interaction):
        await ctx.response.defer()
        if Inventory(ctx.user).get_user_inventory == None:
            embed = Embed(description="Your inventory is empty", color=Color.red())
            await ctx.followup.send(embed=embed)
            return
        a = Inventory(ctx.user).get_user_inventory
        embed = Embed()
        menu = ViewMenu(
            ctx,
            menu_type=ViewMenu.TypeEmbed,
            disable_items_on_timeout=True,
            style="Page $/&",
        )
        embed.color = Color.random()
        for wallpaper in a:
            page_embed = Embed(color=embed.color)
            page_embed.add_field(name="Name", value=str(wallpaper[1]), inline=True)
            page_embed.set_image(url=str(wallpaper[2]))
            menu.add_page(embed=page_embed)
        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()


async def setup(bot: Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))