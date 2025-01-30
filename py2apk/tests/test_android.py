import unittest
from py2apk.utils.ai_processing import AIModel
import numpy as np

class TestAndroidIntegration(unittest.TestCase):
    def test_onnx_model_inference(self):
        """Test ONNX model inference."""
        model = AIModel("tests/models/gpt2.onnx")
        input_data = np.random.rand(1, 10).astype(np.float32)
        output = model.run_inference(input_data)
        self.assertIsNotNone(output, "Inference failed")

if __name__ == '__main__':
    unittest.main()
