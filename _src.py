def setup_src(lib_name):
    from tooling.internal_utils import make_clean_directory
    from _utils import path_to
    make_clean_directory(path_to('src'))

    from _utils import make_file
    from os.path import join
    make_file(join('src', f'{lib_name}.cpp'), f"""#include <{lib_name}/{lib_name}.hpp>

namespace {lib_name} {{


    
}} // namespace {lib_name}
""")
