"""
tests/value_object_tests.py

This script contains tests for pythoneda/value_object.py

Copyright (C) 2023-today rydnr's PythonEDA

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
import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from pythoneda.value_object import attribute, primary_key_attribute, sensitive, ValueObject

import asyncio
import re
import unittest

class ValueObjectTests(unittest.IsolatedAsyncioTestCase):
    """
    Defines tests for PythonEDA/value_object.py.

    Class name: ValueObjectTests

    Responsibilities:
        - Validates the functionality of the attribute, primary_key_attribute and sensitive decorators defined in value_object.py

    Collaborators:
        - ValueObject: Some sample instances of a derived class are used in the tests.
    """
    async def test_str_on_non_id_class(self):
        """
        Tests the behavior of __str__ on classes forgetting to call super().__init__()
        """
        sut = Sample1("val1")

        self.assertEqual(str(sut), '{ "a1": "val1", "_internal": { "class": "Sample1" } }')

    async def test_str_on_id_class(self):
        """
        Tests the behavior of __str__ on classes which call super().__init__()
        """
        sut = Sample2("val2")

        pattern = r'\{ "a2": "val2", "_internal": \{ "id": ".*?", "class": "Sample2", "created": ".*?" \} \}'

        self.assertTrue(re.match(pattern, str(sut)))

    async def test_sensitive_decorator_wraps_the_attribute(self):
        """
        Tests the @sensitive actually wraps the value in a SensitiveValue instance.
        """
        sut = Sample3("myPassword")

        pattern = r'\{ "pwd": "\[hidden\]", "_internal": \{ "id": ".*?", "class": "Sample3", "created": ".*?" \} \}'

        self.assertTrue(re.match(pattern, str(sut)), f'{str(sut)} does not match {str(pattern)}')

    async def test_sensitive_decorator_can_coexist_with_a_primary_key_decorator(self):
        """
        Tests the @sensitive_attribute can be used with a primary_key attribute.
        """
        sut = Sample4("myPassword")

        pattern = r'\{ "pk": "\[hidden\]", "_internal": \{ "id": ".*?", "class": "Sample4", "created": ".*?" \} \}'

        self.assertTrue(re.match(pattern, str(sut)), f'{str(sut)} does not match {str(pattern)}')
        self.assertTrue('pk' in sut.__class__.primary_key())

class Sample1(ValueObject):

    def __init__(self, a1):
        self._a1 = a1

    @property
    @attribute
    def a1(self):
        return self._a1

class Sample2(ValueObject):

    def __init__(self, a2):
        super().__init__();
        self._a2 = a2

    @property
    @attribute
    def a2(self):
        return self._a2

class Sample3(ValueObject):

    def __init__(self, sensitiveValue: str):
        super().__init__()
        self._pwd = sensitiveValue

    @property
    @sensitive
    @attribute
    def pwd(self):
        return self._pwd

class Sample4(ValueObject):

    def __init__(self, sensitiveValue: str):
        super().__init__()
        self._pk = sensitiveValue

    @property
    @sensitive
    @primary_key_attribute
    def pk(self):
        return self._pk

if __name__ == '__main__':
    unittest.main()
