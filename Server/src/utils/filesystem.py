from __future__ import annotations
from pathlib import Path
from typing import List


def find_all_files_paths(path: Path, list_of_paths: List[str]) -> list[Path]:
  """Retrieves the paths of all the files in the starting directory"""
  for child in path.iterdir():
    if child.is_file() and child.name.lower().endswith(".docx"):
      list_of_paths.append(child)
    elif child.is_dir():
      find_all_files_paths(path / child, list_of_paths)
  return list_of_paths