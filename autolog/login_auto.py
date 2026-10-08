"""Autostart: uruchamia RaidBot.exe i klika sekwencje na ekranie 1440x900.

Odstep miedzy kliknieciami: 10 s.
Po zalogowaniu do Windows (flaga --from-autostart) czeka az pulpit wstanie.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.wintypes
import logging
import os
import random
import subprocess
import sys
import time
from pathlib import Path

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
shell32 = ctypes.WinDLL("shell32", use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
VK_CONTROL = 0x11
VK_MENU = 0x12
VK_A = 0x41
VK_BACK = 0x08
SW_RESTORE = 9
ERROR_ALREADY_EXISTS = 183
ERROR_ELEVATION_REQUIRED = 740
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_SHOWWINDOW = 0x0040
HWND = ctypes.c_void_p
LPARAM = ctypes.c_void_p
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, HWND, LPARAM)
ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong

EXE_PATH = Path(r"C:\Windows 11\raid-bot\RaidBot.exe")
USERNAME = "kamzza2"
CLICK_GAP = 10.0
DESKTOP_SETTLE = 25.0
HERE = Path(__file__).resolve().parent
LOG_PATH = HERE / "login_auto.log"
MUTEX_NAME = "Local\\RaidBotAutoLogin"

# (nazwa, x, y, tekst albo None)
STEPS = [
    ("username", 70, 180, USERNAME),
    ("key", 70, 235, "KEY"),
    ("login", 150, 340, None),
    ("settings", 80, 240, None),
    ("preset dropdown", 330, 90, None),
]
PRESETS = (
    ("preset1", 330, 127),
    ("preset2", 330, 143),
)
START_STEP = ("start", 460, 350, None)


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ULONG_PTR),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ULONG_PTR),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("union", INPUTUNION)]


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def enable_dpi_awareness() -> None:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            user32.SetProcessDPIAware()
        except Exception:
            pass
    user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
    user32.GetCursorPos.argtypes = [ctypes.POINTER(ctypes.wintypes.POINT)]
    user32.ShowWindow.argtypes = [HWND, ctypes.c_int]
    user32.BringWindowToTop.argtypes = [HWND]
    user32.SetForegroundWindow.argtypes = [HWND]
    user32.SetForegroundWindow.restype = ctypes.c_bool
    user32.IsWindowVisible.argtypes = [HWND]
    user32.IsWindowVisible.restype = ctypes.c_bool
    user32.GetWindowThreadProcessId.argtypes = [HWND, ctypes.POINTER(ctypes.c_ulong)]
    user32.GetWindowThreadProcessId.restype = ctypes.c_ulong
    user32.EnumWindows.argtypes = [WNDENUMPROC, LPARAM]
    user32.AttachThreadInput.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool]
    user32.GetSystemMetrics.argtypes = [ctypes.c_int]
    user32.GetSystemMetrics.restype = ctypes.c_int
    user32.GetWindowRect.argtypes = [HWND, ctypes.POINTER(RECT)]
    user32.GetWindowRect.restype = ctypes.c_bool
    user32.SetWindowPos.argtypes = [
        HWND,
        HWND,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_uint,
    ]
    user32.SetWindowPos.restype = ctypes.c_bool
    user32.keybd_event.argtypes = [ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ulong, ULONG_PTR]
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
    kernel32.CreateMutexW.restype = ctypes.c_void_p
    kernel32.GetCurrentThreadId.restype = ctypes.c_ulong
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_bool
    shell32.IsUserAnAdmin.restype = ctypes.c_bool
    shell32.ShellExecuteW.argtypes = [
        HWND,
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_int,
    ]
    shell32.ShellExecuteW.restype = ctypes.c_void_p


def setup_logging() -> None:
    handlers: list[logging.Handler] = [logging.FileHandler(LOG_PATH, encoding="utf-8")]
    if sys.stdout is not None:
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", handlers=handlers)


def acquire_single_instance() -> None:
    kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
        logging.info("Inna kopia juz dziala, koncze.")
        raise SystemExit(0)


def is_admin() -> bool:
    try:
        return bool(shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_elevated() -> None:
    script = str(Path(__file__).resolve())
    params = subprocess.list2cmdline([script, *sys.argv[1:]])
    show = 0 if Path(sys.executable).name.lower() == "pythonw.exe" else 1
    logging.info("RaidBot wymaga administratora. Uruchamiam skrypt ponownie z uprawnieniami administratora.")
    result = shell32.ShellExecuteW(None, "runas", sys.executable, params, str(HERE), show)
    code = int(result or 0)
    if code <= 32:
        raise SystemExit(
            f"Nie udalo sie podniesc uprawnien (kod {code}). Na oknie UAC kliknij Tak."
        )
    raise SystemExit(0)


def send_inputs(*inputs: INPUT) -> None:
    arr = (INPUT * len(inputs))(*inputs)
    sent = user32.SendInput(len(inputs), arr, ctypes.sizeof(INPUT))
    if sent != len(inputs):
        raise ctypes.WinError(ctypes.get_last_error())


def mouse_input(flags: int) -> INPUT:
    inp = INPUT(type=INPUT_MOUSE)
    inp.union.mi = MOUSEINPUT(0, 0, 0, flags, 0, 0)
    return inp


def key_input(vk: int = 0, scan: int = 0, flags: int = 0) -> INPUT:
    inp = INPUT(type=INPUT_KEYBOARD)
    inp.union.ki = KEYBDINPUT(vk, scan, flags, 0, 0)
    return inp


def click(x: int, y: int) -> None:
    if not user32.SetCursorPos(x, y):
        raise ctypes.WinError(ctypes.get_last_error())
    time.sleep(0.12)
    send_inputs(mouse_input(MOUSEEVENTF_LEFTDOWN))
    time.sleep(0.06)
    send_inputs(mouse_input(MOUSEEVENTF_LEFTUP))
    time.sleep(0.15)


def hotkey_ctrl_a() -> None:
    send_inputs(key_input(vk=VK_CONTROL), key_input(vk=VK_A))
    time.sleep(0.05)
    send_inputs(
        key_input(vk=VK_A, flags=KEYEVENTF_KEYUP),
        key_input(vk=VK_CONTROL, flags=KEYEVENTF_KEYUP),
    )
    time.sleep(0.05)


def press_backspace() -> None:
    send_inputs(key_input(vk=VK_BACK), key_input(vk=VK_BACK, flags=KEYEVENTF_KEYUP))
    time.sleep(0.05)


def type_text(text: str) -> None:
    for ch in text:
        scan = ord(ch)
        send_inputs(
            key_input(scan=scan, flags=KEYEVENTF_UNICODE),
            key_input(scan=scan, flags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP),
        )
        time.sleep(0.015)


def fill_field(x: int, y: int, text: str) -> None:
    click(x, y)
    time.sleep(0.2)
    hotkey_ctrl_a()
    press_backspace()
    type_text(text)


def load_key() -> str:
    candidates = [
        HERE / "keys.txt",
        HERE / "keys",
        EXE_PATH.parent / "keys.txt",
        EXE_PATH.parent / "keys",
    ]
    path = next((item for item in candidates if item.is_file()), None)
    if path is None:
        raise SystemExit("Brak pliku keys.txt (ani keys) obok skryptu albo obok RaidBot.exe")
    keys = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not keys:
        raise SystemExit(f"Plik kluczy jest pusty: {path}")
    chosen = random.choice(keys)
    logging.info("Klucz %s/%s z %s", keys.index(chosen) + 1, len(keys), path)
    return chosen


def windows_for_pid(pid: int) -> list[int]:
    found: list[int] = []

    def callback(hwnd: int, _lparam: int) -> bool:
        proc_id = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
        if proc_id.value == pid and user32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True

    enum_proc = WNDENUMPROC(callback)
    user32.EnumWindows(enum_proc, 0)
    return found


def main_window(pid: int) -> int | None:
    hwnds = windows_for_pid(pid)
    if not hwnds:
        return None
    best = hwnds[0]
    best_area = -1
    rect = RECT()
    for hwnd in hwnds:
        if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            continue
        area = max(0, rect.right - rect.left) * max(0, rect.bottom - rect.top)
        if area > best_area:
            best_area = area
            best = hwnd
    return best


def move_window_to_origin(pid: int) -> bool:
    hwnd = main_window(pid)
    if not hwnd:
        return False
    user32.ShowWindow(hwnd, SW_RESTORE)
    moved = user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOZORDER | SWP_SHOWWINDOW)
    if moved:
        logging.info("Okno RaidBot przesuniete na 0,0.")
    return bool(moved)


def focus_process(pid: int) -> None:
    hwnd = main_window(pid)
    if not hwnd:
        logging.info("Nie widze jeszcze okna RaidBot (pid %s), klikam i tak.", pid)
        return
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.BringWindowToTop(hwnd)
    fg = user32.GetForegroundWindow()
    current = kernel32.GetCurrentThreadId()
    fg_thread = user32.GetWindowThreadProcessId(fg, None)
    target_thread = user32.GetWindowThreadProcessId(hwnd, None)
    user32.AttachThreadInput(current, fg_thread, True)
    user32.AttachThreadInput(current, target_thread, True)
    user32.keybd_event(VK_MENU, 0, 0, 0)
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
    user32.AttachThreadInput(current, target_thread, False)
    user32.AttachThreadInput(current, fg_thread, False)
    time.sleep(0.2)


def screen_size() -> tuple[int, int]:
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def start_raidbot() -> subprocess.Popen[bytes]:
    try:
        return subprocess.Popen([str(EXE_PATH)], cwd=str(EXE_PATH.parent))
    except OSError as exc:
        if getattr(exc, "winerror", None) != ERROR_ELEVATION_REQUIRED:
            raise
        if not is_admin():
            relaunch_elevated()
        raise SystemExit(
            "RaidBot wymaga administratora, ale uruchomienie i tak zostalo odrzucone."
        ) from exc


def run(from_autostart: bool) -> None:
    if not is_admin():
        relaunch_elevated()
    acquire_single_instance()
    width, height = screen_size()
    logging.info("Ekran %sx%s (oczekiwane 1440x900).", width, height)
    if (width, height) != (1440, 900):
        logging.warning("Rozdzielczosc inna niz 1440x900. Wspolrzedne moga nie trafic.")

    key = load_key()
    if not EXE_PATH.is_file():
        raise SystemExit(f"Nie znaleziono EXE: {EXE_PATH}")

    if from_autostart:
        logging.info("Autostart: czekam %.0f s az pulpit wstanie.", DESKTOP_SETTLE)
        time.sleep(DESKTOP_SETTLE)

    logging.info("Uruchamiam %s", EXE_PATH)
    proc = start_raidbot()
    logging.info("Czekam %.0f s na okno i przesuwam je na 0,0.", CLICK_GAP)
    deadline = time.monotonic() + CLICK_GAP
    while time.monotonic() < deadline:
        if move_window_to_origin(proc.pid):
            break
        time.sleep(0.4)
    remaining = deadline - time.monotonic()
    if remaining > 0:
        time.sleep(remaining)
    if not move_window_to_origin(proc.pid):
        logging.warning("Nie udalo sie przesunac okna RaidBot na 0,0.")

    preset_name, preset_x, preset_y = random.choice(PRESETS)
    logging.info("Wylosowany preset: %s (%s,%s)", preset_name, preset_x, preset_y)
    steps = [*STEPS, (preset_name, preset_x, preset_y, None), START_STEP]

    for index, (name, x, y, text) in enumerate(steps, start=1):
        if proc.poll() is not None:
            raise SystemExit(f"RaidBot zakonczyl sie przed krokiem {name} (kod {proc.returncode}).")
        focus_process(proc.pid)
        payload = key if text == "KEY" else text
        if payload:
            logging.info("%s/%s %s -> klik %s,%s i wpisanie", index, len(steps), name, x, y)
            fill_field(x, y, payload)
        else:
            logging.info("%s/%s %s -> klik %s,%s", index, len(steps), name, x, y)
            click(x, y)
        if name == "login":
            logging.info("Po loginie ponownie przesuwam okno na 0,0.")
            deadline = time.monotonic() + CLICK_GAP
            while time.monotonic() < deadline:
                if move_window_to_origin(proc.pid):
                    break
                time.sleep(0.4)
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(remaining)
            if not move_window_to_origin(proc.pid):
                logging.warning("Po loginie nie udalo sie przesunac okna na 0,0.")
            continue
        if index != len(steps):
            time.sleep(CLICK_GAP)

    logging.info("Sekwencja skonczona.")


def install_autostart() -> None:
    startup = Path(os.environ["APPDATA"]) / r"Microsoft\Windows\Start Menu\Programs\Startup"
    startup.mkdir(parents=True, exist_ok=True)
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    interpreter = pythonw if pythonw.is_file() else Path(sys.executable)
    script = Path(__file__).resolve()
    vbs_path = startup / "RaidBotAutoLogin.vbs"
    vbs = (
        'Set sh = CreateObject("Wscript.Shell")\n'
        f'sh.CurrentDirectory = "{script.parent}"\n'
        f'sh.Run """{interpreter}"" ""{script}"" --from-autostart", 0, False\n'
    )
    vbs_path.write_text(vbs, encoding="utf-8")
    print(f"Autostart zapisany: {vbs_path}")
    print(f"Interpreter: {interpreter}")
    print(f"Skrypt: {script}")


def watch_cursor() -> None:
    print("Najedz myszka. Ctrl+C konczy.")
    point = ctypes.wintypes.POINT()
    try:
        while True:
            user32.GetCursorPos(ctypes.byref(point))
            print(f"\rX={point.x:<5} Y={point.y:<5}", end="", flush=True)
            time.sleep(0.4)
    except KeyboardInterrupt:
        print()


def main() -> None:
    enable_dpi_awareness()
    parser = argparse.ArgumentParser(description="Auto-login RaidBot")
    parser.add_argument("--install", action="store_true", help="dodaj skrypt do autostartu Windows")
    parser.add_argument("--from-autostart", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--pos", action="store_true", help="pokaz wspolrzedne kursora")
    args = parser.parse_args()
    if args.install:
        install_autostart()
        return
    if args.pos:
        watch_cursor()
        return
    setup_logging()
    try:
        run(args.from_autostart)
    except SystemExit as exc:
        if exc.code not in (0, None):
            logging.error("%s", exc)
        raise
    except Exception:
        logging.exception("Blad sekwencji")
        raise


if __name__ == "__main__":
    main()
