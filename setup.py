from cx_Freeze import setup, Executable

target = Executable(
    script="main.py",
    icon="icon.ico"
)

setup(
    name="CYCU Course Selector",
    version="1.3",
    description="CYCU course selector app",
    author="MO7YW4NG",
    options={'bdist_msi': {'initial_target_dir': r'[DesktopFolder]\\CYCU Course Selector'}},
    executables=[target],
)

options={
    'build_exe': {
        'packages': ['requests','json','enum','time','getpass','os'],
#        'include_files': ['config.ini']
    }
}