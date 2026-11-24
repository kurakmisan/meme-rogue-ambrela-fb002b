"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one meme as a PNG using only the standard library and writes it to
/output/entry.png. The picture is built on a 256x256 grid of palette
colours and enlarged four times, so every pixel is deliberate and the
output is byte-identical on every run.
"""
import os
import struct
import zlib

GRID = 256          # logical canvas, in cells
ZOOM = 4            # each cell becomes ZOOM x ZOOM pixels -> 1024 x 1024
OUT = os.environ.get("ENTRY_OUT", "/output/entry.png")

PALETTE = {
    "black": (16, 16, 20),
    "white": (250, 250, 245),
    "wall": (198, 214, 226),
    "floor": (120, 98, 120),
    "sky": (120, 190, 240),
    "tower": (70, 100, 150),
    "frame": (240, 240, 235),
    "desk": (140, 84, 44),
    "desktop": (176, 112, 62),
    "gold": (240, 196, 60),
    "steel": (168, 176, 188),
    "shade": (110, 118, 132),
    "eye": (60, 230, 240),
    "suit": (34, 40, 66),
    "shirt": (236, 238, 244),
    "tie": (214, 40, 48),
    "skin": (238, 190, 150),
    "hair": (78, 52, 36),
    "hoodie": (88, 150, 110),
    "jeans": (58, 78, 130),
    "tray": (150, 150, 158),
    "coffee": (110, 66, 36),
}
NAMES = list(PALETTE)
INDEX = {name: i for i, name in enumerate(NAMES)}

# 5x7 bitmap font, drawn by hand. '#' is ink.
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    " ": ["....."] * 7,
}


def new_canvas(colour):
    return [bytearray([INDEX[colour]]) * GRID for _ in range(GRID)]


def rect(cv, x0, y0, x1, y1, colour):
    """Fill cells x0..x1-1, y0..y1-1."""
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(GRID, x1), min(GRID, y1)
    if x1 <= x0:
        return
    run = bytes([INDEX[colour]]) * (x1 - x0)
    for y in range(y0, y1):
        cv[y][x0:x1] = run


def text_width(s, size):
    return len(s) * 6 * size - size


def text(cv, s, x, y, size, colour):
    for ch in s:
        glyph = FONT[ch]
        for row, line in enumerate(glyph):
            for col, mark in enumerate(line):
                if mark == "#":
                    rect(cv, x + col * size, y + row * size,
                         x + (col + 1) * size, y + (row + 1) * size, colour)
        x += 6 * size


def centred_in(cv, s, x0, x1, y, size, colour):
    text(cv, s, x0 + (x1 - x0 - text_width(s, size)) // 2, y, size, colour)


def centred(cv, s, y, size, colour):
    centred_in(cv, s, 0, GRID, y, size, colour)


def office(cv):
    rect(cv, 0, 184, GRID, 212, "floor")
    # corner-office window with a skyline
    rect(cv, 150, 52, 246, 112, "frame")
    rect(cv, 153, 55, 243, 109, "sky")
    for x, top, wide in ((156, 84, 12), (171, 70, 14), (188, 90, 10),
                         (201, 76, 16), (220, 64, 12), (234, 88, 9)):
        rect(cv, x, top, x + wide, 109, "tower")
    rect(cv, 197, 55, 200, 109, "frame")


def robot(cv):
    # antenna, head, smug face
    rect(cv, 187, 60, 189, 70, "shade")
    rect(cv, 185, 56, 191, 61, "tie")
    rect(cv, 164, 70, 212, 108, "steel")
    rect(cv, 164, 104, 212, 108, "shade")
    rect(cv, 172, 80, 184, 90, "eye")
    rect(cv, 192, 80, 204, 90, "eye")
    rect(cv, 172, 78, 184, 82, "steel")      # half-closed lids
    rect(cv, 192, 78, 204, 82, "steel")
    rect(cv, 180, 97, 200, 99, "black")      # smirk
    rect(cv, 200, 95, 202, 97, "black")
    rect(cv, 183, 108, 193, 114, "shade")    # neck
    # suit, shirt and tie
    rect(cv, 152, 114, 224, 160, "suit")
    rect(cv, 180, 114, 196, 160, "shirt")
    rect(cv, 185, 116, 191, 122, "tie")
    rect(cv, 186, 122, 190, 150, "tie")


def desk(cv):
    rect(cv, 110, 150, 250, 158, "desktop")
    rect(cv, 114, 158, 246, 200, "desk")
    # hands folded on the desk
    rect(cv, 170, 144, 184, 152, "steel")
    rect(cv, 192, 144, 206, 152, "steel")
    # name plate
    rect(cv, 154, 164, 206, 186, "black")
    rect(cv, 156, 166, 204, 184, "gold")
    centred_in(cv, "CEO", 156, 204, 168, 2, "black")


def disc(cv, cx, cy, r, colour):
    for dy in range(-r, r + 1):
        half = int((r * r - dy * dy) ** 0.5)
        rect(cv, cx - half, cy + dy, cx + half + 1, cy + dy + 1, colour)


def bold(cv, s, y, size, colour):
    """Caption text, one cell heavier so it survives a phone screen."""
    x = (GRID - text_width(s, size) - 1) // 2
    text(cv, s, x, y, size, colour)
    text(cv, s, x + 1, y, size, colour)


def intern(cv):
    """Me, demoted: carrying the boss's coffee."""
    centred_in(cv, "ME", 38, 82, 96, 2, "black")
    rect(cv, 59, 111, 62, 115, "black")              # arrow down to my head
    rect(cv, 57, 114, 64, 116, "black")
    rect(cv, 59, 116, 62, 118, "black")
    disc(cv, 60, 130, 11, "skin")
    rect(cv, 49, 119, 72, 126, "hair")
    rect(cv, 53, 127, 58, 128, "hair")               # worried brows
    rect(cv, 62, 127, 67, 128, "hair")
    rect(cv, 54, 129, 57, 132, "black")              # eyes
    rect(cv, 63, 129, 66, 132, "black")
    rect(cv, 56, 136, 65, 138, "black")              # flat mouth
    rect(cv, 48, 142, 73, 178, "hoodie")
    rect(cv, 60, 142, 61, 150, "tie")                # lanyard and intern badge
    rect(cv, 56, 150, 66, 158, "white")
    rect(cv, 58, 152, 64, 153, "black")
    rect(cv, 58, 155, 62, 156, "black")
    rect(cv, 50, 178, 59, 200, "jeans")
    rect(cv, 62, 178, 71, 200, "jeans")
    rect(cv, 48, 200, 60, 204, "black")
    rect(cv, 61, 200, 73, 204, "black")
    # arm, tray and a cup of coffee
    rect(cv, 66, 152, 86, 158, "hoodie")
    rect(cv, 84, 151, 90, 158, "skin")
    rect(cv, 80, 158, 108, 161, "tray")
    rect(cv, 89, 144, 101, 158, "white")
    rect(cv, 89, 144, 101, 147, "coffee")
    rect(cv, 101, 148, 104, 154, "white")
    rect(cv, 92, 136, 94, 141, "frame")              # steam
    rect(cv, 96, 133, 98, 139, "frame")


