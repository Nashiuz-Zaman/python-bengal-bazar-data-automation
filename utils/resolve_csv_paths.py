from pathlib import Path
from typing import Tuple


def resolve_csv_paths(
    *,
    input_csv_name: str,
    replace_from: str | None = None,
    replace_to: str | None = None,
) -> Tuple[Path, Path]:
    """
    Resolve input and output CSV paths inside the csv_data directory.

    Args:
        input_csv_name: Input CSV filename
        replace_from: Substring to replace in input_csv_name
        replace_to: Replacement substring for output CSV name

    Returns:
        (input_csv_path, output_csv_path)
    """
    base_dir = Path(__file__).parent.parent
    csv_dir = base_dir / "csv_data"

    input_csv_path = (csv_dir / input_csv_name).resolve()

    output_csv_name = input_csv_name

    if (replace_from is None) != (replace_to is None):
        raise ValueError("replace_from and replace_to must be provided together")

    if replace_from is not None and replace_to is not None:
        output_csv_name = input_csv_name.replace(replace_from, replace_to)

    output_csv_path = (csv_dir / output_csv_name).resolve()

    return input_csv_path, output_csv_path
