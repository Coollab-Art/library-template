def path_to(name):
    from tooling.internal_utils import parent_folder
    from os.path import join
    return join(parent_folder(), name)


def remove(path):
    import os
    if os.path.exists(path):
        os.remove(path)


def make_file(relative_path, content):
    path = path_to(relative_path)
    remove(path)
    with open(path, 'w') as f:
        f.write(content)
