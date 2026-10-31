import importlib.util
import subprocess
import sys
import unittest
from unittest import mock

import functions


def load_entry(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeBot:
    """A stand-in bot so the chat loop can run without ChatterBot."""

    def __init__(self):
        self.asked = []

    def get_response(self, text):
        self.asked.append(text)
        return "fake answer"


def run_loop(inputs):
    bot = FakeBot()
    printed = []
    with mock.patch("builtins.input", side_effect=inputs), \
            mock.patch("builtins.print", side_effect=lambda *a, **k: printed.append(a)):
        functions.start_chatbot(bot)
    return bot, printed


class IsQuitTests(unittest.TestCase):
    def test_plain_bye_words(self):
        for text in ("bye", "bye jordan", "good bye", "goodbye"):
            self.assertTrue(functions.is_quit(text), text)

    def test_case_and_surrounding_space_do_not_matter(self):
        self.assertTrue(functions.is_quit(" bye"))
        self.assertTrue(functions.is_quit("BYE "))

    def test_non_quit_text(self):
        for text in ("hello", "bye!", "", "good"):
            self.assertFalse(functions.is_quit(text), text)


class StartChatbotTests(unittest.TestCase):
    def test_leading_space_bye_ends_without_asking_bot(self):
        bot, printed = run_loop([" bye"])
        self.assertEqual(bot.asked, [])
        self.assertIn(("Jordan: Good bye and have a blessed day!",), printed)

    def test_empty_line_is_reprompted_not_answered(self):
        bot, _ = run_loop(["", "bye"])
        self.assertEqual(bot.asked, [])

    def test_question_goes_to_bot_and_answer_prints(self):
        bot, printed = run_loop(["Who is the owner of this house?", "bye"])
        self.assertEqual(bot.asked, ["Who is the owner of this house?"])
        self.assertIn(("Jordan:", "fake answer"), printed)

    def test_eof_ends_with_goodbye(self):
        bot, printed = run_loop([EOFError()])
        self.assertEqual(bot.asked, [])
        self.assertIn(("\nJordan: Good bye and have a blessed day!",), printed)


class IdentityTests(unittest.TestCase):
    def test_read_identity_returns_typed_name(self):
        entry = load_entry("main_v2", "main-v2.py")
        with mock.patch("builtins.input", return_value="Mark"):
            self.assertEqual(entry.read_identity(), "Mark")

    def test_read_identity_eof_is_none_not_a_traceback(self):
        entry = load_entry("main_py", "main.py")
        with mock.patch("builtins.input", side_effect=EOFError), \
                mock.patch("builtins.print"):
            self.assertIsNone(entry.read_identity())


class EntryPointTests(unittest.TestCase):
    def run_entry(self, filename, *args, text=""):
        return subprocess.run(
            [sys.executable, filename, *args],
            input=text, capture_output=True, text=True, timeout=30)

    def test_help_exits_0_for_both_entry_points(self):
        for filename in ("main.py", "main-v2.py"):
            result = self.run_entry(filename, "--help")
            self.assertEqual(result.returncode, 0, filename)
            self.assertIn("Usage:", result.stdout, filename)
            self.assertNotIn("Traceback", result.stderr, filename)

    def test_unknown_argument_exits_2_for_both_entry_points(self):
        for filename in ("main.py", "main-v2.py"):
            result = self.run_entry(filename, "--nope")
            self.assertEqual(result.returncode, 2, filename)
            self.assertIn("Usage:", result.stderr, filename)

    def test_missing_chatterbot_is_a_hint_not_a_traceback(self):
        try:
            import chatterbot  # noqa: F401
        except ModuleNotFoundError:
            pass
        else:
            self.skipTest("ChatterBot is installed on this machine")
        for filename in ("main.py", "main-v2.py"):
            result = self.run_entry(filename, text="Mark\nbye\n")
            self.assertEqual(result.returncode, 1, filename)
            self.assertIn("ChatterBot is not installed", result.stderr, filename)
            self.assertNotIn("Traceback", result.stderr, filename)

    def test_importing_an_entry_point_starts_nothing(self):
        result = subprocess.run(
            [sys.executable, "-c", "import main"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
