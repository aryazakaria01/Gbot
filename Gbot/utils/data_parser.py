import requests
import contextlib
import time

from bs4 import BeautifulSoup
from Gbot.utils.helper import cflag, make_it_rw, pos_no, return_json_senpai, day_, season_
from Gbot import QUEEN_PTB

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from jikanpy import AioJikan
from datetime import datetime

ANIME_DB, MANGA_DB, CHAR_DB = {}, {}, {}

#### Anilist part ####

ANIME_TEMPLATE = """{name}
\n➛ **TYPE:** `{formats}`{dura}{avscd}{user_data}
{status_air}{gnrs_}
\n🎬 {trailer_link}
📖 <a href="{surl}">Synopsis</a>
📖 <a href="{url}">Official Site</a>
{additional}"""

# GraphQL Queries.
ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
    }
    genres
    tags {
      name
    }
    averageScore
    relations {
      edges {
        node {
          title {
            romaji
            english
          }
          id
        }
        relationType
      }
    }
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    isAdult
    isFavourite
    mediaListEntry {
      status
      score
      id
    }
    siteUrl
  }
}
"""

ISADULT = """
query ($id: Int) {
  Media (id: $id) {
    isAdult
  }
}
"""

BROWSE_QUERY = """
query ($s: MediaSeason, $y: Int, $sort: [MediaSort]) {
  Page {
    media (season: $s, seasonYear: $y, sort: $sort) {
    	title {
        romaji
      }
      format
    }
  }
}
"""

FAV_ANI_QUERY = """
query ($id: Int, $page: Int) {
  User (id: $id) {
    favourites {
      anime (page: $page, perPage: 10) {
        pageInfo {
          lastPage
        }
        edges {
          node {
            title {
              romaji
            }
            siteUrl
          }
        }
      }
    }
  }
}
"""

FAV_MANGA_QUERY = """
query ($id: Int, $page: Int) {
  User (id: $id) {
    favourites {
      manga (page: $page, perPage: 10) {
        pageInfo {
          lastPage
        }
        edges {
          node {
            title {
              romaji
            }
            siteUrl
          }
        }
      }
    }
  }
}
"""

FAV_CHAR_QUERY = """
query ($id: Int, $page: Int) {
  User (id: $id) {
    favourites {
      characters (page: $page, perPage: 10) {
        pageInfo {
          lastPage
        }
        edges {
          node {
            name {
              full
            }
            siteUrl
          }
        }
      }
    }
  }
}
"""

VIEWER_QRY = """
query {
  Viewer{
    id
    name
    siteUrl
    statistics {
      anime {
        count
        minutesWatched
        episodesWatched
        meanScore
      }
      manga {
        count
        chaptersRead
        volumesRead
        meanScore
      }
    }
  }
}
"""

USER_QRY = """
query ($search: String) {
  User (name: $search) {
    id
    name
    siteUrl
    statistics {
      anime {
        count
        minutesWatched
        episodesWatched
        meanScore
      }
      manga {
        count
        chaptersRead
        volumesRead
        meanScore
      }
    }
  }
}
"""

ANIME_MUTATION = """
mutation ($id: Int) {
  ToggleFavourite (animeId: $id) {
    anime {
      pageInfo {
        total
      }
    }
  }
}"""

MANGA_MUTATION = """
mutation ($id: Int) {
  ToggleFavourite (mangaId: $id) {
    manga {
      pageInfo {
        total
      }
    }
  }
}"""

CHAR_MUTATION = """
mutation ($id: Int) {
  ToggleFavourite (characterId: $id) {
    characters {
      pageInfo {
        total
      }
    }
  }
}"""

ANILIST_MUTATION = """
mutation ($id: Int, $status: MediaListStatus) {
  SaveMediaListEntry (mediaId: $id, status: $status) {
    media {
      title {
        romaji
      }
    }
  }
}"""

ANILIST_MUTATION_UP = """
mutation ($id: [Int], $status: MediaListStatus) {
  UpdateMediaListEntries (ids: $id, status: $status) {
    media {
      title {
        romaji
      }
    }
  }
}"""

ANILIST_MUTATION_DEL = """
mutation ($id: Int) {
  DeleteMediaListEntry (id: $id) {
    deleted
  }
}"""

AIR_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    title {
      romaji
      english
    }
    status
    countryOfOrigin
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    siteUrl
    isFavourite
    mediaListEntry {
      status
      id
    }
  }
}
"""

