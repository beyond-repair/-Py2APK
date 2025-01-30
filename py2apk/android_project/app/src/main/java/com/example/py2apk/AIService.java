package com.example.py2apk;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

public class AIService extends Service {
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        new Thread(() -> {
            try {
                // Run AI task in the background
                String result = runPythonAITask();
                Log.d("AIService", "AI Task Result: " + result);
            } catch (Exception e) {
                Log.e("AIService", "AI Task Failed", e);
            }
        }).start();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private String runPythonAITask() {
        // Call Python code via Chaquopy
        return "AI Task Completed";
    }
}
