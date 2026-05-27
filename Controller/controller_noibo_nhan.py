from Model.model_noibo import ModelNoiBo
from View.view_noibo_nhan import NoiBoNhanWidget

class ControllerNoiBoNhan:
    def __init__(self, model: ModelNoiBo, view: NoiBoNhanWidget, user_session):
        self.model = model
        self.view = view
        self.user_session = user_session
        self.view.da_xem_signal.connect(self.on_da_xem)

    def on_da_xem(self, noibo_id):
        # Có thể thêm hành động sau khi đánh dấu đã xem (ví dụ log)
        pass