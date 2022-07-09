def clear_setup_scripts():
    from _utils import path_to, remove
    from tooling.internal_utils import remove_directory
    remove(path_to('_cmakelists.py'))
    remove(path_to('_include.py'))
    remove(path_to('_main.py'))
    remove(path_to('_readme.py'))
    remove(path_to('_src.py'))
    remove(path_to('_tests.py'))
    remove(path_to('_utils.py'))
    remove(path_to('setup.py'))
    remove_directory(path_to('__pycache__'))


def setup(
    lib_name="mylib",
    cpp_version="cxx_std_20",
    is_header_only=False,
):
    from _readme import setup_readme
    setup_readme(lib_name)
    from _cmakelists import setup_cmakelists
    setup_cmakelists(lib_name, cpp_version, is_header_only)
    from _tests import setup_tests
    setup_tests(lib_name)
    if not is_header_only:
        from _src import setup_src
        setup_src(lib_name)
    else:
        from tooling.internal_utils import remove_directory
        remove_directory('src')
    from _include import setup_include
    setup_include(lib_name)

    clear_setup_scripts()
