import pm4py
from utils import *


class ProcessModel:
    def __init__(self):
        pass

    def generate_process_model(self, data, case_id, activity_key, timestamp_key):
        event_log_xes = pm4py.format_dataframe(
            data,
            case_id=case_id,
            activity_key=activity_key,
            timestamp_key=timestamp_key,
        )
        process_tree = pm4py.discover_process_tree_inductive(event_log_xes)
        bpmn_model = pm4py.convert_to_bpmn(process_tree)
        # pm4py.view_bpmn(bpmn_model)
        self.save_model(bpmn_model)

    def save_model(self, model):
        pm4py.save_vis_bpmn(model, "./models/bpmn.png")
        pm4py.write_bpmn(model, "./models/bpmn.bpmn")
        print("Model Saved")


if __name__ == "__main__":
    data = load_csv(
        "./data",
        "purchase_session_events.csv",
        ["event_time"],
        "utf8",
    )
    process_model = ProcessModel()
    process_model.generate_process_model(
        data, "user_session", "event_type", "event_time"
    )
