def setup_tests(lib_name, needs_imgui: bool):
    from _utils import make_file
    from os.path import join
    make_file(join('tests', 'tests.cpp'), f"""#define {"DOCTEST_CONFIG_IMPLEMENT" if needs_imgui else "DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN"}
#include <doctest/doctest.h>
#include <{lib_name}/{lib_name}.hpp>
{f'''#include <quick_imgui/quick_imgui.hpp>

// Learn how to use Dear ImGui: https://coollibs.github.io/contribute/Programming/dear-imgui

auto main(int argc, char* argv[]) -> int
{{
    const int exit_code = doctest::Context{{}}.run(); // Run all unit tests
    const bool should_run_imgui_tests = argc < 2 || strcmp(argv[1], "-nogpu") != 0;
    if (
        should_run_imgui_tests
        && exit_code == 0 // Only open the window if the tests passed; this makes it easier to notice when some tests fail
    )       
    {{
        quick_imgui::loop("{lib_name} tests", []() {{ // Open a window and run all the ImGui-related code
            ImGui::Begin("{lib_name} tests");
            ImGui::End();
            ImGui::ShowDemoWindow();
        }});
    }}
    return exit_code;
}}
''' if needs_imgui else ""}
// Check out doctest's documentation: https://github.com/doctest/doctest/blob/master/doc/markdown/tutorial.md

int factorial(int number)
{{
    return number <= 1 ? number : factorial(number - 1) * number;
}}

TEST_CASE("testing the factorial function")
{{
    CHECK(factorial(1) == 1);
    CHECK(factorial(2) == 2);
    CHECK(factorial(3) == 6);
    CHECK(factorial(10) == 3628800);
}}
""")
