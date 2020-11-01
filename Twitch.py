from PIL import Image


def break_string(msg: str) -> (str, str):
    split = msg.split(":", 2)
    msg = split[2]
    command = split[1]
    username = command.split("!")[0]
    return (username, msg)


def validate_image(image: str) -> bool:
    im = Image.open(image)
    w, h = im.size
    if w != 1000 or h != 1000:
        return False
    return True
