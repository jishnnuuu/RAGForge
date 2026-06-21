from surya.inference import SuryaInferenceManager
from surya.layout import LayoutPredictor
from surya.recognition import RecognitionPredictor


class SuryaService:

    def __init__(self):

        self.manager = SuryaInferenceManager()

        self.layout_predictor = LayoutPredictor(
            self.manager
        )

        self.ocr_predictor = RecognitionPredictor(
            self.manager
        )