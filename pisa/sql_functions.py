"""SQL functions for manipulate data"""

GRAD_SORT_MAP = {
    "Major": 1,
    "Hauptmann": 2,
    "Oberleutnant": 3,
    "Leutnant": 4,
    "Fourier": 5,
    "Wachtmeister": 6,
    "Korporal": 7,
    "Gefreiter": 8,
    "Soldat": 8
}


def sql_order_grad(funktion):
    """Sortiert nach dienstgrad."""
    return GRAD_SORT_MAP.get(funktion, 100)
