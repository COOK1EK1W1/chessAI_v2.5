import cx_Freeze

print("building")

executables = [cx_Freeze.Executable("main2.py")]

cx_Freeze.setup(
    name="idk",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":["FreeSerif.ttf"]}},
    executables = executables
    )
