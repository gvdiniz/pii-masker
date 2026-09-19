import argparse
import hashlib
from pathlib import Path

import pandas as pd


NAME_COLUMNS = {"name", "nome", "full_name", "nome_completo"}
EMAIL_COLUMNS = {"email", "e-mail"}
PHONE_COLUMNS = {"phone", "telefone", "celular", "mobile"}
CPF_COLUMNS = {"cpf"}


def mask_name(value: str) -> str:
    """Replace a name with a stable pseudonym based on a SHA-256 hash."""
    value = str(value).strip()
    if not value:
        return value

    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"Person_{digest}"


def mask_email(value: str) -> str:
    """Mask the local part of an email while preserving the domain."""
    value = str(value).strip()
    if "@" not in value:
        return "***"

    local, domain = value.split("@", 1)
    if not local:
        return f"***@{domain}"

    return f"{local[0]}***@{domain}"


def mask_phone(value: str) -> str:
    """Keep only the last 4 digits of a phone number."""
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    if not digits:
        return "***"

    last_four = digits[-4:]
    return f"*******{last_four}"


def mask_cpf(value: str) -> str:
    """Keep only the last 2 digits of a CPF-like identifier."""
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    if len(digits) < 2:
        return "***"

    return f"***.***.***-{digits[-2:]}"


def anonymize_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Apply masking rules based on column names."""
    result = df.copy()
    treated_columns = []

    for column in result.columns:
        normalized = column.strip().lower()

        if normalized in NAME_COLUMNS:
            result[column] = result[column].fillna("").map(mask_name)
            treated_columns.append(column)

        elif normalized in EMAIL_COLUMNS:
            result[column] = result[column].fillna("").map(mask_email)
            treated_columns.append(column)

        elif normalized in PHONE_COLUMNS:
            result[column] = result[column].fillna("").map(mask_phone)
            treated_columns.append(column)

        elif normalized in CPF_COLUMNS:
            result[column] = result[column].fillna("").map(mask_cpf)
            treated_columns.append(column)

    return result, treated_columns


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mask common personally identifiable information (PII) in a CSV file."
    )
    parser.add_argument("input", help="Path to the input CSV file")
    parser.add_argument(
        "-o",
        "--output",
        default="output/anonymized_data.csv",
        help="Path to the output CSV file",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)
    anonymized_df, treated_columns = anonymize_dataframe(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    anonymized_df.to_csv(output_path, index=False)

    print(f"Saved anonymized file to: {output_path}")
    if treated_columns:
        print("Treated columns:", ", ".join(treated_columns))
    else:
        print("No known PII columns were detected.")


if __name__ == "__main__":
    main()
