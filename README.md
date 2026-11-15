# code.golf TeX Runner

Offline local test runner for code.golf TeX holes without Docker.

## Requirements
- TeX engine in PATH (`tex` command, e.g. MiKTeX or TeX Live)
- Python 3.8+

## Files
- `runner.py`: runs TeX with code.golf `\argc` / `\argv` and converts DVI output to text.
- `octet.tfm`: font metrics file used by code.golf.
- `dvi-to-text.exe`: Windows binary to decode DVI output.
- `test.py`: test script.

## Usage
```bash
python test.py
```
