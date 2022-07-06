def path_to(name):
    from tooling.internal_utils import parent_folder
    from os.path import join
    return join(parent_folder(), name)


def remove(path):
    import os
    if os.path.exists(path):
        os.remove(path)


def make_file(relative_path, content):
    path = path_to(relative_path)
    remove(path)
    with open(path, 'w') as f:
        f.write(content)


def setup_readme(lib_name):
    make_file('README.md', f"""# {lib_name}
""")


def cmake_body(lib_name, cpp_version, is_header_only):
    if is_header_only:
        return f"""
add_library({lib_name} INTERFACE)
add_library({lib_name}::{lib_name} ALIAS {lib_name})
target_compile_features({lib_name} INTERFACE {cpp_version})
target_include_directories({lib_name} INTERFACE include)
"""

    else:
        return f"""
add_library({lib_name})
add_library({lib_name}::{lib_name} ALIAS {lib_name})
target_compile_features({lib_name} PUBLIC {cpp_version})
# ---Add source files---
target_include_directories({lib_name} PUBLIC include)
target_sources({lib_name} PRIVATE
    src/{lib_name}.cpp
)

if ({lib_name.upper()}_ENABLE_WARNINGS_AS_ERRORS)
    message("-- [{lib_name}] Enabling warnings as errors for {lib_name}")
    if(MSVC)
        target_compile_options({lib_name} PRIVATE /WX /W4)
    else()
        target_compile_options({lib_name} PRIVATE -Werror -Wall -Wextra -Wpedantic -pedantic-errors -Wconversion -Wsign-conversion)
    endif()
else()
    message("-- [{lib_name}] Not using warnings as errors for {lib_name}")
endif()
"""


def setup_cmakelists(lib_name, cpp_version, is_header_only):
    make_file('CMakeLists.txt', "cmake_minimum_required(VERSION 3.8)\n" +
              cmake_body(lib_name, cpp_version, is_header_only))


def remove_this_file():
    print(f"I will remove {__file__}")
    # remove(__file__)


if __name__ == '__main__':
    lib_name = "testlib"
    cpp_version = "cxx_std_17"
    is_header_only = False
    setup_readme(lib_name)
    setup_cmakelists(lib_name, cpp_version, is_header_only)
    remove_this_file()
