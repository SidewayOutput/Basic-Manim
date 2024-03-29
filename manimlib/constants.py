
import numpy as np
import os

Project = r"Basic\,-\,Manim"
PoweredBy = ("Sideway", r"$\,\cdot\,$", "Output")
import manimlib
Letters = " abcdefghijklmnopqrstuvwxyz"
LETTERs = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# There might be other configuration than pixel shape later...
SHORT_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 2560,
        "pixel_width": 1440,
        "frame_rate": 60,
    }
SHORT_LOW_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 854,
        "pixel_width": 480,
        "frame_rate": 15,
    }
ORIENTATION=1

ASPECT_RATIO = (16.0 / 9.0)**((-1)**(1-ORIENTATION))


if ASPECT_RATIO>1:
    PRODUCTION_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 1440,
        "pixel_width": 2560,
        "frame_rate": 60,
    }

    HIGH_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 1080,
        "pixel_width": 1920,
        "frame_rate": 60,
    }

    MEDIUM_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 720,
        "pixel_width": 1280,
        "frame_rate": 30,
    }

    LOW_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 480,
        "pixel_width": 854,
        "frame_rate": 15,
    }

    EXTRA_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 480,
        "pixel_width": 854,
        "frame_rate": 3,
    }
else:
    PRODUCTION_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 2560,
        "pixel_width": 1440,
        "frame_rate": 60,
    }

    HIGH_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 1920,
        "pixel_width": 1080,
        "frame_rate": 60,
    }

    MEDIUM_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 1280,
        "pixel_width": 720,
        "frame_rate": 30,
    }

    LOW_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 854,#848,864
        "pixel_width": 480,#477,486
        "frame_rate": 15,
    }

    EXTRA_QUALITY_CAMERA_CONFIG = {
        "pixel_height": 854,#848,864
        "pixel_width": 480,#477,486
        "frame_rate": 3,
    }
#2560,1920,1280,1024,864,720,704
#1440,1080,720,576,486,405,396
DEFAULT_POINT_DENSITY_2D = 25
DEFAULT_POINT_DENSITY_1D = 250

# Sizes relevant to default camera frame

FRAME_HEIGHT = 8.0
FRAME_WIDTH = FRAME_HEIGHT * ASPECT_RATIO
def fwidth(ASPECT_RATIO):return FRAME_HEIGHT * ASPECT_RATIO
#ASPECT_RATIO=DEFAULT_PIXEL_WIDTH / DEFAULT_PIXEL_HEIGHT
FRAME_Y_RADIUS = FRAME_HEIGHT / 2
FRAME_X_RADIUS = FRAME_WIDTH / 2
def fxradius(ASPECT_RATIO):return fwidth(ASPECT_RATIO) / 2

DEFAULT_PIXEL_HEIGHT = PRODUCTION_QUALITY_CAMERA_CONFIG["pixel_height"] #=1440
DEFAULT_PIXEL_WIDTH = PRODUCTION_QUALITY_CAMERA_CONFIG["pixel_width"] #=2560
DEFAULT_FRAME_RATE = 60

SMALL_BUFF = 0.1
MED_SMALL_BUFF = 0.25
MED_LARGE_BUFF = 0.5
LARGE_BUFF = 1

DWELL_BUFF=0.001
TINY_BUFF=0.01
DWELL_RATIO=0.001
TINY_RATIO=0.01
DWELL_TIME=0.001
TINY_TIME=0.01

DEFAULT_MOBJECT_TO_EDGE_BUFFER = MED_LARGE_BUFF
DEFAULT_MOBJECT_TO_MOBJECT_BUFFER = MED_SMALL_BUFF


# All in seconds
DEFAULT_POINTWISE_FUNCTION_RUN_TIME = 3.0
DEFAULT_WAIT_TIME = 1.0

DEFAULT_ANIMATION_RUN_TIME = 1.0
DEFAULT_ANIMATION_LAG_RATIO = 0
DEFAULT_LAGGED_START_LAG_RATIO = 0.05
DEFAULT_FADE_LAG_RATIO = 0

DEFAULT_DOT_RADIUS = 0.08
DEFAULT_SMALL_DOT_RADIUS = 0.04
DEFAULT_MICRO_DOT_RADIUS = 1E-6
DEFAULT_DASH_LENGTH = 0.05
DEFAULT_ARROW_TIP_LENGTH = 0.35

