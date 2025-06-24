# Logique métier (filtrage, préparation data, etc...)


from models.accident_model import get_all_accidents, get_accidents_by_year

def fetch_accidents():
    return [dict(row) for row in get_all_accidents()]

def filter_by_year(year):
    return [dict(row) for row in get_accidents_by_year(year)]
