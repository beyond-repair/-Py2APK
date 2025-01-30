import json
import numpy as np
from py2apk.android_project.app.src.main.python.ai_model import AIModel

def process_input(input_json: str) -> str:
    """Process input from Android and return JSON output."""
    try:
        data = json.loads(input_json)
        tensor = np.array(data["input"], dtype=np.float32)
        model = AIModel("models/gpt2.onnx")
        output = model.run_inference(tensor)
        return json.dumps({"output": output.tolist()})
    except Exception as e:
        logger.error(f"Error processing input: {e}")
        return json.dumps({"error": str(e)})
