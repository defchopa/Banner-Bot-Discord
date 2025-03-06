from aiohttp import ClientSession
from PIL import Image, ImageFont, ImageDraw
import io
import textwrap

async def banner_dop(voice_count, time, avatar, name, status):

    async with ClientSession() as client:
        async with client.get(avatar) as response:
            avatar = await response.read()
    avatar = Image.open(io.BytesIO(avatar)).resize((333,333)) #размер аватарки 


    background = Image.open('./assets/banner.png')

    draw = ImageDraw.Draw(background)



    mask_im = Image.open("./assets/mask_circle.jpg").convert('L').resize((333,333)) 
    background.paste(avatar, (220, 596), mask_im) #координаты аватарки

    

    myFont = ImageFont.truetype("./assets/21154.otf",120)
    myFont1 = ImageFont.truetype("./assets/21154.ttf",100)
    myFont2 = ImageFont.truetype("./assets/21154.ttf",70)
    myFont3 = ImageFont.truetype("./assets/21154.ttf",90)
    myFont4 = ImageFont.truetype("./assets/20339.ttf",0)
    

    draw.text((540, 700), f"{name}",font=myFont,stroke_fill=(0, 0, 0)) #nick
    draw.text((1168, 544), f"{time}",font=myFont2, stroke_fill=(0, 0, 0)) # time
    draw.text((1620, 836), f"{voice_count}",font=myFont3, stroke_fill=(0, 0, 0))# voice
    current_h2 = 290
    for line in textwrap.wrap(status, width=40):
        pad = 5
        MAX_W, MAX_H = 370, 1200
        w, h = draw.textsize(line, font=myFont4)    
        draw.text(((MAX_W - w) / 2, current_h2), line, font=myFont4)
        current_h2 += h + pad


    f= open("./level.png", "wb") 
    background.save(f, "PNG", subsampling=0, quality=1000)
    return "./level.png"