DES_INFO_QUERY = """
query ($id: Int) {
  Media (id: $id) {
    id
    description (asHtml: false)
  }
}
"""

CHA_INFO_QUERY = """
query ($id: Int, $page: Int) {
  Media (id: $id, type: ANIME) {
    id
    characters (page: $page, perPage: 25, sort: ROLE) {
      pageInfo {
        lastPage
        total
      }
      edges {
        node {
        	name {
          	full
        	}
        }
        role
      }
    }
  }
}
"""

REL_INFO_QUERY = """
query ($id: Int) {
  Media (id: $id, type: ANIME) {
    id
    relations {
      edges {
        node {
          title {
            romaji
          }
        }
        relationType
      }
    }
  }
}
"""

PAGE_QUERY = """
query ($search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo {
      total
    }
    media (search: $search, type: ANIME) {
      id
      idMal
      title {
        romaji
        english
        native
      }
      format
      status
      episodes
      duration
      countryOfOrigin
      source (version: 2)
      trailer {
        id
        site
      }
      genres
      tags {
        name
      }
      averageScore
      relations {
        edges {
          node {
            title {
              romaji
              english
            }
          }
          relationType
          }
        }
      nextAiringEpisode {
        timeUntilAiring
        episode
      }
      isAdult
      isFavourite
      mediaListEntry {
        status
        score
        id
      }
      siteUrl
    }
  }
}
"""

CHARACTER_QUERY = """
query ($id: Int, $search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo{
      total
    }
    characters (id: $id, search: $search) {
      id
      name {
        full
        native
      }
      image {
        large
      }
      isFavourite
      siteUrl
    }
  }
}
"""

MANGA_QUERY = """
query ($search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo {
      total
    }
    media (search: $search, type: MANGA) {
      id
      title {
        romaji
        english
        native
      }
      format
      countryOfOrigin
      source (version: 2)
      status
      description(asHtml: true)
      chapters
      isFavourite
      mediaListEntry {
        status
        score
        id
      }
      volumes
      averageScore
      siteUrl
      isAdult
    }
  }
}
"""

DESC_INFO_QUERY = """
query ($id: Int) {
	Character (id: $id) {
    image {
      large
    }
    description(asHtml: false)
  }
}
"""

LS_INFO_QUERY = """
query ($id: Int) {
	Character (id: $id) {
    image {
      large
    }
    media (page: 1, perPage: 25) {
      nodes {
        title {
          romaji
          english
        }
        type
      }
    }
  }
}
"""

ACTIVITY_QUERY = """
query ($id: Int) {
  Page (perPage: 12) {
  	activities (userId: $id, type: MEDIA_LIST, sort: ID_DESC) {
			...kek
  	}
  }
}
fragment kek on ListActivity {
  type
  media {
    title {
      romaji
    }
    siteUrl
  }
  progress
  status
}
"""

TOP_QUERY = """
query ($gnr: String, $page: Int) {
  Page (perPage: 15, page: $page) {
    pageInfo {
      lastPage
      total
    }
    media (genre: $gnr, sort: SCORE_DESC, type: ANIME) {
      title {
        romaji
      }
    }
  }
}
"""

TOPT_QUERY = """
query ($gnr: String, $page: Int) {
  Page (perPage: 15, page: $page) {
    pageInfo {
      lastPage
      total
    }
    media (tag: $gnr, sort: SCORE_DESC, type: ANIME) {
      title {
        romaji
      }
    }
  }
}
"""

ALLTOP_QUERY = """
query ($page: Int) {
  Page (perPage: 15, page: $page) {
    pageInfo {
      lastPage
      total
    }
    media (sort: SCORE_DESC, type: ANIME) {
      title {
        romaji
      }
    }
  }
}
"""

GET_GENRES = """
query {
  GenreCollection
}
"""

GET_TAGS = """
query{
  MediaTagCollection {
    name
    isAdult
  }
}
"""


async def get_all_tags(text: str = None):
    vars_ = {}
    result = await return_json_senpai(GET_TAGS, vars_, auth=False, user=None)
    msg = "**Tags List:**\n\n`"
    kek = []
    for i in result['data']['MediaTagCollection']:
        if text is not None and 'nsfw' in text:
            if str(i['isAdult']) != 'False':
                kek.append(i['name'])
        else:
            if str(i['isAdult']) == 'False':
                kek.append(i['name'])
    msg += ", ".join(kek)
    msg += "`"
    return msg


