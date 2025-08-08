package com.cleanhdmi;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.util.Log;

/**
 * Main activity for Clean HDMI output
 */
public class MainActivity extends Activity {
    private static final String TAG = "CleanHDMI";
    
    private LiveViewManager liveViewManager;
    private CameraController cameraController;
    private UIController uiController;
    private boolean isUIVisible = false;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "Starting Clean HDMI application");
        
        // Setup fullscreen mode
        setupFullscreen();
        
        // Initialize components
        initializeComponents();
        
        // Start clean live view
        startCleanView();
    }
    
    private void setupFullscreen() {
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        
        // Hide system UI
        View decorView = getWindow().getDecorView();
        int uiOptions = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                      | View.SYSTEM_UI_FLAG_FULLSCREEN
                      | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY;
        decorView.setSystemUiVisibility(uiOptions);
    }
    
    private void initializeComponents() {
        // Create main layout
        FrameLayout layout = new FrameLayout(this);
        layout.setBackgroundColor(0xFF000000); // Black background
        setContentView(layout);
        
        // Initialize managers
        liveViewManager = new LiveViewManager(this, layout);
        cameraController = new CameraController(this);
        uiController = new UIController(this, layout);
        
        // Setup control callbacks
        setupControls();
    }
    
    private void startCleanView() {
        try {
            // Start live view without UI
            liveViewManager.startCleanMode();
            
            // Apply default camera settings
            cameraController.applyDefaultSettings();
            
            Log.d(TAG, "Clean view started successfully");
        } catch (Exception e) {
            Log.e(TAG, "Failed to start clean view: " + e.getMessage());
        }
    }
    
    private void setupControls() {
        // Set up button handlers
        uiController.setOnMenuPressListener(() -> {
            toggleUI();
        });
        
        uiController.setOnFnPressListener(() -> {
            cameraController.toggleFocusLock();
        });
    }
    
    private void toggleUI() {
        if (isUIVisible) {
            uiController.hideUI();
        } else {
            uiController.showUI();
        }
        isUIVisible = !isUIVisible;
    }
    
    @Override
    protected void onResume() {
        super.onResume();
        liveViewManager.resume();
    }
    
    @Override
    protected void onPause() {
        super.onPause();
        liveViewManager.pause();
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        liveViewManager.stop();
        cameraController.release();
    }
}
