#!/usr/bin/env python
import traceback
import platform
import os
import sys
import subprocess as sp
import manimlib.config
import manimlib.extract_scene
import manimlib.stream_starter
from manimlib.utils.sounds import play_error_sound
from manimlib.utils.sounds import play_finish_sound


def get_scene_config(config):
    return dict([
        (key, config[key])
        for key in [
            # "window_config",
            "camera_config",
            "file_writer_config",
            "skip_animations",
            "start_at_animation_number",
            "end_at_animation_number",
            "leave_progress_bars",
            # "preview",
        ]
    ])


def main():
    args = manimlib.config.parse_cli()

    if args.config:
        manimlib.utils.init_config.init_customization()
    else:
        if not args.livestream:
            config = manimlib.config.get_configuration(args)
            scene_config = get_scene_config(config)
            scenes = manimlib.extract_scene.main(config)

            for scene in scenes:
                try:
                    # By invoking, this renders the full scene
                    scene = scene(**scene_config)
                    open_file_if_needed(scene.file_writer, **config)
                    if config["sound"]:
                        play_finish_sound()
                except Exception:
                    print("\n\n")
                    traceback.print_exc()
                    print("\n\n")
                    if config["sound"]:
                        play_error_sound()
        else:
            manimlib.stream_starter.start_livestream(
                to_twitch=args.to_twitch,
                twitch_key=args.twitch_key,
            )


def open_file_if_needed(file_writer, **config):
    if config["quiet"]:
        curr_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    open_file = any([
        config["open_video_upon_completion"],
        config["show_file_in_finder"]
    ])
    if open_file:
        current_os = platform.system()
        file_paths = []

        if config["file_writer_config"]["save_last_frame"]:
            file_paths.append(file_writer.get_image_file_path())
        if config["file_writer_config"]["write_to_movie"]:
            file_paths.append(file_writer.get_movie_file_path())

        for file_path in file_paths:
            if current_os == "Windows":
                os.startfile(file_path)
            else:
                commands = []
                if current_os == "Linux":
                    commands.append("xdg-open")
                elif current_os.startswith("CYGWIN"):
                    commands.append("cygstart")
                else:  # Assume macOS
                    commands.append("open")

                if config["show_file_in_finder"]:
                    commands.append("-R")

                commands.append(file_path)

                # commands.append("-g")
                FNULL = open(os.devnull, 'w')
                sp.call(commands, stdout=FNULL, stderr=sp.STDOUT)
                FNULL.close()

    if config["quiet"]:
        sys.stdout.close()
        sys.stdout = curr_stdout
