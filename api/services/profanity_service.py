import os
import re


class ProfanityFilter:
    """
    A class to filter out profanity from text.

    Attributes:
        - banned_words (List[str]): A list of banned words.

    Methods:
        - load_banned_words(file_path: str) -> List[str]: Load banned words from a file.
        - is_profane(text: str) -> bool: Check if the text contains any banned words.
    """

    def __init__(self, file_path: str = None):
        if file_path is None:
            file_path = os.path.join("data", "banned_words.txt")
        self.banned_words = self.load_banned_words(file_path)

    @staticmethod
    def load_banned_words(file_path) -> list:
        """
        Load banned words from a file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                words = [line.strip() for line in file if line.strip()]
                return words
        except FileNotFoundError:
            return []

    def is_profane(self, text) -> bool:
        """
        Check if the text contains any banned words.
        """
        for word in self.banned_words:
            if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                return True
        return False
