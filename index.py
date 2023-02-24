import io
import random
import shutil
import time

from PIL import Image
from telethon import functions, types
from telethon.sync import TelegramClient

name, api_id, api_hash = "aboba", 22936884, "3f1e687f728cb037cbb5e45aa019bf81"
sticker_id, sticker_hash = 3664822579232780, -6599700879210452751
sticker_pack_name = "test"


def to100(file, name):
    '''to100 resizes an image to 100x100, saves it and returns the file name'''
    img = Image.open(io.BytesIO(file))
    # Calculate the new size of the image
    current_size = img.size
    new_size = (512 - current_size[0],
                512 - current_size[1])

    # Calculate the padding on both sides of the image
    left_padding = new_size[0] // 2
    # right_padding = new_size[0] - left_padding

    # Create a new empty image of the final size
    padded_img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))

    # Paste the original image in the center of the new image
    padded_img.paste(img, (left_padding, 0))

    # Resize the image to the new size
    resized_img = padded_img.resize((100, 100))

    # # Save the resized image to the destination directory
    # resized_img.save("temp/"+name+".png")

    file = io.BytesIO()
    resized_img.save(file, format='PNG')
    file.name = "1.png"
    file.seek(0)

    return file


def save(d):
    '''save saves a document to a file and returns the file name + connected emoji'''

    file = client.download_file(d)
    b = to100(file, str(d.id))

    return b, d.attributes[1].alt


with TelegramClient(name, api_id, api_hash) as client:
    # messages_obj = client.iter_messages("me")
    # for message in messages_obj:
    #     print(message)
    #     break

    result = client(functions.messages.GetStickerSetRequest(
        stickerset=types.InputStickerSetID(
            id=sticker_id,
            access_hash=sticker_hash
        ),
        hash=0
    ))

    client.send_message("@Stickers", "/start")
    time.sleep(1)

    client.send_message("@Stickers", "/newemojipack")
    time.sleep(1)

    client.send_message("@Stickers", "Static emoji")
    time.sleep(1)

    client.send_message("@Stickers", sticker_pack_name+" by @mrfemblog")
    time.sleep(1)

    for sticker in result.documents:
        b, emoji = save(sticker)
        time.sleep(1)
        client.send_file("@Stickers", file=b,
                         force_document=True)
        time.sleep(1)
        client.send_message("@Stickers", emoji)

    time.sleep(1)

    client.send_message("@Stickers", "/publish")
    time.sleep(1)

    client.send_message("@Stickers", "/skip")
    time.sleep(1)

    client.send_message("@Stickers", sticker_pack_name +
                        "_"+str(random.randint(0, 1000)))  # random name :3
