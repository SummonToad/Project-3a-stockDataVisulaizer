"""Flask front end for the Stock Data Visualizer."""
import csv

from flask import Flask, render_template, request

import api_client
import chart_generator
import data_processor
import validation

app = Flask(__name__)


def load_symbols(path="stocks.csv"):
    """Read stock symbols from the CSV (uses a 'Symbol' column, else column 1)."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0]]
    col = header.index("symbol") if "symbol" in header else 0
    symbols = {r[col].strip().upper() for r in rows[1:] if len(r) > col and r[col].strip()}
    return sorted(symbols)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", symbols=load_symbols(), form={}, errors=[], chart=None,
        chart_types=validation.CHART_TYPES, series=validation.TIME_SERIES,
    )


@app.route("/", methods=["POST"])
def generate():
    symbols = load_symbols()
    form = request.form.to_dict()
    clean, errors = validation.validate(form, symbols)
    chart = None

    if not errors:
        try:
            raw = api_client.fetch_stock_data(clean["symbol"], clean["function"])
            df = data_processor.build_dataframe(raw)
            df = data_processor.filter_by_date(df, clean["start"], clean["end"])
            chart = chart_generator.create_chart(
                df, clean["symbol"], clean["chart_type"], clean["function"],
                clean["start"], clean["end"],
            )
        except (api_client.APIError, data_processor.DataError) as err:
            errors.append(str(err))

    return render_template(
        "index.html", symbols=symbols, form=form, errors=errors, chart=chart,
        chart_types=validation.CHART_TYPES, series=validation.TIME_SERIES,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
