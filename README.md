Manim from [github.com/3b1b/manim](https://github.com/3b1b/manim) is an animation engine 
by [github.com/3b1b](https://github.com/3b1b).

The aim of project "Basic-Manim" is to test and update basic manim features based on 
[manim-19Dec19-3b1b](https://github.com/3b1b/manim/tree/ba2f2f8840df37b2e7de2841c961d9a02b03c9e4) for SidewayOutput Projects.

## Installation for Windows 10
### System Preparation
1. Install [ffmpeg](https://www.ffmpeg.org),
2. Install [sox](http://sox.sourceforge.net),
3. Install [MiKTeX](https://miktex.org/download)

### Anaconda Install
1. Install [Anaconda](https://www.anaconda.com/products/individual)

#### Create a Conda Enviroment for Basic-Manim
1. Open Anaconda Prompt
2. Create a conda environment, 'manim', using `conda create -n manim python=3.8`
3. Activate the 'manim' environment using `conda activate manim`

#### Install Python Packages Under enviroment 'manim'
1. pip install colour
2. pip install numpy
3. pip install tqdm
4. pip install scipy
5. pip install pillow
6. pip install pycairo
7. pip install pydub
8. pip install pyreadline
9. ... others when necessary

#### Using Basic-Manim Under enviroment 'manim'
1. change directory to the working directory with 'Basic-Manim' files
2. run `python -m manim tutorial\basicmanim\basicmanim_transform_001a.py -pl` 

## License

In general,

All files in the directory `manim-19Dec19-3b1b-archive` are copyright 3Blue1Brown.

The general purpose animation code found in the remainder of the repository, on the other hand, 
is under the MIT license.

Please refer to [3b1b-LICENSE](3b1b-LICENSE) and [SidewayOutput-LICENSE](SidewayOutput-LICENSE) for details.
