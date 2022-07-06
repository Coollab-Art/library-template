def setup_readme(lib_name):
    from _utils import make_file
    make_file('README.md', f"""# {lib_name}
""")
