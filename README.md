## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

Using `uv`:

```bash
git clone https://github.com/mahmoudbarzegar/python-paseto.git
cd python-paseto
uv sync
```

Using `pip`:

```bash
git clone https://github.com/mahmoudbarzegar/python-paseto.git
cd python-paseto
pip install paseto
```

## Usage

Run the demo:

```bash
uv run main.py
```

This walks through the full flow — login, access, refresh, and several failure cases — printing each step's result to the console.

## A note on secret keys

`main.py` includes a `generate_key()` helper for creating a new symmetric key. In a real application:

- Generate the key **once** and store it securely (e.g. in a `.env` file or secrets manager)
- **Never** hardcode it or commit it to version control
- Rotate it periodically per your security requirements

## Why PASETO over JWT?

|                             | JWT                                            | PASETO                                                 |
| --------------------------- | ---------------------------------------------- | ------------------------------------------------------ |
| Payload                     | Base64-encoded (readable by anyone)            | Encrypted (unreadable without the key)                 |
| Algorithm confusion attacks | Possible (`alg: none`, key-confusion)          | Not possible — version/purpose is fixed per token type |
| Flexibility                 | Many optional algorithms, easy to misconfigure | Small, fixed set of versions with sane defaults        |

## Development

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting/formatting and [pre-commit](https://pre-commit.com/) for git hooks.

```bash
uv run ruff check .
uv run ruff format --check .
```

## License

MIT
