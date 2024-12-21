package com.callguard;

import android.media.MediaRecorder;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.Callback;  // Import Callback

import java.io.IOException;
import android.util.Log;

public class CallRecordingModule extends ReactContextBaseJavaModule {
    private MediaRecorder recorder;
    private boolean isRecording = false;

    public CallRecordingModule(ReactApplicationContext reactContext) {
        super(reactContext);
    }

    @Override
    public String getName() {
        return "CallRecording";
    }

    @ReactMethod
    public void startRecording(String filePath, Callback successCallback, Callback errorCallback) {
        Log.d("CallRecordingModule", "startRecording called with filePath: " + filePath);
        try {
            recorder = new MediaRecorder();
            Log.d("CallRecordingModule", "Initializing MediaRecorder...");
            
            recorder.setAudioSource(MediaRecorder.AudioSource.VOICE_COMMUNICATION);
            recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
            recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);
            recorder.setOutputFile(filePath);

            Log.d("CallRecordingModule", "Preparing MediaRecorder...");
            recorder.prepare();

            Log.d("CallRecordingModule", "Starting recording...");
            recorder.start();
            isRecording = true;

            Log.d("CallRecordingModule", "Recording started successfully.");
            
            // Call successCallback if everything works
            successCallback.invoke("Recording started successfully.");
        } catch (IOException e) {
            Log.e("CallRecordingModule", "Error starting recording: " + e.getMessage(), e);
            // Call errorCallback in case of an error
            errorCallback.invoke("Error starting recording: " + e.getMessage());
        }
    }

    @ReactMethod
    public void stopRecording(Callback successCallback, Callback errorCallback) {
        if (isRecording && recorder != null) {
            try {
                recorder.stop();
                recorder.release();
                recorder = null;
                isRecording = false;
                
                Log.d("CallRecordingModule", "Recording stopped successfully.");
                
                // Call successCallback
                successCallback.invoke("Recording stopped successfully.");
            } catch (IllegalStateException e) {
                Log.e("CallRecordingModule", "Error stopping recording: " + e.getMessage(), e);
                // Call errorCallback in case of an error
                errorCallback.invoke("Error stopping recording: " + e.getMessage());
            }
        } else {
            // If recorder is null or not recording, call errorCallback
            errorCallback.invoke("No recording to stop.");
        }
    }
}