CLOSED_THRESHOLD = 0.001
EPSILON = 1e-8

STRAIGHT_PATH_THRESHOLD = 0.01

#ZEROs=np.array([[-1E-8,0,0],[0,0,0],[0,0,0],[1E-8,0,0]])
ZEROs=np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0]])

XY=YZ=ZX=2
XYZ=3
WXYZ=XYZT=4

OO=ORIGIN = np.array([0., 0., 0.])
OU=UP = np.array([0., 1., 0.])
OD=DOWN = np.array([0., -1., 0.])
RO=RIGHT = np.array([1., 0., 0.])
LO=LEFT = np.array([-1., 0., 0.])
OOI=IN = np.array([0., 0., -1.])
OOT=OUT = np.array([0., 0., 1.])
X_AXIS = np.array([1., 0., 0.])
Y_AXIS = np.array([0., 1., 0.])
Z_AXIS = np.array([0., 0., 1.])
'''
OO=ORIGIN = np.array((0., 0., 0.))
OU=UP = np.array((0., 1., 0.))
OD=DOWN = np.array((0., -1., 0.))
RO=RIGHT = np.array((1., 0., 0.))
LO=LEFT = np.array((-1., 0., 0.))
OOI=IN = np.array((0., 0., -1.))
OOT=OUT = np.array((0., 0., 1.))
X_AXIS = np.array((1., 0., 0.))
Y_AXIS = np.array((0., 1., 0.))
Z_AXIS = np.array((0., 0., 1.))
'''
RH=[1,1,1]
LH=[1,-1,1]

# Useful abbreviations for diagonals
LU = UL = UP + LEFT
RU = UR = UP + RIGHT
LD = DL = DOWN + LEFT
RD = DR = DOWN + RIGHT

TB = TOP = FRAME_Y_RADIUS * UP
BB = BOTTOM = FRAME_Y_RADIUS * DOWN
LB = LEFT_SIDE = FRAME_X_RADIUS * LEFT
RB = RIGHT_SIDE = FRAME_X_RADIUS * RIGHT

PI = np.pi
TAU = 2 * PI
DEGREES = TAU / 360

FFMPEG_BIN = "ffmpeg"


# Related to Text
START_X = 30
START_Y = 20
NORMAL = "NORMAL"
ITALIC = "ITALIC"
OBLIQUE = "OBLIQUE"
BOLD = "BOLD"

DEFAULT_STROKE_WIDTH = 4

# Colors
BLUE_E = "#1C758A"
BLUE_D = "#29ABCA"
BLUE_C = "#58C4DD"
BLUE_B = "#9CDCEB"
BLUE_A = "#C7E9F1"
TEAL_E = "#49A88F"
TEAL_D = "#55C1A7"
TEAL_C = "#5CD0B3"
TEAL_B = "#76DDC0"
TEAL_A = "#ACEAD7"
GREEN_E = "#699C52"
GREEN_D = "#77B05D"
GREEN_C = "#83C167"
GREEN_B = "#A6CF8C"
GREEN_A = "#C9E2AE"
YELLOW_E = "#E8C11C"
YELLOW_D = "#F4D345"
YELLOW_C = "#FFFF00"
YELLOW_B = "#FFEA94"
YELLOW_A = "#FFF1B6"
GOLD_E = "#C78D46"
GOLD_D = "#E1A158"
GOLD_C = "#F0AC5F"
GOLD_B = "#F9B775"
GOLD_A = "#F7C797"
RED_E = "#CF5044"
RED_D = "#E65A4C"
RED_C = "#FC6255"
RED_B = "#FF8080"
RED_A = "#F7A1A3"
MAROON_E = "#94424F"
MAROON_D = "#A24D61"
MAROON_C = "#C55F73"
MAROON_B = "#EC92AB"
MAROON_A = "#ECABC1"
PURPLE_E = "#644172"
PURPLE_D = "#715582"
PURPLE_C = "#9A72AC"
PURPLE_B = "#B189C6"
PURPLE_A = "#CAA3E8"
GREY_E = "#222222"
GREY_D = "#444444"
GREY_C = "#888888"
GREY_B = "#BBBBBB"
GREY_A = "#DDDDDD"
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY_BROWN = "#736357"
DARK_BROWN = "#8B4513"
LIGHT_BROWN = "#CD853F"
PINK = "#D147BD"
LIGHT_PINK = "#DC75CD"
GREEN_SCREEN = "#00FF00"
ORANGE = "#FF862F"
LIGHT_GRAY = LIGHT_GREY = "#BBBBBB"
#Extra
VIOLET="#9400D3"
CYAN="#00FFFF"
LIGHT_BLUE="#0000FF"
LIGHT_GREEN="#ADFF2F"
GREEN="#008000"
SILVER="#C0C0C0"
MAROON="#800000"
OLIVE="#808000"

