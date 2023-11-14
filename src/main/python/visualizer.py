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
        # 차트 제목 추가, 범례 제거
        fig.update_layout(showlegend=False, title_text=title, width=1200, height=600)
        # x 축 제목 추가
        fig.update_xaxes(title_text=x[1])
        # y 축 제목 추가
        fig.update_yaxes(title_text=first_y[1], secondary_y=False)
        fig.update_yaxes(title_text=second_y[1], secondary_y=True)

        return fig

    def generate_plots(self, x_list):
        for x in x_list:
            plot_data = (
                data.groupby(x)
                .agg({"event_type": "count", "price": ["min", "median", "mean", "max"]})
                .reset_index()
            )
            plot_data.columns = [x, "count", "min", "median", "mean", "max"]
            plot_data = plot_data.sort_values("count", ascending=False)
            title_data = {
                "title": f"카테고리별 월간 구매수량-평균금액_{x}",
                "x": [x, "카테고리명"],
                "y": {"first": ["count", "구매수량(건)"], "second": ["mean", "평균금액($)"]},
            }
            fig = self.draw_bar_line_multiplots(plot_data, title_data)
            fig.write_image(f"./plots/{title_data['title']}.png")
            # fig.show()


if __name__ == "__main__":
    data = load_csv(
        "./data",
        "purchase_data.csv",
        ["event_time"],
        "utf8",
    )
    visualizer = Visualizer()
    visualizer.generate_plots(["upper_category", "category_code"])
