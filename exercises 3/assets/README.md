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

## Speech recording 

`speech.wav` contains LibriSpeech development-set clips `1272-128104-0000`
and `1272-128104-0001`, speaker 1272, chapter 128104. The corpus was prepared
by Vassil Panayotov with assistance from Daniel Povey from LibriVox readings.

- Corpus and attribution: https://www.openslr.org/12/
- License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
- Downloaded subset: https://huggingface.co/datasets/hf-internal-testing/librispeech_asr_dummy

Modifications: decoded the original FLAC clips to 16-bit mono PCM without
changing the 16,000 Hz sample rate; placed clip 0000 at 0 seconds and clip 0001
at 7 seconds; inserted zero-valued silence between and after them to produce
a 13-second WAV. Speech samples were not otherwise changed.

Clip 0000 transcript: “Mister Quilter is the apostle of the middle classes and
we are glad to welcome his gospel.”

Clip 0001 transcript: “Nor is Mister Quilter's manner less interesting than
his matter.” Exercise crop: [7.0, 12.0) seconds, exactly 80,000 samples.

Students need SciPy for WAV loading and IPython for playback, in addition
to NumPy and Matplotlib. No librosa, FFmpeg, network access, or download is
needed to run the notebook with its supplied assets.

## Real dorsal-view fly in a larger chamber 

`fly.png` is a teaching composite based on a real dorsal microscope photograph
of a male Drosophila melanogaster with flat, overlapping resting wings, from
the Drosophoto collection. The fly sits
small and off centre on a larger, near-white chamber floor with no cast shadow.
The image is 1536 × 1024 RGB pixels. It is not an unedited chamber recording.

Source attribution: Nicola White and Tom A. R. Price (2021), Drosophila
melanogaster, University of Liverpool DataCat.

- Collection and metadata: https://datacat.liverpool.ac.uk/1561/
- DOI: https://doi.org/10.17638/datacat.liverpool.ac.uk/1561
- Source file: D. mel mature male dorsal (2).tif
- Source download: https://datacat.liverpool.ac.uk/1561/10/D.%20mel%20mature%20male%20dorsal%20(2).tif
- License: CC BY-NC 4.0, https://creativecommons.org/licenses/by-nc/4.0/

Preparation: converted the source TIFF to a 900 × 611 PNG for editing. This
photographic source is included as `fly_source.png`. An image-editing model
then extended the bright background, reduced the specimen's scale, and placed
it off centre. The model was instructed to preserve the photographed specimen,
its dorsal pose and anatomy, and to avoid shadows, walls, debris and labels.
The result is labelled as an edited photographic teaching composite. The image
and its grayscale/mask/position-overlay derivatives retain CC BY-NC 4.0 terms.

A threshold near 0.75 gives a useful body mask; changing the threshold includes
or excludes lighter body parts, transparent wings, and thin legs. At 0.75, the
mean selected-pixel position is approximately x=1028, y=455, on the fly's body.
The clean background has no selected pixels outside the specimen region even
at threshold 0.95. The previous shadowed photograph is no longer used.
