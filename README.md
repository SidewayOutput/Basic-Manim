Manim from [github.com/3b1b/manim](https://github.com/3b1b/manim) (now branch [cairo-backend](https://github.com/3b1b/manim/tree/cairo-backend)) is an animation engine 
by [github.com/3b1b](https://github.com/3b1b).

The aim of project "Basic-Manim" is to test and update basic manim features based on 
[3b1b manim @19Dec2019](https://github.com/3b1b/manim/tree/ba2f2f8840df37b2e7de2841c961d9a02b03c9e4) (Cairo Version) for SidewayOutput Projects. Please note that the method of trial and error is used in developing Basic-Manim and backward compatibility is not guaranteed

## Installation for Windows 10
### Download Basic-Manim
1. Download ['Basic-Manim' files](https://github.com/SidewayOutput/Basic-Manim/archive/main.zip)
2. Unzip 'Basic-Manim' files to a working directory

### System Preparation
1. Install [ffmpeg](https://www.ffmpeg.org)
2. Install [sox](http://sox.sourceforge.net)
3. Install [MiKTeX](https://miktex.org/download)

### Anaconda Install
1. Install [Anaconda](https://www.anaconda.com/products/individual)

#### Create a Conda Enviroment for Basic-Manim
1. Open Anaconda Prompt
2. Create a conda environment, 'basicmanim', using `conda create -n basicmanim python=3.8`
3. Activate the 'manim' environment using `conda activate basicmanim`

#### Install Python Packages Under enviroment 'manim'
1. pip install colour
2. pip install numpy
3. pip install tqdm
4. pip install scipy
5. pip install pillow
6. pip install pycairo
7. pip install pydub
8. pip install pyreadline
9. pip install opencv-python
10. pip install PyYAML
11. pip install manimpango

... others when necessary

#### Using Basic-Manim Under enviroment 'manim'
1. Change directory to the working directory containing the unzipped 'Basic-Manim' files
2. Run `python -m manim tutorial\basicmanim\test.py -pl` to verify the installation

## License

In general,

All files in the directory `manim-19Dec19-3b1b-archive` are [copyright 3Blue1Brown](https://github.com/SidewayOutput/Basic-Manim/blob/main/manim-19Dec19-3b1b-archive/LICENSE).
All files in the directory `manim-01Mar21-3b1b-archive` are [copyright 3Blue1Brown](https://github.com/SidewayOutput/Basic-Manim/blob/main/manim-01Mar21-3b1b-archive/LICENSE.md).

The general purpose animation code found in the remainder of the repository, on the other hand, 
is under the MIT license.

Please refer to [3b1b-LICENSE](3b1b-LICENSE) and [SidewayOutput-LICENSE](SidewayOutput-LICENSE) for details.
