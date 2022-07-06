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
""")