async def get_all_genres():
    vars_ = {}
    result = await return_json_senpai(GET_GENRES, vars_, auth=False)
    msg = "**Genres List:**\n\n"
    for i in result['data']['GenreCollection']:
        msg += f"`{i}`\n"
    return msg


async def get_user_activity(id_, user):
    vars_ = {"id": id_}
    result = await return_json_senpai(ACTIVITY_QUERY,
                                      vars_,
                                      auth=True,
                                      user=user)
    data = result["data"]["Page"]["activities"]
    msg = ""
    for i in data:
        with contextlib.suppress(KeyError):
            name = f"[{i['media']['title']['romaji']}]({i['media']['siteUrl']})"
            if i['status'] in ["watched episode", "read chapter"]:
                msg += f"⚬ {str(i['status']).capitalize()} {i['progress']} of {name}\n"
            else:
                progress = i['progress']
                of = "of"
                if i['status'] == "dropped":
                    of = "at"
                msg += f"⚬ {str(i['status']).capitalize()}{f'{progress} {of} ' if progress is not None else ' '}{name}\n"
    btn = [[InlineKeyboardButton("Back", callback_data=f"getusrbc_{user}")]]
    return f"https://img.anili.st/user/{id_}?a={time.time()}", msg, InlineKeyboardMarkup(
        btn)


async def get_top_animes(gnr: str, page, user):
    vars_ = {"gnr": gnr.lower(), "page": int(page)}
    query = TOP_QUERY
    msg = f"Top animes for genre `{gnr.capitalize()}`:\n\n"
    if gnr == "None":
        query = ALLTOP_QUERY
        vars_ = {"page": int(page)}
        msg = "Top animes:\n\n"
    nsfw = False
    result = await return_json_senpai(query, vars_, auth=False, user=user)
    if len(result['data']['Page']['media']) == 0:
        query = TOPT_QUERY
        msg = f"Top animes for tag `{gnr.capitalize()}`:\n\n"
        result = await return_json_senpai(query, vars_, auth=False, user=user)
        if len(result['data']['Page']['media']) == 0:
            return ["No results Found"]
        nsls = await get_all_tags('nsfw')
        nsfw = gnr.lower() in nsls.lower()
    data = result["data"]["Page"]
    for i in data['media']:
        msg += f"⚬ `{i['title']['romaji']}`\n"
    msg += f"\nTotal available animes: `{data['pageInfo']['total']}`"
    btn = []
    if int(page) == 1:
        if int(data['pageInfo']['lastPage']) != 1:
            btn.append([
                InlineKeyboardButton(
                    "Next",
                    callback_data=f"topanimu_{gnr}_{int(page)+1}_{user}")
            ])
    elif int(page) == int(data['pageInfo']['lastPage']):
        btn.append([
            InlineKeyboardButton(
                "Prev", callback_data=f"topanimu_{gnr}_{int(page)-1}_{user}")
        ])
    else:
        btn.append([
            InlineKeyboardButton(
                "Prev", callback_data=f"topanimu_{gnr}_{int(page)-1}_{user}"),
            InlineKeyboardButton(
                "Next", callback_data=f"topanimu_{gnr}_{int(page)+1}_{user}")
        ])
    return [msg, nsfw], InlineKeyboardMarkup(btn) if len(btn) != 0 else ""


async def get_user_favourites(id_, user, req, page, sighs):
    vars_ = {"id": int(id_), "page": int(page)}
    result = await return_json_senpai(
        FAV_ANI_QUERY if req == "ANIME" else
        FAV_CHAR_QUERY if req == "CHAR" else FAV_MANGA_QUERY,
        vars_,
        auth=True,
        user=int(user))
    data = result["data"]["User"][
        "favourites"]["anime" if req == "ANIME" else "characters" if req ==
                      "CHAR" else "manga"]
    msg = "Favourite Animes:\n\n" if req == "ANIME" else "Favourite Characters:\n\n" if req == "CHAR" else "Favourite Manga:\n\n"
    for i in data["edges"]:
        msg += f"⚬ [{i['node']['title']['romaji'] if req!='CHAR' else i['node']['name']['full']}]({i['node']['siteUrl']})\n"
    btn = []
    if int(page) == 1:
        if int(data['pageInfo']['lastPage']) != 1:
            btn.append([
                InlineKeyboardButton(
                    "Next",
                    callback_data=
                    f"myfavqry_{req}_{id_}_{str(int(page)+1)}_{sighs}_{user}")
            ])
    elif int(page) == int(data['pageInfo']['lastPage']):
        btn.append([
            InlineKeyboardButton(
                "Prev",
                callback_data=
                f"myfavqry_{req}_{id_}_{str(int(page)-1)}_{sighs}_{user}")
        ])
    else:
        btn.append([
            InlineKeyboardButton(
                "Prev",
                callback_data=
                f"myfavqry_{req}_{id_}_{str(int(page)-1)}_{sighs}_{user}"),
            InlineKeyboardButton(
                "Next",
                callback_data=
                f"myfavqry_{req}_{id_}_{str(int(page)+1)}_{sighs}_{user}")
        ])
    btn.append([
        InlineKeyboardButton("Back",
                             callback_data=f"myfavs_{id_}_{sighs}_{user}")
    ])
    return f"https://img.anili.st/user/{id_}?a=({time.time()})", msg, InlineKeyboardMarkup(
        btn)


