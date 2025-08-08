package com.cleanhdmi;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

public class CameraService extends Service {
    private static final String TAG = "CameraService";
    
    @Override
    public void onCreate() {
        super.onCreate();
        Log.d(TAG, "Service created");
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG, "Service started");
        return START_STICKY;
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "Service destroyed");
    }
}
