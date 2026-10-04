from pathlib import Path

RAW_DIR = Path("/usr/local/airflow/data/raw")
REFINED_DIR = Path("/usr/local/airflow/data/refined")


def delete_all_files(directory: Path, pattern: str):
    if not directory.exists():
        print(f"Directory does not exist: {directory}")
        return

    files = list(directory.glob(pattern))

    if not files:
        print(f"No files found in {directory} with pattern {pattern}")
        return

    for file in files:
        file.unlink()
        print(f"Deleted file: {file}")


def cleanup_raw_files():
    delete_all_files(RAW_DIR, "reddit_raw_*.json")


def cleanup_refined_files():
    delete_all_files(REFINED_DIR, "reddit_transformed_*.csv")