import onnxruntime as ort
import numpy as np
import logging

logger = logging.getLogger(__name__)

class AIModel:
    """Handles ONNX model loading and inference."""
    
    def __init__(self, model_path: str):
        self.session = ort.InferenceSession(model_path)
        logger.info(f"Loaded ONNX model from {model_path}")

    def run_inference(self, input_data: np.ndarray) -> Optional[np.ndarray]:
        """Run inference on the ONNX model."""
        try:
            input_name = self.session.get_inputs()[0].name
            output_name = self.session.get_outputs()[0].name
            return self.session.run([output_name], {input_name: input_data})[0]
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            return None
