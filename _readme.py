def setup_readme(lib_name):
    from _utils import make_file
    make_file('README.md', f"""# {lib_name}

## Including

To add this library to your project, simply add those two lines to your *CMakeLists.txt*:
```cmake
add_subdirectory(path/to/{lib_name})
target_link_libraries(${{PROJECT_NAME}} PRIVATE {lib_name}::{lib_name})
```

Then include it as:
```cpp
#include <{lib_name}/{lib_name}.hpp>
```

## Running the tests

Simply use "tests/CMakeLists.txt" to generate a project, then run it.

<ins>*Detailed steps for VSCode:*</ins>

- Go to *Settings* (<kbd>CTRL</kbd> + <kbd>,</kbd>), select *Workspace*, search for "Source Directory" and set it as `${{workspaceFolder}}/tests`.
- Reload the window (<kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>P</kbd> and search for "Reload Window").
- Delete the CMake cache (<kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>P</kbd> and search for "Delete cache and reconfigure").
- Then the CMake extension should pick it up and you can run the tests as usual with the triangle icon.
""")
