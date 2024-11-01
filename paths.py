import os

CURRENT_FILE_PATH = os.path.abspath(__file__)

ROOT_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), "data")
VACANCIES_JSON_PATH = os.path.join(ROOT_PATH, "vacancies.json")
