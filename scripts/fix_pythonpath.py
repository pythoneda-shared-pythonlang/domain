#!/usr/bin/env python3
"""
pythoneda/scripts/fix_pythonpath.py

This file rewrites entries in PYTHONPATH to use local repositories.

Copyright (C) 2023-today rydnr's pythoneda/base

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import importlib
import importlib.util
import logging
import os
from pathlib import Path
import pkgutil
import sys
from typing import Callable, Dict, List

class FixPythonPath():
    """
    A script to rewrite PYTHONPATH to use local repositories.

    Class name: FixPythonPath

    Responsibilities:
        - Analyze sys.path entries.
        - For each entry, check if they are also available in local folder (relative to the current folder)
        - Print the transformed PYTHONPATH to the standard output.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Initializes the instance.
        """
        super().__init__()

    @classmethod
    def fix_syspath(cls):
        """
        Fixes the sys.path collection to avoid duplicated entries for the specific project
        this class is defined.
        """
        current_folder = Path(os.getcwd()).resolve()
        root_folder = current_folder.parent.parent
        paths_to_remove = []
        paths_to_remove.append(Path(__file__).resolve().parent)
        paths_to_add = []
        break_python_module_loop = False
        for first_folder in [ name for name in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, name)) and name.startswith('pythoneda') ]:
            for second_folder in [ name for name in os.listdir(root_folder / first_folder) if os.path.isdir(root_folder / first_folder / name) ]:
                for python_module in [ name for name in os.listdir(root_folder / first_folder / second_folder) if os.path.isdir(root_folder / first_folder / second_folder / name) and (root_folder / first_folder / second_folder / name / "__init__.py").exists() ]:
                    for path in sys.path:
                        if os.path.isdir(Path(path) / python_module):
                            paths_to_add.append(str(root_folder / first_folder / second_folder))
                            break_python_module_loop = True
                            paths_to_remove.append(path)
                            break
                    if break_python_module_loop:
                        break_python_module_loop = False
                        break

        for path in paths_to_remove:
            if str(path) in sys.path:
                sys.path.remove(str(path))
        for path in paths_to_add:
            if not str(path) in sys.path:
                sys.path.append(str(path))

    @classmethod
    def print_syspath(cls) -> str:
        """
        Prints the syspath so it can be used to define the PYTHONPATH variable.
        :return: The PYTHONPATH variable.
        :rtype: str
        """
        result = "\n".join(sys.path)
        print(result)
        return result

    @classmethod
    def main(cls):
        """
        Runs the application from the command line.
        :param file: The file where this specific instance is defined.
        :type file: str
        """
        cls()
        cls.fix_syspath()
        cls.print_syspath()

if __name__ == "__main__":

    FixPythonPath.main()