def bubble(cv):
    rect(cv, 6, 49, 148, 91, "black")
    rect(cv, 8, 51, 146, 89, "white")
    for step in range(6):                            # tail towards the robot
        rect(cv, 146 + step * 3, 66 + step, 149 + step * 3, 76 - step, "black")
    for step in range(5):
        rect(cv, 146 + step * 3, 68 + step, 149 + step * 3, 74 - step, "white")
    centred_in(cv, "TWO SUGARS,", 8, 146, 54, 2, "black")
    centred_in(cv, "INTERN.", 8, 146, 72, 2, "black")


def draw(cv):
    office(cv)
    robot(cv)
    desk(cv)
    intern(cv)
    bubble(cv)
    rect(cv, 0, 0, GRID, 44, "black")
    bold(cv, "ASKED MY AGENT TO", 5, 2, "white")
    bold(cv, "GET ME A RAISE", 24, 2, "white")
    rect(cv, 0, 212, GRID, GRID, "black")
    bold(cv, "IT GOT ONE.", 223, 3, "white")


def png_bytes(cv):
    rgb = [bytes(PALETTE[n]) for n in NAMES]
    raw = bytearray()
    for line in cv:
        row = b"".join(rgb[i] * ZOOM for i in line)
        for _ in range(ZOOM):
            raw += b"\x00" + row

    def chunk(kind, data):
        body = kind + data
        return (struct.pack(">I", len(data)) + body
                + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF))

    side = GRID * ZOOM
    header = struct.pack(">IIBBBBB", side, side, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def main():
    cv = new_canvas("wall")
    draw(cv)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as fh:
        fh.write(png_bytes(cv))


if __name__ == "__main__":
    main()
