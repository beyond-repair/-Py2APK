package com.example.py2apk;

import ai.onnxruntime.OrtEnvironment;
import ai.onnxruntime.OrtSession;
import android.content.Context;
import android.util.Log;
import java.io.InputStream;
import java.nio.ByteBuffer;
import android.content.res.AssetManager;

public class AIModelRunner {
    private static OrtEnvironment env;
    private static OrtSession session;

    public static void loadModel(Context context, String modelFile) {
        try {
            env = OrtEnvironment.getEnvironment();
            AssetManager assetManager = context.getAssets();
            InputStream inputStream = assetManager.open(modelFile);
            byte[] modelBytes = new byte[inputStream.available()];
            inputStream.read(modelBytes);
            inputStream.close();

            session = env.createSession(modelBytes);
            Log.d("AIModelRunner", "ONNX Model Loaded Successfully");
        } catch (Exception e) {
            Log.e("AIModelRunner", "Failed to load ONNX model", e);
        }
    }

    public static float[] runInference(float[] input) {
        try {
            return session.run(input);
        } catch (Exception e) {
            Log.e("AIModelRunner", "Inference failed", e);
            return null;
        }
    }
}