async def get_featured_in_lists(idm,
                                req,
                                auth: bool = False,
                                user: int = None,
                                page: int = 0):
    vars_ = {"id": int(idm)}
    result = await return_json_senpai(LS_INFO_QUERY,
                                      vars_,
                                      auth=auth,
                                      user=user)
    data = result["data"]["Character"]["media"]["nodes"]
    if req == "ANI":
        out = "ANIMES:\n\n"
        out_ = []
        for ani in data:
            k = ani["title"]["english"] or ani["title"]["romaji"]
            kk = ani["type"]
            if kk == "ANIME":
                out_.append(f"➛ __{k}__\n")
    else:
        out = "MANGAS:\n\n"
        out_ = []
        for ani in data:
            k = ani["title"]["english"] or ani["title"]["romaji"]
            kk = ani["type"]
            if kk == "MANGA":
                out_.append(f"➛ __{k}__\n")
    total = len(out_)
    for _ in range(15 * page):
        out_.pop(0)
    out_ = "".join(out_[:15])
    return ([out + out_, total] if len(out_) != 0 else
            False), result["data"]["Character"]["image"]["large"]


async def get_additional_info(idm, req, ctgry, page: int = 0):
    vars_ = {"id": int(idm)}
    if req == 'char':
        vars_['page'] = page
    result = await return_json_senpai(
        ((DES_INFO_QUERY if req == "desc" else CHA_INFO_QUERY if req == "char"
          else REL_INFO_QUERY) if ctgry == "ANI" else DESC_INFO_QUERY),
        vars_,
    )
    data = result["data"]["Media"] if ctgry == "ANI" else result["data"][
        "Character"]
    pic = f"https://img.anili.st/media/{idm}"
    if req == "desc":
        synopsis = data.get("description")
        return (pic if ctgry == "ANI" else data["image"]["large"]), synopsis
    elif req == "char":
        charlist = []
        for char in data["characters"]['edges']:
            charlist.append(
                f"`➛ {char['node']['name']['full']} `({char['role']})")
        chrctrs = ("\n").join(charlist)
        charls = f"`{chrctrs}`" if len(charlist) != 0 else ""
        return pic, charls, data["characters"]['pageInfo']
    else:
        prqlsql = data.get("relations").get("edges")
        ps = ""
        for i in prqlsql:
            ps += f'➛ {i["node"]["title"]["romaji"]} `{i["relationType"]}`\n'
        return pic, ps


