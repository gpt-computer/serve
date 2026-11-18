"""Regenerate gptc_cli/autocomplete.py from the canonical CLI parser metadata.

Without --check this overwrites ../gptc_cli/autocomplete.py with the output of
gptc.parsers.get_main_parser(). With --check it compares against the checked-in
file and exits non-zero on drift (no write).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AC_FILE = PROJECT_ROOT / "gptc_cli" / "autocomplete.py"

# Allow this script to run from any working directory, including pre-commit.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _generate():
    from gptc.parsers import get_main_parser

    def _gaa(key, parser):
        _result = {}
        _compl = []
        for v in parser._actions:
            if v.option_strings:
                _compl.extend(v.option_strings)
            elif v.choices:
                _compl.extend(v.choices)
                if isinstance(v.choices, dict):
                    for kk, vv in v.choices.items():
                        _result.update(_gaa(" ".join([key, kk]).strip(), vv))
        # filter out single dash, as they serve as abbrev
        _compl = [k for k in _compl if (not k.startswith("-") or k.startswith("--"))]
        _result.update({key: _compl})
        return _result

    compl = _gaa("", get_main_parser())
    cmd = compl.pop("")
    compl = {"commands": cmd, "completions": compl}
    return f"ac_table = {compl}\n"


def _format(src):
    try:
        import black

        mode = black.FileMode(line_length=88, string_normalization=False)
        return black.format_str(src, mode=mode)
    except ImportError:
        return src


def _update_autocomplete(check=False):
    generated = _format(_generate())
    if check:
        current = AC_FILE.read_text(encoding="utf-8")
        if current != generated:
            print(
                f"autocomplete drift detected in {AC_FILE}; "
                "run `python scripts/update-autocomplete-cli.py` and black -S to regenerate",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"{AC_FILE} is in sync with gptc.parsers.get_main_parser()")
        return
    with open(AC_FILE, "w", encoding="utf-8") as fp:
        fp.write(generated)


if __name__ == "__main__":
    if "--check" in sys.argv:
        _update_autocomplete(check=True)
    else:
        _update_autocomplete()
