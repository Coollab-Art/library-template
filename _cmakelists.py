def cmake_minimum_required():
    return "cmake_minimum_required(VERSION 3.8)"

def setup_cmakelists(lib_name, cpp_version, is_header_only):
    from _utils import make_file
    from os.path import join

    make_file('CMakeLists.txt', cmake_minimum_required() + "\n" +
              cmakelists_body(lib_name, cpp_version, is_header_only))

    make_file(join('tests', 'CMakeLists.txt'), f"""{cmake_minimum_required()}
project({lib_name}-tests)

add_executable(${{PROJECT_NAME}} tests.cpp)
target_compile_features(${{PROJECT_NAME}} PRIVATE {cpp_version})

{enable_warnings("${PROJECT_NAME}", "")}

set({lib_name.upper()}_ENABLE_WARNINGS_AS_ERRORS ON)
add_subdirectory(.. ${{CMAKE_CURRENT_SOURCE_DIR}}/build/{lib_name})
target_link_libraries(${{PROJECT_NAME}} PRIVATE {lib_name}::{lib_name})

add_subdirectory(doctest)
target_link_libraries(${{PROJECT_NAME}} PRIVATE doctest::doctest)
""")


def enable_warnings(lib_name, before_each_line):
    return f"""{before_each_line}if(MSVC)
{before_each_line}    target_compile_options({lib_name} PRIVATE /WX /W4)
{before_each_line}else()
{before_each_line}    target_compile_options({lib_name} PRIVATE -Werror -Wall -Wextra -Wpedantic -pedantic-errors -Wconversion -Wsign-conversion)
{before_each_line}endif()"""


def cmakelists_body(lib_name, cpp_version, is_header_only):
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
{enable_warnings(lib_name, "    ")}
else()
    message("-- [{lib_name}] Not using warnings as errors for {lib_name}")
endif()
"""