async def get_anime(vars_, auth: bool = False, user: int = None):
    result = await return_json_senpai(ANIME_QUERY, vars_, auth=auth, user=user)

    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"[{error_sts}]"]

    data = result["data"]["Media"]

    # Data of all fields in returned json
    # pylint: disable=possibly-unused-variable
    idm = data.get("id")
    idmal = data.get("idMal")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    native = data["title"]["native"]
    formats = data.get("format")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    country = data.get("countryOfOrigin")
    c_flag = cflag(country)

    prqlsql = data.get("relations").get("edges")
    adult = data.get("isAdult")
    url = data.get("siteUrl")
    trailer_link = "N/A"
    gnrs = ", ".join(data['genres'])
    score = data['averageScore']
    avscd = f"\n➛ **SCORE:** `{score}%` 🌟" if score is not None else ""
    tags = []
    for i in data['tags']:
        tags.append(i["name"])
    tags_ = f"\n➛ **TAGS:** `{', '.join(tags[:5])}`" if tags != [] else ""
    bot = "Gbot"
    gnrs_ = ""
    if len(gnrs) != 0:
        gnrs_ = f"\n➛ **GENRES:** `{gnrs}`"
    isfav = data.get("isFavourite")
    fav = ", in Favourites" if isfav is True else ""
    user_data = ""
    in_ls = False
    in_ls_id = ""
    if auth is True:
        in_list = data.get("mediaListEntry")
        if in_list is not None:
            in_ls = True
            in_ls_id = in_list['id']
            in_ls_stts = in_list['status']
            in_ls_score = f" and scored {in_list['score']}" if in_list[
                'score'] != 0 else ""
            user_data = f"\n➛ **USER DATA:** `{in_ls_stts}{fav}{in_ls_score}`"
    if data["title"]["english"] is not None:
        name = f"""**{romaji}** | `{english}`"""
    else:
        name = f"""[{c_flag}]**{romaji}**"""
    prql, prql_id, sql, sql_id = "", "None", "", "None"
    for i in prqlsql:
        if i["relationType"] == "PREQUEL":
            pname = (i["node"]["title"]["english"]
                     if i["node"]["title"]["english"] is not None else
                     i["node"]["title"]["romaji"])
            prql += f"**PREQUEL:** `{pname}`\n"
            prql_id = i["node"]["id"]
            break
    for i in prqlsql:
        if i["relationType"] == "SEQUEL":
            sname = (i["node"]["title"]["english"]
                     if i["node"]["title"]["english"] is not None else
                     i["node"]["title"]["romaji"])
            sql += f"**SEQUEL:** `{sname}`\n"
            sql_id = i["node"]["id"]
            break
    additional = f"{prql}{sql}"
    surl = f"https://t.me/{bot}/?start=des_ANI_{idm}"
    dura = (f"\n➛ **DURATION:** `{duration} min/ep`"
            if duration is not None else "")
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["timeUntilAiring"]
        air_on = make_it_rw(nextAir * 1000)
        eps = data["nextAiringEpisode"]["episode"]
        th = pos_no(str(eps))
        air_on += f"\n➛ **EPISODES:** `{eps}`"
    if air_on is None:
        eps_ = f"{episodes}" if episodes is not None else ""
        status_air = f"➛ **STATUS:** `{status}`\n➛ **EPISODES:** `{eps_}`"
    else:
        status_air = f"➛ **STATUS:** `{status}`\n➛ **NEXT AIRING:** {air_on}"
    if data["trailer"] and data["trailer"]["site"] == "youtube":
        trailer_link = f"<a href='https://youtu.be/{data['trailer']['id']}'>Trailer</a>"
    title_img = f"https://img.anili.st/media/{idm}"
    try:
        finals_ = ANIME_TEMPLATE.format(**locals())
    except KeyError as kys:
        return [f"{kys}"]
    return title_img, finals_, [idm, in_ls, in_ls_id, isfav,
                                str(adult)], prql_id, sql_id


