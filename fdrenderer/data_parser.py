import json
from typing import Optional

from pydantic import ValidationError

from .model import DropFile


class DataParser:

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> Optional[dict[str, list[DropFile]]]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return {
                    key: [DropFile(**item) for item in value]
                    for key, value in data.items()
                }

        except FileNotFoundError:
            print(f"Ошибка: Файл '{self.file_path}' не найден.\n{e.with_traceback()}")

        except json.JSONDecodeError:
            print(
                f"Ошибка: Не удалось разобрать файл '{self.file_path}'. Убедитесь, что он в формате JSON.\n{e.with_traceback()}"
            )

        except ValidationError as e:
            print(f"Ошибка валидации данных:\n{e.with_traceback()}")

        return None
