import os

import cv2

DENSITY = "$@#&%9865432MZYXWTRQPONLJGDCBwmqpkdbhazoecvunxrjrtI1?}{)(/|!li+~=_-:,^'."
GRAY_LEVELS = 23
CHAR_ASPECT_RATIO = 0.4
COLS = 190


def get_gray(pixel):
    scale = pixel * GRAY_LEVELS // 255
    return f"\033[38;5;{232 + scale}m"


def to_ascii(frame, cols=COLS, char_aspect=CHAR_ASPECT_RATIO):
    height, width = frame.shape[:2]
    scale = width / cols
    rows = int(height / (scale / char_aspect))
    resized = cv2.resize(frame, (cols, rows))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    lines = []
    for row in gray:
        line = ""
        for pixel in row:
            ansi = ansi_cache[pixel]
            char = char_cache[pixel]
            line += f"{ansi}{char}"
        lines.append(line + "\033[0m")
    return "\n".join(lines)


ansi_cache = [get_gray(i) for i in range(256)]
char_cache = [DENSITY[(255 - i) * len(DENSITY) // 256] for i in range(256)]

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    ascii_art = to_ascii(frame)

    os.system("cls" if os.name == "nt" else "clear")
    print(ascii_art)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
