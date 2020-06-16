def _check_is_dataframe(obj):
    import importlib
    pandas_loader = importlib.find_loader('pandas')
    found = pandas_loader is not None
    if not found: return False
    import pandas as pd
    return isinstance(obj, pd.DataFrame)
