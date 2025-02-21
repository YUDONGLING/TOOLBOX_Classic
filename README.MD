# General Dev ToolBox for Python 3.X
For Git Repository, to add ToolBox as a submodule, use Git and run:
```
cd "{{ THE_PATH_OF_GIT_REPOSITORY }}"
git submodule add "https://github.com/YUDONGLING/TOOLBOX_Classic.git" "Pkg"
```
For Git Repository, to checkout ToolBox, use Git and run:
```
git submodule init
git submodule update
```
For Windows Filesystem, use CMD and run:
```
mklink /j "{{ THE_PATH_YOU_LIKE_TO_USE_TOOLBOX }}\Pkg" "{{ THE_PATH_OF_THE_TOOLBOX }}"
```
For MacOS Filesystem, use Termail and run:
```
ln -s {{ THE_PATH_OF_THE_TOOLBOX }} {{ THE_PATH_YOU_LIKE_TO_USE_TOOLBOX }}/Pkg
```
