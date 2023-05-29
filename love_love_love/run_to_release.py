import sys
import os
import shutil
import platform
from cx_Freeze import setup, Executable

VERSION = '1.0.1'


if __name__ == '__main__':
    os_family = {'Windows': 'win', 'Darwin': 'mac', 'Linux': 'linux'}[platform.system()]
    sys.argv[:] = [sys.argv[0], 'build']

    buildOptions = dict(
        packages=[],
        excludes=[],
        include_files=[('assets', 'assets')])

    target = Executable(
        'main.py',
        base={'win': 'Win32GUI', 'mac': None, 'linux': None}[os_family],
        targetName='game',
        icon='assets/icon.' + {'win': 'ico', 'mac': 'icns', 'linux': 'ico'}[os_family],
        copyright='Mikhail Shubin',
    )

    setup(
        name='Love',
        version=VERSION,
        description='Love in a maze',
        options={'build_exe': buildOptions},
        executables=[target]
        )

    # zip files
    build_dir = 'build/'+os.listdir('build')[-1]
    print(f'build/love_in_a_maze_{os_family}_v{VERSION}')
    shutil.make_archive(f'build/love_in_a_maze_{os_family}_v{VERSION}', 'zip', build_dir)
