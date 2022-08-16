from enum import Enum, auto


def clear_setup_scripts():
    from _utils import path_to, remove
    from tooling.internal_utils import remove_directory
    remove(path_to('_cmakelists.py'))
    remove(path_to('_continuous_integration.py'))
    remove(path_to('_imgui_ini.py'))
    remove(path_to('_include.py'))
    remove(path_to('_license.py'))
    remove(path_to('_main.py'))
    remove(path_to('_readme.py'))
    remove(path_to('_src.py'))
    remove(path_to('_tests.py'))
    remove(path_to('_utils.py'))
    remove(path_to('setup.py'))
    remove_directory(path_to('__pycache__'))


def commit_in_git():
    import os
    os.system('git add .')
    os.system('git commit -m "🎉 Initial commit" --amend')


class Usage(Enum):
    NEVER = auto()
    TESTS_ONLY = auto()
    ALWAYS = auto()


def setup(
    lib_name="mylib",
    cpp_version="cxx_std_20",
    is_header_only=False,
    uses_dear_imgui=Usage.NEVER,
):
    tests_need_imgui = uses_dear_imgui in [Usage.TESTS_ONLY, Usage.ALWAYS]
    from _readme import setup_readme
    setup_readme(lib_name, uses_dear_imgui == Usage.ALWAYS)
    from _license import setup_license
    setup_license()
    from _cmakelists import setup_cmakelists
    setup_cmakelists(lib_name, cpp_version, is_header_only, tests_need_imgui)
    from _tests import setup_tests
    setup_tests(lib_name, tests_need_imgui)
    if (tests_need_imgui):
        from _imgui_ini import setup_imgui_ini
        setup_imgui_ini(lib_name)
    if not is_header_only:
        from _src import setup_src
        setup_src(lib_name)
    else:
        from tooling.internal_utils import remove_directory
        remove_directory('src')
    from _include import setup_include
    setup_include(lib_name)
    from _continuous_integration import setup_continuous_integration
    setup_continuous_integration(lib_name, tests_need_imgui)

    clear_setup_scripts()
    commit_in_git()
