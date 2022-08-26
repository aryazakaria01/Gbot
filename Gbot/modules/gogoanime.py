"""
Copyright ( C ) GopiNath  
"""

from gogoanimeapi import gogoanime as anime
from telethon import Button, events

from Gbot import telethn


@telethn.on(events.NewMessage(pattern="^/gogo ?(.*)"))
async def gogo(event):
    args = event.pattern_match.group(1)
    if not args:
        return await event.respond(
            "Your Query should be in This format: /search <space> Name of the Anime you want to Search."
        )
    result = anime.get_search_results(args)
    buttons = []
    for i in result:
        k = [Button.inline(f'{i["name"]}', data=f'search_{i["animeid"]}')]
        buttons.append(k)
        if len(buttons) == 99:
            break
    await event.reply("search", buttons=buttons)


@telethn.on(events.CallbackQuery(pattern=r"search(\_(.*))"))
async def search(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("_", 1)[1]
    animeid = input
    await event.answer("Fetching Anime Details")
    result = anime.get_anime_details(animeid)
    episodes = result["episodes"]
    nfo = f"{animeid}?{episodes}"
    buttons = Button.inline("Download", data=f"episode_{nfo}")
    text = """
{} (Released: {})
Type: {}
Status: {}
Generies: {}
Episodes: {}
Summary: {}
"""
    await event.edit(
        text.format(
            result["title"],
            result["year"],
            result["type"],
            result["status"],
            result["genre"],
            result["episodes"],
            result["plot_summary"],
        ),
        buttons=buttons,
    )


@telethn.on(events.CallbackQuery(pattern=r"episode(\_(.*))"))
async def episode(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("_", 1)[1]
    animeid, episodes = input.split("?", 1)
    animeid = animeid.strip()
    epsd = int(episodes.strip())
    buttons = []
    cbutton = []
    for i in range(epsd):
        nfo = f"{i}?{animeid}"
        button = Button.inline(f"{i}", data=f"download_{nfo}")
        buttons.append(button)
        if len(buttons) == 4:
            cbutton.append(buttons)
            buttons = []
    text = f"You selected {animeid},\n\nSelect the Episode you want :-"
    await event.edit(text, buttons=cbutton)


@telethn.on(events.CallbackQuery(pattern=r"download(\_(.*))"))
async def episode(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("_", 1)[1]
    imd, episode = input.split("?", 1)
    animeid = episode.strip()
    epsd = imd.strip()
    result = anime.get_episodes_link(animeid, epsd)
    text = f"You are watching Episode {epsd} of {animeid}:\n\nNote: Select HDP link for faster streaming."

    butons = []
    cbutton = []
    for i in result:
        if i != "title":
            k = Button.url(f"{i}", f"{result[i]}")
            butons.append(k)
            if len(butons) == 1:
                cbutton.append(butons)
                butons = []
    await event.edit(text, buttons=cbutton)
