from _main import setup, Usage

setup(
    lib_name="mylib",
    cpp_version="cxx_std_20",
    is_header_only=False,
    uses_dear_imgui=Usage.NEVER,
)
