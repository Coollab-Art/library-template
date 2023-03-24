def setup_readme(lib_name, needs_imgui):
    from _utils import make_file
    make_file('README.md', f"""# {lib_name}

## Including

To add this library to your project, simply add these {"three" if needs_imgui else "two"} lines to your *CMakeLists.txt*{" and replace `folder/containing/imgui` with the path to the parent folder containing *imgui*" if needs_imgui else ""}:
```cmake
add_subdirectory(path/to/{lib_name}){f'''
target_include_directories({lib_name} SYSTEM PRIVATE folder/containing/imgui)''' if needs_imgui else ""}
target_link_libraries(${{PROJECT_NAME}} PRIVATE {lib_name}::{lib_name})
```

Then include it as:
```cpp
#include <{lib_name}/{lib_name}.hpp>
```

## Running the tests

Simply use "tests/CMakeLists.txt" to generate a project, then run it.<br/>
If you are using VSCode and the CMake extension, this project already contains a *.vscode/settings.json* that will use the right CMakeLists.txt automatically.
""")
