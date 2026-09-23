# Dungeon Escape artwork

Generated with the built-in Imagegen tool for this game. All six PNG player sprites face right and rotate with the player. Each tile atlas is a 2×2 grid: floor, wall, exit, alternate floor. The engine draws the heading pointer and EXIT label. Keep these files beside blockworld.py in this assets directory.

The mouse, turtle, beetle, and robot backgrounds were removed locally with user approval; penguin and fox retain their generated alpha. No runtime background processing is required.

## Prompt specifications

Player prompt: one cute rounded overhead game character facing right, dark outline, flat colors, minimal shading, readable at 40 pixels, complete centered character, transparent background, no floor, scene, text, labels or direction pointer. The earlier six-character concept sheet was a style reference.

Environment prompt: a square atlas of exactly four equal quadrants, no margins, text or characters; top-left floor, top-right wall, bottom-left exit, bottom-right alternate floor. Cute hand-painted overhead game art, textures fill each tile, welcoming green exit glow.

### mouse

- `mouse_player.png`: pale lilac round mouse, pink round ears, obvious projecting pink pointy nose at RIGHT and slim curled pink tail extending LEFT.
- `mouse_tiles.png`: cozy mouse burrow: warm sandy packed-earth floor, carved earth and rounded stone walls with a few thick roots, exit as a small arched wood-framed burrow door with a soft green welcoming glow.

### penguin

- `penguin_player.png`: round cobalt blue penguin, cream face and belly, tiny orange feet, prominent triangular golden beak at RIGHT.
- `penguin_tiles.png`: penguin ice cave: smooth pale blue snowy ice floor, chunky opaque blue ice-block walls, exit as a rounded igloo-style ice arch with a soft green welcoming glow.

### turtle

- `turtle_player.png`: mint and forest green turtle, patterned oval shell, four stubby feet, distinct yellow-green head extended toward RIGHT.
- `turtle_tiles.png`: turtle pond: walkable flat shallow turquoise water tile with faint ripples and tiny submerged stones, mossy raised stone banks as solid walls, exit as a broad round lily pad landing with a soft green glowing rim.

### beetle

- `beetle_player.png`: coral red beetle, rounded divided wing covers, little dark legs, distinct head and forward antennae extending RIGHT.
- `beetle_tiles.png`: beetle forest floor: warm dark earth and tiny moss flecks as the walkable floor, thick knotted bark/log-and-root barrier as the wall, exit as an opening through an old hollow log with a soft green welcoming glow.

### robot

- `robot_player.png`: cream tiny rounded robot, dark joints, cyan triangular projecting visor at RIGHT, cute simple round torso.
- `robot_tiles.png`: friendly robot lab: clean slate-blue metal floor with restrained cyan circuit traces, chunky steel equipment/block walls, exit as a circular cyan teleporter platform with a soft green glowing rim.

### fox

- `fox_player.png`: orange fox, rounded body, cream pointy muzzle at RIGHT, dark ear tips, fluffy cream-tipped tail trailing LEFT.
- `fox_tiles.png`: fox woodland den: autumn ochre packed soil with sparse little leaf flecks as floor, warm reddish rocky earth and root banks as walls, exit as a cozy arched den entrance framed by orange autumn leaves with a soft green welcoming glow.

