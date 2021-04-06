import os
import hashlib
from contextlib import contextmanager

from manimlib.utils.directories import get_tex_dir
from manimlib.config import get_manim_dir
from manimlib.config import get_custom_config

from manimlib.constants import TEX_TEXT_TO_REPLACE
from manimlib.constants import TEX_USE_CTEX

SAVED_TEX_CONFIG = {}


def get_tex_config():
    """
    Returns a dict which should look something like this:
    {
        "executable": "latex",
        "template_file": "tex_template.tex",
        "intermediate_filetype": "dvi",
        "text_to_replace": "YourTextHere",
        "tex_body": "..."
    }
    """
    # Only load once, then save thereafter
    if not SAVED_TEX_CONFIG:
        custom_config = get_custom_config()
        SAVED_TEX_CONFIG.update(custom_config["tex"])
        # Read in template file
        template_filename = os.path.join(
            get_manim_dir(), "manimlib", "tex_templates",
            SAVED_TEX_CONFIG["template_file"],
        )
        with open(template_filename, "r") as file:
            SAVED_TEX_CONFIG["tex_body"] = file.read()
    return SAVED_TEX_CONFIG


def tex_hash(*args):
    if len(args)==1:
        tex_file_content=args[0]
        # Truncating at 16 bytes for cleanliness
        hasher = hashlib.sha256(tex_file_content.encode())
        return hasher.hexdigest()[:16]
    else:
        expression, template_tex_file_body=args
        id_str = str(expression + template_tex_file_body)
        hasher = hashlib.sha256()
        hasher.update(id_str.encode())
        # Truncating at 16 bytes for cleanliness
        return hasher.hexdigest()[:16]


def tex_to_svg_file(*args):
    if len(args)==1:
        tex_file_content=args[0]
        svg_file = os.path.join(
            get_tex_dir(), tex_hash(tex_file_content) + ".svg"
        )
        if not os.path.exists(svg_file):
            # If svg doesn't exist, create it
            tex_to_svg(tex_file_content, svg_file)
        return svg_file
    else:
        expression, template_tex_file_body=args
        tex_file = generate_tex_file(expression, template_tex_file_body)
        dvi_file = tex_to_dvi(tex_file)
        return dvi_to_svg(dvi_file)


def tex_to_svg(tex_file_content, svg_file):
    tex_file = svg_file.replace(".svg", ".tex")
    with open(tex_file, "w", encoding="utf-8") as outfile:
        outfile.write(tex_file_content)
    svg_file = dvi_to_svg(tex_to_dvi(tex_file))

    # Cleanup superfluous documents
    tex_dir, name = os.path.split(svg_file)
    stem, end = name.split(".")
    for file in filter(lambda s: s.startswith(stem), os.listdir(tex_dir)):
        if not file.endswith(end):
            os.remove(os.path.join(tex_dir, file))

    return svg_file


def generate_tex_file(expression, template_tex_file_body):
    result = os.path.join(
        get_tex_dir(),
        tex_hash(expression, template_tex_file_body)
    ) + ".tex"
    if not os.path.exists(result):
        print("Writing \"%s\" to %s" % (
            "".join(expression), result
        ))
        new_body = template_tex_file_body.replace(
            TEX_TEXT_TO_REPLACE, expression
        )
        with open(result, "w", encoding="utf-8") as outfile:
            outfile.write(new_body)
    return result


def tex_to_dvi(tex_file):
    result = tex_file.replace(".tex", ".dvi" if not TEX_USE_CTEX else ".xdv")
    if not os.path.exists(result):
        commands = [
            "latex",
            "-interaction=batchmode",
            "-halt-on-error",
            "-output-directory=\"{}\"".format(get_tex_dir()),
            "\"{}\"".format(tex_file),
            ">",
            os.devnull
        ] if not TEX_USE_CTEX else [
            "xelatex",
            "-no-pdf",
            "-interaction=batchmode",
            "-halt-on-error",
            "-output-directory=\"{}\"".format(get_tex_dir()),
            "\"{}\"".format(tex_file),
            ">",
            os.devnull
        ]
        exit_code = os.system(" ".join(commands))
        if exit_code != 0:
            log_file = tex_file.replace(".tex", ".log")
            raise Exception(
                ("Latex error converting to dvi. " if not TEX_USE_CTEX
                 else "Xelatex error converting to xdv. ") +
                "See log output above or the log file: %s" % log_file)
    return result


def dvi_to_svg(dvi_file, regen_if_exists=False):
    """
    Converts a dvi, which potentially has multiple slides, into a
    directory full of enumerated pngs corresponding with these slides.
    Returns a list of PIL Image objects for these images sorted as they
    where in the dvi
    """
    result = dvi_file.replace(".dvi" if not TEX_USE_CTEX else ".xdv", ".svg")
    if not os.path.exists(result):
        commands = [
            "dvisvgm",
            "\"{}\"".format(dvi_file),
            "-n",
            "-v",
            "0",
            "-o",
            "\"{}\"".format(result),
            ">",
            os.devnull
        ]
        os.system(" ".join(commands))
    return result


# TODO, perhaps this should live elsewhere
@contextmanager
def display_during_execution(message):
    # Only show top line
    to_print = message.split("\n")[0]
    try:
        print(to_print, end="\r")
        yield
    finally:
        print(" " * len(to_print), end="\r")