# Abbreviated names for the "median" colors
BLUE = BLUE_C
TEAL = TEAL_C
GREEN = GREEN_C
YELLOW = YELLOW_C
GOLD = GOLD_C
RED = RED_C
MAROON = MAROON_C
PURPLE = PURPLE_C
GRAY = GREY = GREY_C

COLOR_MAP = {
    "DARK_BLUE": "#236B8E",
    "DARK_BROWN": "#8B4513",
    "LIGHT_BROWN": "#CD853F",
    "BLUE_E": "#1C758A",
    "BLUE_D": "#29ABCA",
    "BLUE_C": "#58C4DD",
    "BLUE_B": "#9CDCEB",
    "BLUE_A": "#C7E9F1",
    "TEAL_E": "#49A88F",
    "TEAL_D": "#55C1A7",
    "TEAL_C": "#5CD0B3",
    "TEAL_B": "#76DDC0",
    "TEAL_A": "#ACEAD7",
    "GREEN_E": "#699C52",
    "GREEN_D": "#77B05D",
    "GREEN_C": "#83C167",
    "GREEN_B": "#A6CF8C",
    "GREEN_A": "#C9E2AE",
    "YELLOW_E": "#E8C11C",
    "YELLOW_D": "#F4D345",
    "YELLOW_C": "#FFFF00",
    "YELLOW_B": "#FFEA94",
    "YELLOW_A": "#FFF1B6",
    "GOLD_E": "#C78D46",
    "GOLD_D": "#E1A158",
    "GOLD_C": "#F0AC5F",
    "GOLD_B": "#F9B775",
    "GOLD_A": "#F7C797",
    "RED_E": "#CF5044",
    "RED_D": "#E65A4C",
    "RED_C": "#FC6255",
    "RED_B": "#FF8080",
    "RED_A": "#F7A1A3",
    "MAROON_E": "#94424F",
    "MAROON_D": "#A24D61",
    "MAROON_C": "#C55F73",
    "MAROON_B": "#EC92AB",
    "MAROON_A": "#ECABC1",
    "PURPLE_E": "#644172",
    "PURPLE_D": "#715582",
    "PURPLE_C": "#9A72AC",
    "PURPLE_B": "#B189C6",
    "PURPLE_A": "#CAA3E8",
    "WHITE": "#FFFFFF",
    "BLACK": "#000000",
    "LIGHT_GRAY": "#BBBBBB",
    "LIGHT_GREY": "#BBBBBB",
    "GRAY": "#888888",
    "GREY": "#888888",
    "DARK_GREY": "#444444",
    "DARK_GRAY": "#444444",
    "DARKER_GREY": "#222222",
    "DARKER_GRAY": "#222222",
    "GREY_BROWN": "#736357",
    "PINK": "#D147BD",
    "LIGHT_PINK": "#DC75CD",
    "GREEN_SCREEN": "#00FF00",
    "ORANGE": "#FF862F",

    "VIOLET":"#9400D3",
    "CYAN":"#00FFFF",
    "LIGHT_BLUE":"#0000FF",
    "LIGHT_GREEN":"#ADFF2F",
    "GREEN":"#008000",
    "SILVER":"#C0C0C0",
    "MAROON":"#800000",
    "OLIVE":"#808000",
}




PALETTE = list(COLOR_MAP.values())
locals().update(COLOR_MAP)
for name in [s for s in list(COLOR_MAP.keys()) if s.endswith("_C")]:
    locals()[name.replace("_C", "")] = locals()[name]

'''
MEDIA_DIR = ""
VIDEO_DIR = ""
VIDEO_OUTPUT_DIR = ""
TEX_DIR = ""
TEXT_DIR = ""
'''

