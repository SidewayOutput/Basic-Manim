import inspect
import itertools as it
import sys
from manimlib.constants import CHOOSE_NUMBER_MESSAGE, INVALID_NUMBER_MESSAGE, NO_SCENE_MESSAGE, SCENE_NOT_FOUND_MESSAGE
from manimlib.scene.scene import Scene
from manimlib.config import get_custom_config
from manimlib.utils.sounds import play_error_sound
from manimlib.utils.sounds import play_finish_sound


class BlankScene(Scene):
    def construct(self):
        exec(get_custom_config()["universal_import_line"])
        self.embed()


def is_child_scene(obj, module):
    if not inspect.isclass(obj):
        return False
    if not issubclass(obj, Scene):
        return False
    if obj == Scene:
        return False
    if not obj.__module__.startswith(module.__name__):
        return False
    return True


def prompt_user_for_choice(scene_classes):
    num_to_class = {}
    for count, scene_class in zip(it.count(1), scene_classes):
        name = scene_class.__name__
        print("%d: %s" % (count, name))
        num_to_class[count] = scene_class
    try:
        user_input = input(CHOOSE_NUMBER_MESSAGE)
        return [
            num_to_class[int(num_str)]
            for num_str in user_input.split(",")
        ]
    except KeyError:
        print(INVALID_NUMBER_MESSAGE)
        sys.exit(2)
        user_input = input(CHOOSE_NUMBER_MESSAGE)
        return [
            num_to_class[int(num_str)]
            for num_str in user_input.split(",")
        ]
    except EOFError:
        sys.exit(1)


def get_scenes_to_render(scene_classes, config):
    if len(scene_classes) == 0:
        print(NO_SCENE_MESSAGE)
        return []
    if config["write_all"]:
        return scene_classes
    result = []
    for scene_name in config["scene_names"]:
        found = False
        for scene_class in scene_classes:
            if scene_class.__name__ == scene_name:
                result.append(scene_class)
                found = True
                break
        if not found and (scene_name != ""):
            print(SCENE_NOT_FOUND_MESSAGE.format(
                scene_name
            ),
                file=sys.stderr
            )
    if result:
        return result
    return [scene_classes[0]] if len(scene_classes) == 1 else prompt_user_for_choice(scene_classes)


def get_scene_classes_from_module(module):
    if hasattr(module, "SCENES_IN_ORDER"):
        return module.SCENES_IN_ORDER
    else:
        return [
            member[1]
            for member in inspect.getmembers(
                module,
                lambda x: is_child_scene(x, module)
            )
        ]


def main(config):
    module = config["module"]
    #scene_config = get_scene_config(config)
    if module is None:
        # If no module was passed in, just play the blank scene
        return [BlankScene]

    all_scene_classes = get_scene_classes_from_module(module)
    scene_classes_to_render = get_scenes_to_render(all_scene_classes, config)
    return scene_classes_to_render


"""
if __name__ == "__main__":
    main()
"""