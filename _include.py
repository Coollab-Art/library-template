def setup_include(lib_name):
    from tooling.internal_utils import make_clean_directory
    from _utils import path_to
    from os.path import join
    make_clean_directory(path_to('include'))
    make_clean_directory(path_to(join('include', lib_name)))

    from _utils import make_file
    make_file(join('include', lib_name, f'{lib_name}.hpp'), f"""#pragma once

namespace {lib_name} {{


    
}} // namespace {lib_name}
""")
