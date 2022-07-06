def clear_setup_scripts():
    print(f"I will remove {__file__}")
    # remove(__file__)
    # TODO remove setup folder
    # Remove __pycache__


def setup(
    lib_name="",
    cpp_version="cxx_std_20",
    is_header_only=False,
):
    from _readme import setup_readme
    setup_readme(lib_name)
    from _cmakelists import setup_cmakelists
    setup_cmakelists(lib_name, cpp_version, is_header_only)
    from _tests import setup_tests
    setup_tests(lib_name)

    clear_setup_scripts()
