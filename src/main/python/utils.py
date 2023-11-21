import json
import simplejson
import numpy as np
import pandas as pd


def load_csv(dir, filename, timestamp_cols, encoding_type):
    filepath = f"{dir}/{filename}"
    data = pd.read_csv(filepath, parse_dates=timestamp_cols, encoding=encoding_type)
    return data


def load_json(dir):
    with open(dir, encoding="utf-8-sig") as f:
        json_file = json.load(f)
    return json_file


def save_json(data, dir):
    with open(dir, "w", encoding="utf-8-sig") as file:
        file.write(
            simplejson.dumps(data, ignore_nan=True, ensure_ascii=False, indent=3)
        )


def save_csv(data, dir, encoding="utf8"):
    data.to_csv(dir, encoding=encoding, index=False)


if __name__ == "__main__":
    data = load_csv(
        "./data",
        "kaggle_ecommerce_behavior_data_2019_Nov_partial.csv",
        ["event_time"],
        "utf8",
    )
    print(data)
