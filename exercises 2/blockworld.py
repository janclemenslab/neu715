"""Dungeon Escape: a tiny room-exploration game for beginner Python notebooks.

Student API: forward, left, right, toss_dice.
"""

from functools import lru_cache
from math import isfinite
from pathlib import Path
from random import Random
from time import sleep

__all__ = [
    "forward",
    "left",
    "right",
    "toss_dice",
    "reset",
    "load",
    "show",
    "new_hallway",
    "new_practice_room",
    "new_twisty_room",
]

_ARROWS = ">v<^"
_STEPS = ((1, 0), (0, 1), (-1, 0), (0, -1))
_DEFAULT_WORLD = (
    "######",
    "#>..E#",
    "######",
)
_rng = Random()
_THEMES = ("mouse", "penguin", "turtle", "beetle", "robot", "fox")


class _World:
    def __init__(self, lines):
        self.load(lines)

    def load(self, lines, visible=True, theme="mouse", delay=0.25):
        if theme not in _THEMES:
            raise ValueError(f"Choose a theme from: {', '.join(_THEMES)}.")
        if not isinstance(delay, (int, float)) or not isfinite(delay) or delay < 0:
            raise ValueError("delay must be a finite, non-negative number of seconds.")
        lines = tuple(lines)
        if not lines or not all(lines) or len({len(line) for line in lines}) != 1:
            raise ValueError("The room must be a non-empty rectangle.")

        start = exit_position = None
        for y, line in enumerate(lines):
            for x, tile in enumerate(line):
                if tile in _ARROWS:
                    if start is not None:
                        raise ValueError("The room needs exactly one starting arrow.")
                    start = (x, y, _ARROWS.index(tile))
                elif tile == "E":
                    if exit_position is not None:
                        raise ValueError("The room needs exactly one exit (E).")
                    exit_position = (x, y)
                elif tile not in "#. ":
                    raise ValueError("Use #, ., a starting arrow, and E in a room.")
        if start is None or exit_position is None:
            raise ValueError("The room needs one starting arrow and one exit (E).")

        self.lines = lines
        self.start = start
        self.visible = visible
        self.theme = theme
        self.delay = delay
        self.reset()

    def reset(self):
        self.x, self.y, self.heading = self.start
        self.last_bump = None
        self.revealed = {(self.x, self.y)}
        if self.visible:
            self.revealed = {
                (x, y) for y, line in enumerate(self.lines) for x in range(len(line))
            }

    def forward(self):
        dx, dy = _STEPS[self.heading]
        x, y = self.x + dx, self.y + dy
        outside = not (0 <= y < len(self.lines) and 0 <= x < len(self.lines[0]))
        if outside or self.lines[y][x] == "#":
            self.last_bump = (x, y)
            if not outside:
                self.revealed.add((x, y))
            return "wall"

        self.x, self.y = x, y
        self.last_bump = None
        self.revealed.add((x, y))
        return "exit" if self.lines[y][x] == "E" else "moved"


_world = _World(_DEFAULT_WORLD)
_display_handle = None
_display_execution = None


def _corridor(segment_lengths, turns):
    """Build a one-square-wide corridor from lengths and left/right turns."""
    if len(segment_lengths) != len(turns) + 1 or any(length < 1 for length in segment_lengths):
        raise ValueError("A corridor needs one more positive length than turns.")

    x = y = heading = 0
    path = [(x, y)]
    for index, length in enumerate(segment_lengths):
        dx, dy = _STEPS[heading]
        for _ in range(length):
            x, y = x + dx, y + dy
            if (x, y) in path:
                raise ValueError("The corridor cannot cross itself.")
            path.append((x, y))
        if index < len(turns):
            if turns[index] not in ("left", "right"):
                raise ValueError("Turns must be 'left' or 'right'.")
            heading = (heading + (1 if turns[index] == "right" else -1)) % 4

    dx, dy = _STEPS[heading]
    exit_position = (x + dx, y + dy)
    xs = [point[0] for point in path] + [exit_position[0]]
    ys = [point[1] for point in path] + [exit_position[1]]
    shift_x, shift_y = 1 - min(xs), 1 - min(ys)
    width, height = max(xs) - min(xs) + 3, max(ys) - min(ys) + 3
    grid = [["#"] * width for _ in range(height)]

    for path_x, path_y in path:
        grid[path_y + shift_y][path_x + shift_x] = "."
    grid[shift_y][shift_x] = ">"
    exit_x, exit_y = exit_position
    grid[exit_y + shift_y][exit_x + shift_x] = "E"
    return tuple("".join(row) for row in grid)


def _seed(seed):
    if seed is not None:
        _rng.seed(seed)


@lru_cache(maxsize=6)
def _art(theme):
    """Load artwork once at its display size, including all four headings."""
    from PIL import Image, ImageDraw

    assets = Path(__file__).with_name("assets")
    with Image.open(assets / f"{theme}_player.png") as source:
        sprite = source.convert("RGBA").resize((59, 59), Image.Resampling.LANCZOS)
    player = Image.new("RGBA", (65, 65))
    player.paste(sprite, (3, 3))
    ImageDraw.Draw(player).polygon(((64, 32), (52, 25), (52, 40)),
                                   fill="white", outline="#020617", width=2)
    players = tuple(player.rotate(-90 * heading) for heading in range(4))
    with Image.open(assets / f"{theme}_tiles.png") as atlas:
        w, h = atlas.width // 2, atlas.height // 2
        tiles = tuple(atlas.crop((x * w, y * h, (x + 1) * w, (y + 1) * h))
                      .convert("RGB").resize((65, 65), Image.Resampling.LANCZOS)
                      for y in range(2) for x in range(2))
    return players, tiles


