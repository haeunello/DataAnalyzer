import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import *


class Visualizer:
    def __init__(self):
        pass

    def draw_bar_line_multiplots(self, data, settings):
        # setting 예시
        # {"title": "차트 제목",
        # "x" : ["x_col", "x"],
        # "y" : { "first":["f_col", "첫번째 y"], "second": ["s_col", "두번째 y"]})}

        title = settings["title"]
        x = settings["x"]
        first_y = settings["y"]["first"]
        second_y = settings["y"]["second"]

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 그래프 추가
        fig.add_trace(go.Bar(x=data[x[0]], y=data[first_y[0]]), secondary_y=False)
        fig.add_trace(go.Scatter(x=data[x[0]], y=data[second_y[0]]), secondary_y=True)

        # 차트 제목 추가
        fig.update_layout(title_text=title)
        # x 축 제목 추가
        fig.update_xaxes(title_text=x[1])
        # y 축 제목 추가
        fig.update_yaxes(title_text=first_y[1], secondary_y=False)
        fig.update_yaxes(title_text=second_y[1], secondary_y=True)

        return fig


if __name__ == "__main__":
    data = load_csv(
        "./data",
        "purchase_data.csv",
        ["event_time"],
        "utf8",
    )
    resp = (
        data.groupby("category_code")
        .agg({"event_type": "count", "price": ["min", "median", "mean", "max"]})
        .reset_index()
    )
    resp.columns = ["category_code", "cnt", "min", "median", "mean", "max"]
    resp = resp.sort_values("cnt", ascending=False)
    resp

    visualizer = Visualizer()
    fig = visualizer.draw_bar_line_multiplots(
        resp,
        {
            "title": "카테고리별 월간 구매수량-평균금액",
            "x": ["category_code", "cnt"],
            "y": {"first": ["cnt", "구매수량(건)"], "second": ["mean", "평균금액($)"]},
        },
    )
    fig.show()
