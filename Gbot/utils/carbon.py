"""
Copyright ( C ) GopiNath  
"""

from io import BytesIO
from Gbot import aiohttpsession


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiohttpsession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "Queen_Carbon.png"
    return image