@lru_cache(maxsize=1)
def _room_image(lines, theme):
    """Cache the static room; movement only needs a copy and a player overlay."""
    from PIL import Image, ImageDraw, ImageFont

    _, tiles = _art(theme)
    board = Image.new("RGB", (len(lines[0]) * 65, len(lines) * 65), "#020617")
    draw = ImageDraw.Draw(board)
    font = ImageFont.load_default(size=11)
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            index = 1 if tile == "#" else 2 if tile == "E" else 3 if (x + y) % 2 else 0
            px, py = x * 65, y * 65
            board.paste(tiles[index], (px, py))
            draw.rectangle((px, py, px + 64, py + 64), outline="#020617")
            if tile == "E":
                draw.rectangle((px + 2, py + 2, px + 62, py + 62), outline="#86efac", width=2)
                draw.rectangle((px + 17, py + 2, px + 48, py + 15), fill="#14532d")
                draw.text((px + 32, py + 9), "EXIT", anchor="mm", fill="white", font=font)
    return board


def _render():
    """Render one frame without changing the room or displaying anything."""
    from PIL import Image, ImageDraw, ImageFont

    board = _room_image(_world.lines, _world.theme).copy()
    if not _world.visible:
        draw = ImageDraw.Draw(board)
        for y, line in enumerate(_world.lines):
            for x in range(len(line)):
                if (x, y) not in _world.revealed:
                    draw.rectangle((x * 65, y * 65, (x + 1) * 65 - 1, (y + 1) * 65 - 1), fill="#020617")
    players, _ = _art(_world.theme)
    player = players[_world.heading]
    board.paste(player, (_world.x * 65, _world.y * 65), player)
    frame = Image.new("RGB", (max(260, board.width + 8), max(200, board.height + 38)), "#020617")
    frame.paste(board, ((frame.width - board.width) // 2, 34))
    title = "Bonk! Wall." if _world.last_bump is not None else "Dungeon Escape" if _world.visible else "The room is dark..."
    ImageDraw.Draw(frame).text((frame.width // 2, 16), title, anchor="mm",
                               fill="white", font=ImageFont.load_default(size=20))
    return frame


def show():
    """Draw the discovered room, then pause for the room's configured delay."""
    global _display_handle, _display_execution
    try:
        from IPython import get_ipython
    except ImportError:
        return
    shell = get_ipython()
    if shell is None:
        return

    from io import BytesIO
    from IPython.display import Image, display

    output = BytesIO()
    _render().save(output, format="PNG", compress_level=1)
    frame = Image(data=output.getvalue())
    if _display_handle is not None and _display_execution == shell.execution_count:
        _display_handle.update(frame)
    else:
        _display_handle = display(frame, display_id=True)
        _display_execution = shell.execution_count
    sleep(_world.delay)


def load(lines, *, visible=True, theme="mouse", delay=0.25):
    """Load a themed room; delay sets the pause after each step in seconds."""
    _world.load(lines, visible=visible, theme=theme, delay=delay)
    show()


def new_hallway(seed=None, *, visible=True, theme="mouse", delay=0.25):
    """Create a kinked hallway; visible=True shows the whole map."""
    _seed(seed)
    length = _rng.randint(6, 12)
    bend_after = _rng.randint(3, length - 3)
    first_turn = _rng.choice(("left", "right"))
    second_turn = "right" if first_turn == "left" else "left"
    load(_corridor((bend_after, 1, length - bend_after - 1), (first_turn, second_turn)), visible=visible, theme=theme, delay=delay)


def new_practice_room(turn="left", seed=None, *, visible=True, theme="mouse", delay=0.25):
    """Create a one-corner room; visible=True shows the whole map."""
    _seed(seed)
    load(_corridor((_rng.randint(3, 5), _rng.randint(3, 5)), (turn,)), visible=visible, theme=theme, delay=delay)


def new_twisty_room(seed=None, *, visible=True, theme="mouse", delay=0.25):
    """Create two independently random turns with random distances; visible=False hides the map."""
    _seed(seed)
    first_turn = _rng.choice(("left", "right"))
    second_turn = _rng.choice(("left", "right"))
    turns = (first_turn, second_turn)
    lengths = (
        _rng.randint(2, 4),
        _rng.randint(2, 4),  # Keep a wall between parallel corridor sections.
        _rng.randint(3, 5),
    )
    load(_corridor(lengths, turns), visible=visible, theme=theme, delay=delay)


def forward():
    """Move one square: return 'exit' on the exit, 'moved' on floor, or 'wall' if blocked."""
    feedback = _world.forward()
    show()
    return feedback


def left():
    """Turn 90 degrees left."""
    _world.heading = (_world.heading - 1) % 4
    show()


def right():
    """Turn 90 degrees right."""
    _world.heading = (_world.heading + 1) % 4
    show()


def toss_dice():
    """Return True or False with equal probability."""
    return _rng.random() < 0.5


def reset():
    """Return to the start, keeping the room's theme, visibility, and delay."""
    _world.reset()
    show()