async def get_anilist(qdb, page, auth: bool = False, user: int = None):
    vars_ = {"search": ANIME_DB[qdb], "page": page}
    result = await return_json_senpai(PAGE_QUERY, vars_, auth=auth, user=user)

    if len(result['data']['Page']['media']) == 0:
        return ["No results Found"]

    data = result["data"]["Page"]["media"][0]
    # Data of all fields in returned json
    # pylint: disable=possibly-unused-variable
    idm = data.get("id")
    bot = "Gbot"
    idmal = data.get("idMal")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    native = data["title"]["native"]
    formats = data.get("format")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    country = data.get("countryOfOrigin")
    c_flag = cflag(country)
    source = data.get("source")
    prqlsql = data.get("relations").get("edges")
    adult = data.get("isAdult")
    trailer_link = "N/A"
    isfav = data.get("isFavourite")
    gnrs = ", ".join(data['genres'])
    gnrs_ = ""
    if len(gnrs) != 0:
        gnrs_ = f"\n➛ **GENRES:** `{gnrs}`"
    fav = ", in Favourites" if isfav is True else ""
    score = data['averageScore']
    avscd = f"\n➛ **SCORE:** `{score}%` 🌟" if score is not None else ""
    tags = []
    for i in data['tags']:
        tags.append(i["name"])
    tags_ = f"\n➛ **TAGS:** `{', '.join(tags[:5])}`" if tags != [] else ""
    in_ls = False
    in_ls_id = ""
    user_data = ""
    if auth is True:
        in_list = data.get("mediaListEntry")
        if in_list is not None:
            in_ls = True
            in_ls_id = in_list['id']
            in_ls_stts = in_list['status']
            in_ls_score = f" and scored {in_list['score']}" if in_list[
                'score'] != 0 else ""
            user_data = f"\n➛ **USER DATA:** `{in_ls_stts}{fav}{in_ls_score}`"
    if data["title"]["english"] is not None:
        name = f"**{english}** | `{romaji}`"
    else:
        name = f"[{c_flag}]**{romaji}** | `{native}`"
    prql, sql = "", ""
    for i in prqlsql:
        if i["relationType"] == "PREQUEL":
            pname = (i["node"]["title"]["english"]
                     if i["node"]["title"]["english"] is not None else
                     i["node"]["title"]["romaji"])
            prql += f"**PREQUEL:** `{pname}`\n"
            break
    for i in prqlsql:
        if i["relationType"] == "SEQUEL":
            sname = (i["node"]["title"]["english"]
                     if i["node"]["title"]["english"] is not None else
                     i["node"]["title"]["romaji"])
            sql += f"**SEQUEL:** `{sname}`\n"
            break
    additional = f"{prql}{sql}"
    additional.replace("-", "")
    dura = (f"\n➛ **DURATION:** `{duration} min/ep`"
            if duration is not None else "")
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["timeUntilAiring"]
        air_on = make_it_rw(nextAir * 1000)
        eps = data["nextAiringEpisode"]["episode"]
        th = pos_no(str(eps))
        air_on += f"\n➛** EPISODES:** `{eps}`"
    if air_on is None:
        eps_ = f"{episodes}" if episodes is not None else ""
        status_air = f"➛ **STATUS:** `{status}`\n➛ **EPISODES:** `{eps_}`"
    else:
        status_air = f"➛ **STATUS:** `{status}`\n➛ **NEXT AIRING:** {air_on}"
    if data["trailer"] and data["trailer"]["site"] == "youtube":
        trailer_link = f"<a href='https://youtu.be/{data['trailer']['id']}'>Trailer</a>"
    url = data.get("siteUrl")
    title_img = f"https://img.anili.st/media/{idm}"
    surl = f"https://t.me/{bot}/?start=des_ANI_{idm}"
    total = result["data"]["Page"]["pageInfo"]["total"]
    try:
        finals_ = ANIME_TEMPLATE.format(**locals())
    except KeyError as kys:
        return [f"{kys}"]
    return title_img, [finals_,
                       total], [idm, in_ls, in_ls_id, isfav,
                                str(adult)]


async def get_character(query, page, auth: bool = False, user: int = None):
    var = {"search": CHAR_DB[query], "page": int(page)}
    result = await return_json_senpai(CHARACTER_QUERY,
                                      var,
                                      auth=auth,
                                      user=user)
    if len(result['data']['Page']['characters']) == 0:
        return ["No results Found"]
    data = result["data"]["Page"]["characters"][0]
    # Character Data
    id_ = data["id"]
    name = data["name"]["full"]
    img = data["image"]["large"]
    site_url = data["siteUrl"]
    isfav = data.get("isFavourite")
    cap_text = f"""**{name}**
**ID:** {id_}
<a href='{site_url}'>Visit Website</a>"""
    total = result["data"]["Page"]["pageInfo"]["total"]
    return img, [cap_text, total], [id_, isfav]


async def browse_(qry: str):
    s, y = season_()
    sort = "POPULARITY_DESC"
    if qry == 'upcoming':
        s, y = season_(True)
    if qry == 'trending':
        sort = "TRENDING_DESC"
    vars_ = {"s": s, "y": y, "sort": sort}
    result = await return_json_senpai(BROWSE_QUERY, vars_)
    data = result["data"]["Page"]["media"]
    ls = []
    for i in data:
        if i['format'] in ['TV', 'MOVIE', 'ONA']:
            ls.append('➛ `' + i['title']['romaji'] + '`')
    out = f'{qry.capitalize()} animes in {s} {y}:\n\n'
    return out + "\n".join(ls[:20])


