def setup_imgui_ini(lib_name):
    from tooling.internal_utils import make_directory_if_necessary
    from _utils import path_to
    from os.path import join
    make_directory_if_necessary(path_to('build'))

    from _utils import make_file
    make_file(join('build', 'imgui.ini'), f"""[Window][MyMainDockSpace]
Pos=0,0
Size=1920,1001
Collapsed=0

[Window][Debug##Default]
Pos=60,60
Size=400,400
Collapsed=0

[Window][Dear ImGui Demo]
Pos=1114,74
Size=550,680
Collapsed=0

[Window][{lib_name} tests]
Pos=0,0
Size=1920,1001
Collapsed=0
DockId=0xF3CABE56,0

[Docking][Data]
DockSpace ID=0xF3CABE56 Window=0x74B75B81 Pos=0,29 Size=1920,1001 CentralNode=1 Selected=0x250A9A24
""")
