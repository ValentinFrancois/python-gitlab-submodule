import unittest

from gitlab_submodule.string_utils import lstrip, rstrip


class TestObjects(unittest.TestCase):

    def test_lstrip_pattern_present(self):
        self.assertEqual(lstrip('FOObar', 'FOO'), 'bar')

    def test_lstrip_pattern_empty(self):
        self.assertEqual(lstrip('FOObar', ''), 'FOObar')

    def test_lstrip_pattern_absent(self):
        self.assertEqual(lstrip('bar', 'FOO'), 'bar')
        self.assertEqual(lstrip('foobar', 'FOO'), 'foobar')

    def test_lstrip_string_empty(self):
        self.assertEqual(lstrip('', 'foo'), '')

    def test_rstrip_pattern_present(self):
        self.assertEqual(rstrip('fooBAR', 'BAR'), 'foo')

    def test_rstrip_pattern_empty(self):
        self.assertEqual(rstrip('fooBAR', ''), 'fooBAR')

    def test_rstrip_pattern_absent(self):
        self.assertEqual(rstrip('foo', 'BAR'), 'foo')
        self.assertEqual(rstrip('foobar', 'BAR'), 'foobar')

    def test_rstrip_string_empty(self):
        self.assertEqual(rstrip('', 'foo'), '')
