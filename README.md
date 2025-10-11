[Neu715 - Neuroscientific Data Analysis using Python](http://janclemenslab.org/neu715)

To run the notebooks: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/janclemenslab/neu715/HEAD)


# Dev

## Install
```shell
conda create -y -n neu715 jupyter-book matplotlib numpy fabric3
```

## Build
```shell
jb clean .
jb build .
git commit -a -m 'COMMIT_MSG'
git push
```