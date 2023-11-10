from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from .paths import FONTS_DIR, IMAGES_DIR


def drawer(img, text, dp, mask, W=500):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font=str((FONTS_DIR / "Poppins-SemiBold.ttf").resolve()), size=25)

    if len(text) > 20:
        text = text[:20] + "..."

    w, h = draw.textsize(text, font=font)
    draw.text(((W - w) / 2, 165), text, font=font, fill="white", align="left")
    img.paste(dp, (218, 102), mask)

    return img


def circler(img):
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, Image.ANTIALIAS)

    img.putalpha(mask)

    return img, mask


def download_dp(url):
    dp_download = requests.get(url, stream=True).raw
    img = Image.open(dp_download).convert("RGBA").resize((65, 65), Image.ANTIALIAS)

    return img


def process(username, url):
    arr = BytesIO()

    img = drawer(
        Image.open(IMAGES_DIR / "template.png"), username, *circler(download_dp(url))
    )
    img.save(arr, "PNG")
    arr.seek(0)

    return arr
