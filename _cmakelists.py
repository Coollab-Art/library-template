def setup_cmakelists(lib_name, cpp_version, is_header_only):
    from _utils import make_file
    make_file('CMakeLists.txt', "cmake_minimum_required(VERSION 3.8)\n" +
              cmakelists_body(lib_name, cpp_version, is_header_only))


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
    if(MSVC)
        target_compile_options({lib_name} PRIVATE /WX /W4)
    else()
        target_compile_options({lib_name} PRIVATE -Werror -Wall -Wextra -Wpedantic -pedantic-errors -Wconversion -Wsign-conversion)
    endif()
else()
    message("-- [{lib_name}] Not using warnings as errors for {lib_name}")
endif()
"""
