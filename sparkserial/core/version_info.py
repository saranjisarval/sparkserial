import json
import os

try:
    from importlib.metadata import version as _installed_version, PackageNotFoundError
except ImportError:  # pragma: no cover - py<3.8 fallback, not expected given requires-python
    from importlib_metadata import version as _installed_version, PackageNotFoundError

APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".sparkserial")
CONFIG_FILE = os.path.join(APP_DATA_DIR, "config.json")
WHATS_NEW_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "whats_new.json")
LAST_SEEN_VERSION_KEY = "last_seen_version"


def get_current_version():
    """The version of the sparkserial package actually installed/running."""
    try:
        return _installed_version("sparkserial")
    except PackageNotFoundError:
        return "0.0.0"


def _parse_version(version_str):
    """Parses 'X.Y.Z'-style strings into a comparable tuple of ints.
    Any non-numeric suffix (e.g. 'rc1') is ignored rather than raising."""
    parts = []
    for chunk in str(version_str).split('.'):
        digits = ''.join(ch for ch in chunk if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def _load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_config(config):
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass


def get_last_seen_version():
    return _load_config().get(LAST_SEEN_VERSION_KEY)


def set_last_seen_version(version_str):
    # Read-modify-write: config.json also holds unrelated keys (e.g. CommandManager's
    # custom commands_file path), so we must not clobber them.
    config = _load_config()
    config[LAST_SEEN_VERSION_KEY] = version_str
    _save_config(config)


def load_whats_new():
    """Loads the bundled version -> [highlight, ...] map."""
    try:
        with open(os.path.normpath(WHATS_NEW_FILE), 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def get_unseen_release_notes():
    """Returns [(version_str, [highlights]), ...], oldest first, for every released
    version newer than what this user last saw, up to and including the version
    currently installed. Returns [] if there's nothing new to show (including on a
    brand new install, where we just silently record the current version)."""
    last_seen = get_last_seen_version()
    current = get_current_version()
    current_tuple = _parse_version(current)

    if last_seen is None:
        # First-ever launch: nothing to announce, just start tracking from here.
        return []

    last_seen_tuple = _parse_version(last_seen)
    all_notes = load_whats_new()

    unseen = [
        (ver, notes) for ver, notes in all_notes.items()
        if last_seen_tuple < _parse_version(ver) <= current_tuple
    ]
    unseen.sort(key=lambda item: _parse_version(item[0]))
    return unseen
