cmake_minimum_required(VERSION 3.8)

set(WARNINGS_AS_ERRORS_FOR_MYLIB OFF CACHE BOOL "ON iff you want to treat warnings as errors")

add_library(mylib)
add_library(mylib::mylib ALIAS mylib)
target_compile_features(mylib PUBLIC cxx_std_20)

# ---Add source files---
if(WARNINGS_AS_ERRORS_FOR_MYLIB)
    target_include_directories(mylib PUBLIC include)
else()
    target_include_directories(mylib SYSTEM PUBLIC include)
endif()
file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS src/*.cpp)
target_sources(mylib PRIVATE ${SRC_FILES})

# ---Set warning level---
if(MSVC)
    target_compile_options(mylib PRIVATE /W4)
else()
    target_compile_options(mylib PRIVATE -Wall -Wextra -Wpedantic -pedantic-errors -Wconversion -Wsign-conversion)
endif()

# ---Maybe enable warnings as errors---
if(WARNINGS_AS_ERRORS_FOR_MYLIB)
    if(MSVC)
        target_compile_options(mylib PRIVATE /WX)
    else()
        target_compile_options(mylib PRIVATE -Werror)
    endif()
endif()
