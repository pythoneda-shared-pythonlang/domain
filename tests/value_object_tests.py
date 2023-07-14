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
import re
from typing import Dict, List
import unittest

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from pythoneda.value_object import attribute, internal_attribute, primary_key_attribute, sensitive, ValueObject

class ValueObjectTests(unittest.TestCase):
    """
    Defines tests for pythoneda/value_object.py.

    Class name: ValueObjectTests

    Responsibilities:
        - Validates the functionality of the attribute, primary_key_attribute and sensitive decorators defined in value_object.py

    Collaborators:
        - ValueObject: Some sample instances of a derived class are used in the tests.
    """
    def test_str_on_non_id_class(self):
        """
        Tests the behavior of __str__ on classes forgetting to call super().__init__()
        """
        sut = ValueObjectTests.Sample1("val1")

        self.assertEqual(str(sut), '{ "a1": "val1", "_internal": { "id": null, "created": null, "updated": null, "class": "__main__.Sample1" } }')

    def test_str_on_id_class(self):
        """
        Tests the behavior of __str__ on classes which call super().__init__()
        """
        sut = ValueObjectTests.Sample2("val2")

        pattern = r'\{ "a2": "val2", "_internal": \{ "id": ".*?", "created": ".*?", "updated": null, "class": "__main__.Sample2" \} \}'

        self.assertTrue(re.match(pattern, str(sut)), f'{str(sut)} does not match {str(pattern)}')

    def test_sensitive_decorator_wraps_the_attribute(self):
        """
        Tests the @sensitive actually wraps the value in a SensitiveValue instance.
        """
        sut = ValueObjectTests.Sample3("myPassword")

        pattern = r'\{ "pwd": "\[hidden\]", "_internal": \{ "id": ".*?", "created": ".*?", "updated": null, "class": "__main__.Sample3" \} \}'

        self.assertTrue(re.match(pattern, str(sut)), f'{str(sut)} does not match {str(pattern)}')

    def test_sensitive_decorator_can_coexist_with_a_primary_key_decorator(self):
        """
        Tests the @sensitive_attribute can be used with a primary_key attribute.
        """
        sut = ValueObjectTests.Sample4("myPassword")

        pattern = r'\{ "pk": "\[hidden\]", "_internal": \{ "id": ".*?", "created": ".*?", "updated": null, "class": "__main__.Sample4" \} \}'

        self.assertTrue(re.match(pattern, str(sut)), f'{str(sut)} does not match {str(pattern)}')
        self.assertTrue('pk' in sut.__class__.primary_key())

    def test_bug_when_sensitive_decorator_is_not_the_innermost_decorator(self):
        """
        Tests the @sensitive_attribute can be used with a primary_key attribute.
        """
        sut = ValueObjectTests.Sample5("myPassword")

        pattern = r'\{ "pk": "\[hidden\]", "_internal": \{ "id": ".*?", "created": ".*?", "updated": null, "class": "__main__.Sample5" \} \}'

        self.assertTrue(re.match(pattern, str(sut)), f'{str(sut)} does not match {str(pattern)}')
        self.assertTrue('pk' in sut.__class__.primary_key())

    def test_to_json_with_list(self):
        """
        Tests whether the str() representation of instances with list attributes is JSON compliant.
        """
        sut = ValueObjectTests.Sample6("a string", [ "another string" ], { "internalKey": 13 })

        pattern = r'\{ "a_string": "a string", "a_list": \[ "another string" \], "_internal": \{ "a_dict": \{ "internalKey" \}, "id": ".*?", "created": ".*?", "updated": null, "class": "__main__.Sample6" \} \}'

        self.assertTrue(re.match(pattern, str(sut)), f'{str(sut)} does not match {str(pattern)}')

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
        @primary_key_attribute
        @sensitive
        def pk(self):
            return self._pk

    class Sample5(ValueObject):

        def __init__(self, sensitiveValue: str):
            super().__init__()
            self._pk = sensitiveValue

        @property
        @sensitive
        @primary_key_attribute
        def pk(self):
            return self._pk

    class Sample6(ValueObject):

        def __init__(self, aString:str, aList:List, aDict:Dict):
            super().__init__()
            self._a_string = aString
            self._a_list = aList
            self._a_dict = aDict

        @property
        @primary_key_attribute
        def a_string(self) -> str:
            return self._a_string

        @property
        @attribute
        def a_list(self) -> List:
            return self._a_list

        @property
        @internal_attribute
        def a_dict(self) -> Dict:
            return self._a_dict

if __name__ == '__main__':
    unittest.main()
