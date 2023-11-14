from utils import *


class Preprocessor:
    def __init__(self, raw_data, params):
        self.data = raw_data
        self.params = params

    def check_data_consistency(self):
        def generate_abnormal_cases():
            info = self.params["preprocess"]["consistency"]
            abnormal_cases = dict()
            for key in info:
                df_groupby = self.data.groupby(key)[info[key]].nunique()
                df_groupby["sum"] = df_groupby.sum(axis=1)
                abnormal_cases[key] = df_groupby.loc[
                    df_groupby["sum"] > len(info[key])
                ].index.tolist()
            return abnormal_cases

        def get_case_details(case_list):
            details = dict()
            for key in case_list:
                if case_list[key]:
                    related_keys = params["preprocess"]["consistency"][key]
                    n_data = self.data.loc[data[key].isin(case_list[key])]
                    details[key] = (
                        n_data.groupby(key)
                        .agg({rkey: "unique" for rkey in related_keys})
                        .to_dict("index")
                    )
            return details

        abnormal_cases = generate_abnormal_cases()
        abnormal_details = get_case_details(abnormal_cases)
        return abnormal_details

    def add_upper_category_column(self):
        # category_code가 세분화되어 있어서, 상위 category 컬럼 생성
        added_data = self.data.copy()
        added_data.loc[
            (~added_data["category_code"].isna())
            & (added_data["category_code"].str.contains(".")),
            "upper_category",
        ] = (
            added_data["category_code"].str.split(".").str[0]
        )
        return added_data

    def filter_purchase_date(self, data, purchase_col):
        filtered_df = data.loc[data[purchase_col] == "purchase"].copy()
        save_csv(filtered_df, "./data/purchase_data.csv")
        return filtered_df

    def run(self):
        data = self.add_upper_category_column()
        data = self.filter_purchase_date(data, "event_type")
        return "Completed"


if __name__ == "__main__":
    data = load_csv(
        "./data",
        "kaggle_ecommerce_behavior_data_2019_Nov_partial.csv",
        ["event_time"],
        "utf8",
    )
    params = load_json("./params/param_test.json")
    p = Preprocessor(data, params)
    # print(p.check_data_consistency())
    p.run()
