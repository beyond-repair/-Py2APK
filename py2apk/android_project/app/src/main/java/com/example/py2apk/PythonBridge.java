package com.example.py2apk;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class PythonBridge {
    private static PythonBridge instance;
    private Python python;

    private PythonBridge() {
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(context));
        }
        python = Python.getInstance();
    }

    public static PythonBridge getInstance() {
        if (instance == null) {
            instance = new PythonBridge();
        }
        return instance;
    }

    public String runPythonScript(String scriptName, String input) {
        PyObject pyObject = python.getModule(scriptName);
        return pyObject.callAttr("process_input", input).toString();
    }
}
