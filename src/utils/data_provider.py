"""Unified Multi-Format Data Provider Utility.

Supports reading test data from Excel (.xlsx), CSV (.csv), JSON (.json), and YAML (.yaml/.yml).
Implements Strategy Pattern to provide clean, reusable data fetching for Data-Driven Testing.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("DataProvider")


class DataProvider:
    """Enterprise Data Provider class for loading test data from multiple file formats."""

    @staticmethod
    def load_data(file_path: Union[str, Path], key_or_sheet: str | None = None) -> List[Dict[str, Any]]:
        """Load test data based on file extension.

        Args:
            file_path: Path to the data file (.xlsx, .csv, .json, .yaml, .yml)
            key_or_sheet: Sheet name for Excel, or root key for JSON/YAML (optional)

        Returns:
            List of dictionaries representing rows/items of test data.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Test data file not found at path: {path.resolve()}")

        ext = path.suffix.lower()
        logger.info("Loading test data from file: %s (format: %s)", path.name, ext)

        if ext == ".xlsx":
            sheet_name = key_or_sheet or "Sheet1"
            return ExcelReader(path).get_sheet_data(sheet_name)
        elif ext == ".csv":
            return DataProvider._read_csv(path)
        elif ext == ".json":
            return DataProvider._read_json(path, key=key_or_sheet)
        elif ext in (".yaml", ".yml"):
            return DataProvider._read_yaml(path, key=key_or_sheet)
        else:
            raise ValueError(f"Unsupported file extension '{ext}'. Supported: .xlsx, .csv, .json, .yaml, .yml")

    @staticmethod
    def _read_csv(file_path: Path) -> List[Dict[str, Any]]:
        """Read CSV file into a list of dictionaries."""
        data = []
        with open(file_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(dict(row))
        return data

    @staticmethod
    def _read_json(file_path: Path, key: str | None = None) -> List[Dict[str, Any]]:
        """Read JSON file into a list of dictionaries."""
        with open(file_path, mode="r", encoding="utf-8") as json_file:
            content = json.load(json_file)

        if key and isinstance(content, dict):
            content = content.get(key, [])

        if isinstance(content, list):
            return content
        elif isinstance(content, dict):
            return [content]
        return []

    @staticmethod
    def _read_yaml(file_path: Path, key: str | None = None) -> List[Dict[str, Any]]:
        """Read YAML file into a list of dictionaries."""
        with open(file_path, mode="r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)

        if key and isinstance(content, dict):
            content = content.get(key, [])

        if isinstance(content, list):
            return content
        elif isinstance(content, dict):
            return [content]
        return []
