def setup_continuous_integration(lib_name, needs_imgui: bool):
    from tooling.internal_utils import make_clean_directory
    from _utils import path_to
    from os.path import join
    make_clean_directory(path_to(join('.github', 'workflows')))

    from _utils import make_file
    make_file(join('.github', 'workflows', 'build_and_run_tests.yml'),
              f"""name: Build and Run tests

on: 
  push:
    branches: [ main ]

  pull_request:
    branches: [ main ]


env:
  TARGET: {lib_name}-tests

jobs:
#-----------------------------------------------------------------------------------------------
  Windows_MSVC_Debug:
    name: Windows MSVC Debug
    runs-on: windows-2022
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake .\\tests -B ${{{{github.workspace}}}}\\build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_C_COMPILER=cl -D CMAKE_CXX_COMPILER=cl 

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}\\build --config Debug --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}\\build\\Debug\\${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  Windows_MSVC_Release:
    name: Windows MSVC Release
    runs-on: windows-2022
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake .\\tests -B ${{{{github.workspace}}}}\\build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_C_COMPILER=cl -D CMAKE_CXX_COMPILER=cl

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}\\build --config Release --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}\\build\\Release\\${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  Windows_Clang_Debug:
    name: Windows Clang Debug
    runs-on: windows-2022
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake .\\tests -B ${{{{github.workspace}}}}\\build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -T ClangCL

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}\\build --config Debug --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}\\build\\Debug\\${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  Windows_Clang_Release:
    name: Windows Clang Release
    runs-on: windows-2022
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake .\\tests -B ${{{{github.workspace}}}}\\build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -T ClangCL

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}\\build --config Release --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}\\build\\Release\\${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  Linux_GCC_Debug:
    name: Linux GCC Debug
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive
    {f'''
    - name: Update package
      run: sudo apt-get update -y

    - name: Install glfw dependencies
      run: sudo apt-get install -y libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev mesa-common-dev''' if needs_imgui else ""}
    
    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Debug -D CMAKE_C_COMPILER=gcc-11 -D CMAKE_CXX_COMPILER=g++-11

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Debug --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}
    
#-----------------------------------------------------------------------------------------------
  Linux_GCC_Release:
    name: Linux GCC Release
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive
    {f'''
    - name: Update package
      run: sudo apt-get update -y
    
    - name: Install glfw dependencies
      run: sudo apt-get install -y libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev mesa-common-dev''' if needs_imgui else ""}
    
    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Release -D CMAKE_C_COMPILER=gcc-11 -D CMAKE_CXX_COMPILER=g++-11

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Release --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  Linux_Clang_Debug:
    name: Linux Clang Debug 
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive
    {f'''
    - name: Update package
      run: sudo apt-get update -y
    
    - name: Install glfw dependencies
      run: sudo apt-get install -y libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev mesa-common-dev''' if needs_imgui else ""}
    
    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Debug -D CMAKE_C_COMPILER=clang -D CMAKE_CXX_COMPILER=clang++

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Debug --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  Linux_Clang_Release:
    name: Linux Clang Release
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive
    {f'''
    - name: Update package
      run: sudo apt-get update -y
    
    - name: Install glfw dependencies
      run: sudo apt-get install -y libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev mesa-common-dev''' if needs_imgui else ""}
    
    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Release -D CMAKE_C_COMPILER=clang -D CMAKE_CXX_COMPILER=clang++

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Release --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}{f'''

#-----------------------------------------------------------------------------------------------
  MacOS_GCC_Debug: 
    name: MacOS GCC Debug
    runs-on: macos-11
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Debug -D CMAKE_C_COMPILER=gcc-11 -D CMAKE_CXX_COMPILER=g++-11

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Debug --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}''' if not needs_imgui else ''}{f''' 
    
#-----------------------------------------------------------------------------------------------
  MacOS_GCC_Release: 
    name: MacOS GCC Release
    runs-on: macos-11
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Release -D CMAKE_C_COMPILER=gcc-11 -D CMAKE_CXX_COMPILER=g++-11

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Release --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}''' if not needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  MacOS_Clang_Debug:
    name: MacOS Clang Debug 
    runs-on: macos-11
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Debug -D CMAKE_C_COMPILER=$(brew --prefix llvm)/bin/clang -D CMAKE_CXX_COMPILER=$(brew --prefix llvm)/bin/clang++

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Debug --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}

#-----------------------------------------------------------------------------------------------
  MacOS_Clang_Release: 
    name: MacOS Clang Release
    runs-on: macos-11
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive

    - name: Configure CMake
      run: cmake ./tests -B ${{{{github.workspace}}}}/build -DWARNINGS_AS_ERRORS_FOR_{lib_name.upper()}=ON -D CMAKE_BUILD_TYPE=Release -D CMAKE_C_COMPILER=$(brew --prefix llvm)/bin/clang -D CMAKE_CXX_COMPILER=$(brew --prefix llvm)/bin/clang++

    - name: Build
      run: cmake --build ${{{{github.workspace}}}}/build --config Release --target ${{{{env.TARGET}}}}

    - name: Run
      run: ${{{{github.workspace}}}}/build/${{{{env.TARGET}}}}{f' -nogpu' if needs_imgui else ''}                 
""")
