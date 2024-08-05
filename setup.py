from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['ttkbootstrap'], 'excludes': [], 'include_files':['assets/', 'README.md'] }

base = 'gui'

executables = [
    Executable('main.py', base=base, target_name = 'Thermal Threes', icon='assets/tree-blue.ico')
]

setup(name='Thermal Trees',
      version = '3.0',
      author='Isaac vega Salgado',
      author_email='isaacvega361@gmail.com',
      description = 'Thermal Trees',
      options = {'build_exe': build_options},
      executables = executables)
