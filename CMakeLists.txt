cmake_minimum_required(VERSION 3.8)

add_library(mylib)
add_library(mylib::mylib ALIAS mylib)
target_compile_features(mylib PUBLIC cxx_std_20)
# ---Add source files---
target_include_directories(mylib PUBLIC include)
target_sources(mylib PRIVATE
    src/mylib.cpp
)

if (MYLIB_ENABLE_WARNINGS_AS_ERRORS)
    message("-- [mylib] Enabling warnings as errors for mylib")
    if(MSVC)
        target_compile_options(mylib PRIVATE /WX /W4)
    else()
        target_compile_options(mylib PRIVATE -Werror -Wall -Wextra -Wpedantic -pedantic-errors -Wconversion -Wsign-conversion)
    endif()
else()
    message("-- [mylib] Not using warnings as errors for mylib")
endif()
