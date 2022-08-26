"""
Copyright ( C ) GopiNath  
"""
import github

from pyrogram import filters
from Gbot import pgram

Queen_PYRO_Repo = filters.command("repo")


@pgram.on_message(Queen_PYRO_Repo)
@pgram.on_edited_message(Queen_PYRO_Repo)
async def give_repo(m):
    g = github.Github()
    repo = g.get_repo("Awesome-RJ/QueenBot")
    list_of_users = "".join(
        f"*{count}.* [{i.login}](https://github.com/{i.login})\n"
        for count, i in enumerate(repo.get_contributors(), start=1))

    text = f"""[Github](https://github.com/Awesome-RJ/QueenBot) | [support group](https://t.me/Black_Knights_Union_Support)
```----------------
| Contributors |
----------------```
{list_of_users}"""
    await m.reply(text, disable_web_page_preview=False)


__mod_name__ = "[✨ ᴄᴏɴᴛʀɪʙᴜᴛᴇʀꜱ ✨]"
