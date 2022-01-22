"""Get an updated list of holidays from ANBIMA website."""

from typing import List
from requests import get
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)


URL = 'http://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls'
DATE_FORMAT = "%Y-%m-%d"


def _get_binaries_from_web() -> bytes:
    """Read Excel file and get its binary contents."""
    return get(URL).content
# if __name__ == '__main__':
#     print(_get_binaries_from_web())


def _binaries_to_dates_list(binary_content: bytes) -> List[str]:
    """Extract dates list from binaries."""
    df = pd.read_excel(binary_content)
    dates = df.dropna().iloc[:, 0]
    return pd.to_datetime(dates).dt.strftime(DATE_FORMAT).to_list()
# if __name__ == '__main__':
#     binaries = _get_binaries_from_web()
#     print(_binaries_to_dates_list(binaries))


def get_holidays_list() -> List[str]:
    """Get holidays list from ANBIMA webpage."""
    binaries = _get_binaries_from_web()
    return _binaries_to_dates_list(binaries)
# if __name__ == '__main__':
#     print(get_holidays_list())


@app.route('/')
def get_holidays_anbima():
    return jsonify(get_holidays_list())


if __name__ == "__main__":
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
