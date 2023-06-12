from utils import *


class ParamsGenerator:
    def __init__(self):
        self.params = dict()

    def generate_preprocess_params(self):
        preprocess_params = dict()
        # 사용자 입력 받도록 수정 필요
        preprocess_params["consistency"] = {
            "user_session": ["user_id"],
            "category_id": ["category_code"],
            "product_id": ["category_id", "brand"],
        }
        self.params["preprocess"] = preprocess_params

    def save_params(self):
        filepath = "./params/param_test.json"
        save_json(self.params, filepath)

    def create_params(self):
        self.generate_preprocess_params()
        self.save_params()


if __name__ == "__main__":
    gen = ParamsGenerator()
    gen.create_params()