async def get_manga(qdb, page, auth: bool = False, user: int = None):
    vars_ = {"search": MANGA_DB[qdb], "asHtml": True, "page": page}
    result = await return_json_senpai(MANGA_QUERY, vars_, auth=auth, user=user)
    if len(result['data']['Page']['media']) == 0:
        return ["No results Found"]
    data = result["data"]["Page"]["media"][0]

    # Data of all fields in returned json
    # pylint: disable=possibly-unused-variable
    idm = data.get("id")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    native = data["title"]["native"]
    status = data.get("status")
    synopsis = data.get("description")
    description = synopsis[:500]
    if len(synopsis) > 500:
        description += f"...`\n\n[For more info click here](https://t.me/Gbot/?start=des_ANI_{idm})`"
    volumes = data.get("volumes")
    chapters = data.get("chapters")
    score = data.get("averageScore")
    url = data.get("siteUrl")
    format_ = data.get("format")
    country = data.get("countryOfOrigin")
    source = data.get("source")
    isfav = data.get("isFavourite")
    adult = data.get("isAdult")
    fav = ", in Favourites" if isfav is True else ""
    in_ls = False
    in_ls_id = ""
    user_data = ""
    if auth is True:
        in_list = data.get("mediaListEntry")
        if in_list is not None:
            in_ls = True
            in_ls_id = in_list['id']
            in_ls_stts = in_list['status']
            in_ls_score = f" and scored {in_list['score']}" if in_list[
                'score'] != 0 else ""
            user_data = f"➛ **USER DATA:** `{in_ls_stts}{fav}{in_ls_score}`\n"
    name = f"""**{english}** | `{romaji}`"""
    if english is None:
        name = f"""**{romaji}**
        {native}"""
    finals_ = f"{name}\n\n"
    finals_ += f"➛ **ID:** `{idm}`\n"
    finals_ += f"➛ **STATUS:** `{status}`\n"
    finals_ += f"➛ **VOLUMES:** `{volumes}`\n"
    finals_ += f"➛ **CHAPTERS:** `{chapters}`\n"
    finals_ += f"➛ **SCORE:** `{score}`\n"
    finals_ += f"➛ **FORMAT:** `{format_}`\n"
    finals_ += f"➛ **SOURCE:** `{source}`\n"
    finals_ += user_data
    finals_ += f"\nDescription: `{description}`\n\n"
    pic = f"https://img.anili.st/media/{idm}"
    return pic, [finals_, result["data"]["Page"]["pageInfo"]["total"],
                 url], [idm, in_ls, in_ls_id, isfav,
                        str(adult)]


async def get_airing(vars_, auth: bool = False, user: int = None):
    result = await return_json_senpai(AIR_QUERY, vars_, auth=auth, user=user)
    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"{error_sts}"]
    data = result["data"]["Media"]
    # Airing Details
    mid = data.get("id")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    status = data.get("status")
    country = data.get("countryOfOrigin")
    coverImg = f"https://img.anili.st/media/{mid}"
    isfav = data.get("isFavourite")
    in_ls = False
    in_ls_id = ""
    user_data = ""
    if auth is True:
        in_list = data.get("mediaListEntry")
        if in_list is not None:
            in_ls = True
            in_ls_id = in_list['id']
            in_ls_stts = in_list['status']
            user_data = f"**USER DATA:** `{in_ls_stts}`\n"
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["timeUntilAiring"]
        episode = data["nextAiringEpisode"]["episode"]
        th = pos_no(episode)
        air_on = make_it_rw(nextAir * 1000)
    title_ = english or romaji
    out = f"**{title_}**"
    out += f"\n\n**ID:** `{mid}`"
    out += f"\n**Status:** `{status}`\n"
    out += user_data
    if air_on:
        out += f"Airing Episode `{episode}{th}` in `{air_on}`"
    site = data["siteUrl"]
    return [coverImg, out], site, [mid, in_ls, in_ls_id, isfav]


async def toggle_favourites(id_: int, media: str, user: int):
    vars_ = {"id": int(id_)}
    query = (ANIME_MUTATION if media in ("ANIME", "AIRING") else
             CHAR_MUTATION if media == "CHARACTER" else MANGA_MUTATION)
    k = await return_json_senpai(query=query,
                                 vars_=vars_,
                                 auth=True,
                                 user=int(user))
    try:
        return "ok"
    except (KeyError, IndexError):
        return "failed"


