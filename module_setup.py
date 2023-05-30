import os

def create_file(path, content=""):
    with open(path, 'w') as f:
        f.write(content)

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
def creaate_file(,):
def create_project_structure(project_name, modules):
    create_directory(project_name)
    create_file(os.path.join(project_name, 'README.md'), "# This is the README for project " + project_name + "\n")
    create_file(os.path.join(project_name, '.gitignore'), get_gitgnore())
    create_file(os.path.join(project_name, 'LICENSE'), get_license('2023','Abstract Endeavors'))
    create_file(os.path.join(project_name, '__init__.py'))
    create_file(os.path.join(project_name, 'setup.py'), "# This is the setup.py for project " + project_name + "\n" + create_setup(project_name, project_name, modules))
    create_file(os.path.join(project_name, 'setup_installer.py'),create_setup_installer())
    create_file(os.path.join(project_name, 'pyproject.toml'), create_pyproject_toml())
    create_directory(os.path.join(project_name, 'src'))
    create_file(os.path.join(os.path.join(project_name, 'src'), '__init__.py'))

    for module in modules:
        module_path = os.path.join(project_name, 'src', module)
        create_directory(module_path)
        create_file(os.path.join(module_path, 'setup.py'), "# This is the setup.py for module " + module + "\n" + create_setup(project_name, module, [module]))
        create_file(os.path.join(module_path, 'README.md'), "# This is the README for module " + module + "\n")
        create_file(os.path.join(module_path, 'LICENSE'), get_license('2023','Abstract Endeavors'))
        create_file(os.path.join(module_path, '.gitignore'), get_gitgnore())
        create_file(os.path.join(module_path, '__init__.py'))
        create_file(os.path.join(module_path, 'requirements.txt'), "\n")
        create_file(os.path.join(module_path, 'pyproject.toml'), create_pyproject_toml())
        create_directory(os.path.join(module_path, 'src'))
        create_file(os.path.join(module_path, 'src', '__init__.py'))
        create_file(os.path.join(module_path, 'src', 'main.py'), content=create_main(module))
def create_setup_installer():
    return """import os
import subprocess
from dotenv import load_dotenv
import time
import pexpect

# Load environment variables from .env file
def get_parent_directory():
    globals()['parent_dir'] = os.getcwd()
get_parent_directory()
load_dotenv(parent_dir+'/.env')

def get_sudo_password():
    return os.getenv("SUDO_PASSWORD")

def get_pypi_username():
    return os.getenv("PYPI_USERNAME")

def get_pypi_password():
    return os.getenv("PYPI_PASSWORD")

def get_src_dir():
    globals()['src_dir'] = os.path.join(os.getcwd(),"src")

def get_project_dirs():
    globals()['project_dirs'] = [name for name in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, name))]

def install_setup():
    return "python3 setup.py install"

def install_twine():
    return "pip3 install build twine --break-system-packages"

def build_module():
    return "python3 -m build"

def upload_module():
    username = get_pypi_username()
    password = get_pypi_password()
    cmd = "python3 -m twine upload dist/*"

    child = pexpect.spawn(cmd)
    child.expect("Enter your username: ")
    child.sendline(username)
    child.expect("Enter your password: ")
    child.sendline(password)

    # Wait for the process to finish
    child.expect(pexpect.EOF)
    output = child.before.decode("utf-8")

    # Write output to the output file
    with open("output.txt", "w") as f:
        f.write(output)

    print_cmd(cmd, output)

    return child.exitstatus

def print_cmd(input,output):
    print(f"Command Line Arguments: {input}")
    print(f"Output:\n{output}")

def cmd_run(cmd):
    # Clear the output file before running the command
    with open('output.txt', 'w') as f:
        pass

    cmd += f' >> output.txt; echo END_OF_CMD >> output.txt'  # Add the delimiter at the end of cmd
    print(cmd)
    output = subprocess.call(f'gnome-terminal -- bash -c "{cmd}"', shell=True)

    # Wait until the delimiter appears in the output file
    while True:
        time.sleep(0.5)  # Sleep for a while to reduce CPU usage
        with open('output.txt', 'r') as f:
            lines = f.readlines()
            if lines:  # Check if the file is not empty
                last_line = lines[-1].strip()  # Read the last line of the file
                if last_line == 'END_OF_CMD':
                    break  # Break the loop if the delimiter is found

    # Print the command and its output
    with open('output.txt', 'r') as f:
        output = f.read().strip()  # Read the entire output
    print_cmd(cmd, output)
    print(output)
    # Delete the output file and the bash script
    os.remove('output.txt')

def cmd_run_sudo(cmd):
    cmd_run(f'echo "{get_sudo_password()}" | sudo -S -k {cmd}')

def run_setup_loop():
    get_src_dir()
    get_project_dirs()
    cmd_run_sudo(install_twine())
    for project_dir in project_dirs:
        # Construct the path to the setup.py file
        setup_file = os.path.join(src_dir, project_dir, "setup.py")

        # Check if the setup.py file exists
        if os.path.isfile(setup_file):
            # Change the current directory to the project directory
            os.chdir(os.path.join(src_dir, project_dir))

            print(f"Running setup.py for project: {project_dir}")
            cmd_run_sudo(install_setup())
            cmd_run_sudo(build_module())
            upload_module()

            print(f"Completed setup.py for project: {project_dir}")
            print()

        # Change the current directory back to the "src" directory
        os.chdir(src_dir)

cmd_run(install_twine())
run_setup_loop()
"""
def create_entry_point_list(modules):
    return ', '.join([f'"{module}={module}.main:main"' for module in modules])

def create_setup(package_name, module_name, modules):
    return f"""from setuptools import setup, find_packages
from time import time
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='{module_name}',
    version='0.0.1',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='{module_name} is a Python package.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/{package_name}/{module_name}',
    packages=find_packages(where="src"),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        "Operating System :: OS Independent",
    ],
    package_dir={{"": "src"}},
    python_requires=">=3.6",
    install_requires=[
        # Add your project's requirements here, e.g.,
        # 'numpy>=1.22.0',
        # 'pandas>=1.3.0',
    ],
    entry_points={{
        'console_scripts': [{create_entry_point_list(modules)}]
    }},
)
"""

def create_main(module_name):
    return f"""import os
import importlib.util

excluded_files = ['__pycache__', 'main.py', '__init__.py']
excluded_directories = ['__pycache__']

def import_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_filtered_files(directory):
    modules = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item not in excluded_files:
            if item_path.endswith('.py'):
                modules.append(import_module_from_file(item_path))
        elif os.path.isdir(item_path) and item not in excluded_directories:
            modules.extend(get_filtered_files(item_path))
    return modules

def main():
    print("Hello, this is {module_name}.")
    # You can import and use other modules or functions of {module_name} here.
    script_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(script_path)

    filtered_modules = get_filtered_files(directory_path)

if __name__ == "__main__":
    # Get the absolute directory path of the current script file
    main()
"""

def get_gitgnore():
    return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
"""

def get_license(year, name):
    return f"""MIT License

Copyright (c) {year} {name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def get_modules():
    paths = [
#********insert your module names
    ]

    return [os.path.basename(path)+'_test' for path in paths]

def create_pyproject_toml():
    return """
[build-system]
requires = ["setuptools>=42"]
build-backend = "setuptools.build_meta"
"""

def create_initialize_bash():
    return """pip3 install build twine
python3 -m build
python3 -m twine upload dist/*"""

# specify your project and modules
project_name = 'abstract_package_test'
modules = get_modules() # add your modules here

create_project_structure(project_name, modules)
