from utils import *


class Preprocessor:
    def __init__(self, raw_data, params):
        self.data = raw_data
        self.params = params

    def check_data_consistency(self):
        info = self.params["preprocess"]["consistency"]
        abnormal_cases = dict()
        for key in info:
            df_groupby = self.data.groupby(key)[info[key]].nunique()
            df_groupby["sum"] = df_groupby.sum(axis=1)
            abnormal_cases[key] = df_groupby.loc[
                df_groupby["sum"] > len(info[key])
            ].index.tolist()
        return abnormal_cases


if __name__ == "__main__":
    data = load_csv(
        "./data",
        "kaggle_ecommerce_behavior_data_2019_Nov_partial.csv",
        ["event_time"],
        "utf8",
    )
    params = load_json("./params/param_test.json")
    p = Preprocessor(data, params)
    print(p.check_data_consistency())
