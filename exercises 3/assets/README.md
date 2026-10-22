# Images used for the array exercises

`astronaut.png` is the unchanged 512 × 512 RGB photograph of astronaut Eileen
Collins bundled with the installed scikit-image sample data. Its bundled
documentation attributes it to the NASA Great Images database and states that
it is released into the public domain, with no known copyright restrictions.

Original image reference from that documentation: https://flic.kr/p/r9qvLn

The copy is included locally so students do not need scikit-image, a download,
or a network connection.

Exercise ROI: x = [170, 290), y = [50, 190), measured from the top-left corner.

## Flies in a chamber

`flies_chamber.png` is an AI-generated illustration, made with the built-in
ImageGen tool for Exercise 5. It is not experimental data. It shows eight dark
flies on a light chamber floor, suitable for comparing brightness thresholds.
The original generated RGB PNG is included without modification.

Generation prompt:

> Use case: scientific-educational. Asset type: an illustrative teaching input image for a beginner NumPy grayscale thresholding exercise, NOT actual experimental data. Create a realistic monochrome overhead bright-field camera view of EIGHT small Drosophila fruit flies freely walking separately in the center of a uniformly bright matte off-white rectangular observation chamber floor. Make the view look like a clean tracking-camera frame: all eight flies visible from above, recognizable small dark oval abdomens, dark thorax and heads, delicate legs, faint translucent wings. The eight flies should be scattered in varied positions and orientations, widely separated, not overlapping or touching. Each fly should occupy roughly 50–75 pixels in length in a 1024px-wide image so all bodies are easy to see. Uniform diffuse illumination, near-white floor with only minimal texture, no cast shadows, no glare or gradients. Crop entirely inside the chamber so no dark walls, rim, border, corners or camera artifacts are visible. Critical for thresholding: fly bodies and legs are dark grey to near black, background stays consistently light grey to white, with a clear brightness gap. Do not add food, debris, equipment, lettering, labels, axes, scales, watermarks or decorative elements. Landscape 3:2 composition. A clean realistic teaching illustration suitable for turning into a pixel mask with a simple brightness threshold.
