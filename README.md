# PII Masker

A small Python project for masking common personally identifiable information (PII) in CSV files.

The goal is to provide a simple example of **data de-identification** for learning and demonstration purposes.

## What it does

The script reads a CSV file and automatically masks columns with common names such as:

- `name` / `nome`
- `email`
- `phone` / `telefone` / `celular`
- `cpf`

Example:

| Before | After |
|---|---|
| `Ana Souza` | `Person_434ae6a3` |
| `ana.souza@example.com` | `a***@example.com` |
| `11987654321` | `*******4321` |
| `123.456.789-01` | `***.***.***-01` |

Other columns are kept unchanged.

## Project structure

```text
pii-masker/
├── anonymizer.py
├── sample_data.csv
├── requirements.txt
├── output/
├── .gitignore
└── README.md
```

## Installation

Clone the repository and install the dependency:

```bash
pip install -r requirements.txt
```

## Usage

Run:

```bash
python anonymizer.py sample_data.csv
```

The anonymized file will be written to:

```text
output/anonymized_data.csv
```

You can also choose another output path:

```bash
python anonymizer.py sample_data.csv -o my_output.csv
```

## Notes

This project demonstrates simple masking and pseudonymization techniques.

It should **not** be treated as a complete anonymization solution for production or regulatory compliance. True anonymization requires evaluating re-identification risk, indirect identifiers, dataset context, and applicable privacy requirements.

The sample data in this repository is synthetic.

## Possible next steps

Some ideas for future versions:

- configurable masking rules
- automatic PII detection based on values
- support for Excel files
- salted hashing
- reversible tokenization
- unit tests
- command-line configuration
- simple web interface

## Tech

- Python
- pandas

## License

MIT
