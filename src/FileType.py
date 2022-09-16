from enum import Enum

class FileType(Enum):
    IMAGE_FILES = "Image Files"
    TEXT_FILES = "Text Files"
    PDF_FILE = "PDF File"

file_types_list = [
    (FileType.IMAGE_FILES.value, [".jpeg", ".png", ".jpg"]),
    (FileType.TEXT_FILES.value, [".txt"]),
    (FileType.PDF_FILE.value, [".pdf"])
]
