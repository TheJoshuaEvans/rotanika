import unittest
from utils import display_len, get_version, wrap_line

class TestDisplayLen(unittest.TestCase):
    """Unit tests for display_len."""

    def test_display_len_basic(self):
        """Test basic ASCII characters."""
        text = "Hello, World!"
        expected_length = 13
        self.assertEqual(display_len(text), expected_length)

    def test_display_len_wide_characters(self):
        """Test with wide characters (e.g., CJK characters)."""
        text = "你好，世界！"  # "Hello, World!" in Chinese
        expected_length = 12  # Each Chinese character counts as 2
        self.assertEqual(display_len(text), expected_length)

    def test_display_len_mixed_characters(self):
        """Test with a mix of ASCII and wide characters."""
        text = "Hello 你好"
        expected_length = 10  # 5 (Hello) + 1 (space) + 2*2 (你好)
        self.assertEqual(display_len(text), expected_length)

    def test_display_len_emojis(self):
        """Test with emojis which are typically wide characters."""
        text = "Hello 😊"
        expected_length = 8  # 5 (Hello) + 1 (space) + 2 (emoji)
        self.assertEqual(display_len(text), expected_length)

class TestGetVersion(unittest.TestCase):
    """Unit tests for get_version."""

    def test_get_version(self):
        """Test that get_version returns a non-empty string."""
        version = get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)

class TestWrapLine(unittest.TestCase):
    """Unit tests for wrap_line."""

    def test_wrap_line_basic(self):
        """Test basic wrapping functionality."""
        text = "This is a simple test case for wrapping."
        max_width = 10
        expected = [
            "This is a",
            "simple",
            "test case",
            "for",
            "wrapping."
        ]
        result = wrap_line(text, max_width)
        self.assertEqual(result, expected)

    def test_wrap_line_no_wrap_needed(self):
        """Test case where no wrapping is needed."""
        text = "Short text."
        max_width = 50
        expected = ["Short text."]
        result = wrap_line(text, max_width)
        self.assertEqual(result, expected)

    def test_wrap_line_exact_fit(self):
        """Test case where words fit exactly into the max width."""
        text = "Fit exactly"
        max_width = 12
        expected = ["Fit exactly"]
        result = wrap_line(text, max_width)
        self.assertEqual(result, expected)

    def test_wrap_lines_long_word(self):
        """Test case with a word longer than max width."""
        text = "Supercalifragilisticexpialidocious is a long word."
        max_width = 10
        expected = [
            "Supercalifragilisticexpialidocious",
            "is a long",
            "word."
        ]
        result = wrap_line(text, max_width)
        self.assertEqual(result, expected)

    def test_wrap_lines_strip_leading_spaces(self):
        """Test that leading spaces are stripped from wrapped lines."""
        text = "   Leading spaces should be                 removed."
        max_width = 15
        expected = [
            "Leading spaces",
            "should be      ",
            "removed."
        ]
        result = wrap_line(text, max_width)
        self.assertEqual(result, expected)

    def test_wrap_lines_emojis(self):
        """Test wrapping functionality with emojis, accounting for double-width characters.

        The ghost emoji 👻 is double-width and should be accounted for when wrapping.
        This test exposes if the system is not properly handling double-width emojis.
        """
        text = "Test some emojis🚀 👻 that should be wrapped properly."
        max_width = 20
        expected = [
            "Test some emojis🚀",
            "👻 that should be",
            "wrapped properly."
        ]
        result = wrap_line(text, max_width)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
