import unittest
from unittest.mock import Mock, call, patch

from autolog import login_auto


class FirstFieldReached(Exception):
    pass


class InitialWindowMoveTests(unittest.TestCase):
    def test_move_before_first_field(self):
        cases = [
            ([0, 1, 2], [True], [call(28)], False),
            ([0, 1, 2, 3], [False, True], [call(0.4), call(27)], False),
            ([0, 31, 31], [True], [], False),
            ([0, 31, 31], [False], [], True),
        ]
        for times, results, expected_sleeps, warning in cases:
            with self.subTest(times=times, results=results):
                proc = Mock(pid=123)
                proc.poll.return_value = None
                with (
                    patch.object(login_auto, "is_admin", return_value=True),
                    patch.object(login_auto, "acquire_single_instance"),
                    patch.object(login_auto, "screen_size", return_value=(1440, 900)),
                    patch.object(login_auto, "load_key", return_value="key"),
                    patch.object(login_auto, "EXE_PATH") as exe_path,
                    patch.object(login_auto, "start_raidbot", return_value=proc),
                    patch.object(login_auto, "focus_process"),
                    patch.object(login_auto, "move_window_to_origin", side_effect=results) as move,
                    patch.object(login_auto, "fill_field", side_effect=FirstFieldReached),
                    patch.object(login_auto.time, "monotonic", side_effect=times),
                    patch.object(login_auto.time, "sleep") as sleep,
                    patch.object(login_auto.logging, "warning") as log_warning,
                ):
                    exe_path.is_file.return_value = True
                    with self.assertRaises(FirstFieldReached):
                        login_auto.run(False)

                    self.assertEqual(move.call_args_list, [call(123)] * len(results))
                    self.assertEqual(sleep.call_args_list, expected_sleeps)
                    self.assertEqual(log_warning.called, warning)


if __name__ == "__main__":
    unittest.main()