def initialize_directories(config):
    pass
    '''
    global MEDIA_DIR
    global VIDEO_DIR
    global VIDEO_OUTPUT_DIR
    global TEX_DIR
    global TEXT_DIR

    video_path_specified = config["video_dir"] or config["video_output_dir"]

    if not (video_path_specified and config["tex_dir"]):
        if config["media_dir"]:
            MEDIA_DIR = config["media_dir"]
        else:
            MEDIA_DIR = os.path.join(
                os.path.expanduser('~'),
                "Dropbox (3Blue1Brown)/3Blue1Brown Team Folder"
            )
        if not os.path.isdir(MEDIA_DIR):
            MEDIA_DIR = "./media"
        print(
            f"Media will be written to {MEDIA_DIR + os.sep}. You can change "
            "this behavior with the --media_dir flag."
        )
    else:
        if config["media_dir"]:
            print(
                "Ignoring --media_dir, since both --tex_dir and a video "
                "directory were both passed"
            )

    #TEX_DIR = config["tex_dir"] or os.path.join(MEDIA_DIR, "Tex")
    #TEXT_DIR = os.path.join(MEDIA_DIR, "texts")
    if not video_path_specified:
        VIDEO_DIR = os.path.join(MEDIA_DIR, "videos")
        VIDEO_OUTPUT_DIR = os.path.join(MEDIA_DIR, "videos")
    elif config["video_output_dir"]:
        VIDEO_OUTPUT_DIR = config["video_output_dir"]
    else:
        VIDEO_DIR = config["video_dir"]

    for folder in [VIDEO_DIR, VIDEO_OUTPUT_DIR, TEX_DIR, TEXT_DIR]:
        if folder != "" and not os.path.exists(folder):
            os.makedirs(folder)
'''

NOT_SETTING_FONT_MSG = '''
Warning:
You haven't set font.
If you are not using English, this may cause text rendering problem.
You set font like:
text = Text('your text', font='your font')
or:
class MyText(Text):
    CONFIG = {
        'font': 'My Font'
    }
'''

TEX_USE_CTEX = False
TEX_TEXT_TO_REPLACE = "[tex_expression]"#"YourTextHere"
TEMPLATE_TEX_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),"tex_templates",
    "tex_template.tex" if not TEX_USE_CTEX else "ctex_template.tex"
)
with open(TEMPLATE_TEX_FILE, "r") as infile:
    TEMPLATE_TEXT_FILE_BODY = infile.read()
    TEMPLATE_TEX_FILE_BODY = TEMPLATE_TEXT_FILE_BODY.replace(
        TEX_TEXT_TO_REPLACE,
        "\\begin{align*}\n" + TEX_TEXT_TO_REPLACE + "\n\\end{align*}",
    )

HELP_MESSAGE = """
   Usage:
   python extract_scene.py <module> [<scene name>]
   -p preview in low quality
   -s show and save picture of last frame
   -w write result to file [this is default if nothing else is stated]
   -o <file_name> write to a different file_name
   -l use low quality
   -m use medium quality
   -a run and save every scene in the script, or all args for the given scene
   -q don't print progress
   -f when writing to a movie file, export the frames in png sequence
   -t use transperency when exporting images
   -n specify the number of the animation to start from
   -r specify a resolution
   -c specify a background color
"""
SCENE_NOT_FOUND_MESSAGE = """
   {} is not in the script
"""
CHOOSE_NUMBER_MESSAGE = """
Choose number corresponding to desired scene/arguments.
(Use comma separated list for multiple entries)
Choice(s): """
INVALID_NUMBER_MESSAGE = "Fine then, if you don't want to give a valid number I'll just quit"

NO_SCENE_MESSAGE = """
   There are no scenes inside that module
"""


# Streaming related configuration
LIVE_STREAM_NAME = "LiveStream"
TWITCH_STREAM_KEY = "YOUR_STREAM_KEY"
STREAMING_PROTOCOL = "tcp"
STREAMING_IP = "127.0.0.1"
STREAMING_PORT = "2000"
STREAMING_CLIENT = "ffplay"
STREAMING_URL = f"{STREAMING_PROTOCOL}://{STREAMING_IP}:{STREAMING_PORT}?listen"
STREAMING_CONSOLE_BANNER = """
Manim is now running in streaming mode. Stream animations by passing
them to manim.play(), e.g.
>>> c = Circle()
>>> manim.play(ShowCreation(c))
"""

