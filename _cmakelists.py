def cmake_minimum_required(version):
    return f"cmake_minimum_required(VERSION {version})"


def setup_cmakelists(lib_name, cpp_version, is_header_only, tests_need_imgui: bool):
    from _utils import make_file
    from os.path import join

    make_file('CMakeLists.txt', cmake_minimum_required("3.8") + "\n\n" +
              f'set(WARNINGS_AS_ERRORS_FOR_{lib_name.upper()} OFF CACHE BOOL "ON iff you want to treat warnings as errors")\n' +
              cmakelists_body(lib_name, cpp_version, is_header_only))

    make_file(join('tests', 'CMakeLists.txt'), f"""{cmake_minimum_required("3.11")}
project({lib_name}-tests)

# ---Create executable---
add_executable(${{PROJECT_NAME}} tests.cpp)
target_compile_features(${{PROJECT_NAME}} PRIVATE {cpp_version})

{setup_warnings(lib_name, "${PROJECT_NAME}")}

# ---Include our library---
add_subdirectory(.. ${{CMAKE_CURRENT_SOURCE_DIR}}/build/{lib_name})
target_link_libraries(${{PROJECT_NAME}} PRIVATE {lib_name}::{lib_name})

# ---Add doctest---
include(FetchContent)
FetchContent_Declare(
    doctest
    GIT_REPOSITORY https://github.com/doctest/doctest
    GIT_TAG b7c21ec5ceeadb4951b00396fc1e4642dd347e5f
)
FetchContent_MakeAvailable(doctest)
target_link_libraries(${{PROJECT_NAME}} PRIVATE doctest::doctest){f'''

# ---Add quick_imgui---
include(FetchContent)
FetchContent_Declare(
    quick_imgui
    GIT_REPOSITORY https://github.com/CoolLibs/quick_imgui
    GIT_TAG 1a2c38b9976d81889799fe1fb3e0c993dd787a70
)
FetchContent_MakeAvailable(quick_imgui)
target_include_directories({lib_name} SYSTEM PRIVATE ${{quick_imgui_SOURCE_DIR}}/lib) # Give our library access to Dear ImGui
target_link_libraries(${{PROJECT_NAME}} PRIVATE quick_imgui::quick_imgui)''' if tests_need_imgui else ""}

# ---Ignore .vscode/settings.json in Git---
find_package(Git QUIET)
if(GIT_FOUND)
    get_filename_component(PARENT_DIR ${{CMAKE_CURRENT_SOURCE_DIR}} DIRECTORY)
    if (EXISTS "${{PARENT_DIR}}/.git")
        execute_process(COMMAND ${{GIT_EXECUTABLE}} update-index --assume-unchanged .vscode/settings.json
            WORKING_DIRECTORY ${{PARENT_DIR}}
            RESULT_VARIABLE ERRORS)
        if(NOT ERRORS EQUAL "0")
            message("Git assume-unchanged failed: ${{ERRORS}}")
        endif()
    else()
        message("No Git repository found.")
    endif()
else()
    message("Git executable not found.")
endif()
""")


def setup_warnings(lib_name, target_name):
    return f"""# ---Set warning level---
if(MSVC)
    target_compile_options({target_name} PRIVATE /W4)
else()
    target_compile_options({target_name} PRIVATE -Wall -Wextra -Wpedantic -pedantic-errors -Wconversion -Wsign-conversion -Wimplicit-fallthrough)
endif()

# ---Maybe enable warnings as errors---
if(WARNINGS_AS_ERRORS_FOR_{lib_name.upper()})
    if(MSVC)
        target_compile_options({target_name} PRIVATE /WX)
    else()
        target_compile_options({target_name} PRIVATE -Werror)
    endif()
endif()"""


def cmakelists_body(lib_name, cpp_version, is_header_only):
    if is_header_only:
        return f"""
add_library({lib_name} INTERFACE)
add_library({lib_name}::{lib_name} ALIAS {lib_name})
target_compile_features({lib_name} INTERFACE {cpp_version})
if(WARNINGS_AS_ERRORS_FOR_{lib_name.upper()})
    target_include_directories({lib_name} INTERFACE include)
else()
    target_include_directories({lib_name} SYSTEM INTERFACE include)
endif()
"""

    else:
        return f"""
add_library({lib_name})
add_library({lib_name}::{lib_name} ALIAS {lib_name})
target_compile_features({lib_name} PUBLIC {cpp_version})

# ---Add source files---
if(WARNINGS_AS_ERRORS_FOR_{lib_name.upper()})
    target_include_directories({lib_name} PUBLIC include)
else()
    target_include_directories({lib_name} SYSTEM PUBLIC include)
endif()
file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS src/*.cpp)
target_sources({lib_name} PRIVATE ${{SRC_FILES}})

{setup_warnings(lib_name, lib_name)}
"""