async def get_user(vars_, req, user):
    query = USER_QRY if "user" in req else VIEWER_QRY
    k = await return_json_senpai(query=query,
                                 vars_=vars_,
                                 auth=not "user" in req,
                                 user=int(user))
    error = k.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"{error_sts}"]

    data = k['data']['User' if "user" in req else 'Viewer']
    anime = data['statistics']['anime']
    manga = data['statistics']['manga']
    stats = f"""
**Anime Stats**:
Total Anime Watched: `{anime['count']}`
Total Episode Watched: `{anime['episodesWatched']}`
Total Time Spent: `{anime['minutesWatched']}`
Average Score: `{anime['meanScore']}`
**Manga Stats**:
Total Manga Read: `{manga['count']}`
Total Chapters Read: `{manga['chaptersRead']}`
Total Volumes Read: `{manga['volumesRead']}`
Average Score: `{manga['meanScore']}`
"""
    btn = []
    if not "user" in req:
        btn.append([
            InlineKeyboardButton(
                "Favourites", callback_data=f"myfavs_{data['id']}_yes_{user}"),
            InlineKeyboardButton("Activity",
                                 callback_data=f"myacc_{data['id']}_{user}")
        ])
    btn.append([InlineKeyboardButton("Profile", url=str(data['siteUrl']))])
    return f'https://img.anili.st/user/{data["id"]}?a={time.time()}', stats, InlineKeyboardMarkup(
        btn)


async def update_anilist(id_, req, user, eid: int = None, status: str = None):
    vars_ = {"id": int(id_), "status": status}
    if req == "lsus":
        vars_ = {"id": int(eid), "status": status}
    if req == "dlt":
        vars_ = {"id": int(eid)}
    k = await return_json_senpai(
        query=(ANILIST_MUTATION if req == "lsas" else
               ANILIST_MUTATION_UP if req == "lsus" else ANILIST_MUTATION_DEL),
        vars_=vars_,
        auth=True,
        user=int(user))
    try:
        k['data']['SaveMediaListEntry'] if req == "lsas" else k['data'][
            'UpdateMediaListEntries'] if req == "lsus" else k["data"][
                'DeleteMediaListEntry']
        return "ok"
    except (KeyError, IndexError):
        return "failed"


async def check_if_adult(id_):
    vars_ = {"id": int(id_)}
    k = await return_json_senpai(query=ISADULT, vars_=vars_, auth=False)
    if str(k['data']['Media']['isAdult']) == "True":
        return "True"
    else:
        return "False"


####       END        ####

#### Jikanpy part ####


async def get_scheduled(x: int = 9):
    day = str(day_(x if x != 9 else datetime.now().weekday())).lower()
    out = f"Scheduled animes for {day.capitalize()}\n\n"
    async with AioJikan() as session:
        sched_ls = (await session.schedule(day=day)).get(day)
        for i in sched_ls:
            out += f"➛ `{i['title']}`\n"
    return out, x if x != 9 else datetime.now().weekday()


####     END      ####

#### chiaki part ####


def get_wols(x: str):
    data = requests.get(f"https://chiaki.vercel.app/search2?query={x}").json()
    ls = []
    for i in data:
        sls = [data[i], i]
        ls.append(sls)
    return ls


def get_wo(x: int, page: int):
    data = requests.get(f"https://chiaki.vercel.app/get2?group_id={x}").json()
    msg = "Watch order for the given query is:\n\n"
    out = []
    for i in data:
        out.append(f"{i['index']}. `{i['name']}`\n")
    total = len(out)
    for _ in range(50 * page):
        out.pop(0)
    out_ = "".join(out[:50])
    return msg + out_, total


####     END     ####

##### Anime Fillers Part #####


def search_filler(query):
    html = requests.get("https://www.animefillerlist.com/shows").text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.findAll("div", attrs={"class": "Group"})
    index = {}
    for i in div:
        li = i.findAll("li")
        for jk in li:
            yum = jk.a["href"].split("/")[-1]
            cum = jk.text
            index[cum] = yum
    ret = {}
    keys = list(index.keys())
    for i in range(len(keys)):
        if query.lower() in keys[i].lower():
            ret[keys[i]] = index[keys[i]]
    return ret


def parse_filler(filler_id):
    url = "https://www.animefillerlist.com/shows/" + filler_id
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", attrs={"id": "Condensed"})
    all_ep = div.find_all("span", attrs={"class": "Episodes"})
    if len(all_ep) == 1:
        ttl_ep = all_ep[0].findAll("a")
        total_ep = []
        mix_ep = None
        filler_ep = None
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": filler_ep,
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 2:
        ttl_ep = all_ep[0].findAll("a")
        fl_ep = all_ep[1].findAll("a")
        total_ep = []
        mix_ep = None
        ac_ep = None
        filler_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 3:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 4:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        al_ep = all_ep[3].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        for aol in al_ep:
            ac_ep.append(aol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ", ".join(ac_ep),
        }
        return dict_
