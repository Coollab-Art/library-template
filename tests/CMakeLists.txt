cmake_minimum_required(VERSION 3.11)
project(mylib-tests)

add_executable(${PROJECT_NAME} tests.cpp)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_20)

if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /WX /W4)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Werror -Wall -Wextra -Wpedantic -pedantic-errors -Wconversion -Wsign-conversion)
endif()

set(MYLIB_ENABLE_WARNINGS_AS_ERRORS ON)
add_subdirectory(.. ${CMAKE_CURRENT_SOURCE_DIR}/build/mylib)
target_link_libraries(${PROJECT_NAME} PRIVATE mylib::mylib)

# ---Add doctest---
include(FetchContent)
FetchContent_Declare(
    doctest
    GIT_REPOSITORY https://github.com/doctest/doctest
    GIT_TAG b7c21ec5ceeadb4951b00396fc1e4642dd347e5f
)
FetchContent_MakeAvailable(doctest)
target_link_libraries(${PROJECT_NAME} PRIVATE doctest::doctest)
