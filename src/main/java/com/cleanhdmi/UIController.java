package com.cleanhdmi;

import android.content.Context;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.Button;
import android.widget.TextView;
import android.view.Gravity;
import android.graphics.Color;

/**
 * Controls UI overlay elements
 */
public class UIController {
    private Context context;
    private FrameLayout container;
    private LinearLayout uiPanel;
    private boolean isVisible = false;
    
    private Runnable onMenuPress;
    private Runnable onFnPress;
    
    public UIController(Context context, FrameLayout container) {
        this.context = context;
        this.container = container;
        createUI();
    }
    
    private void createUI() {
        uiPanel = new LinearLayout(context);
        uiPanel.setOrientation(LinearLayout.VERTICAL);
        uiPanel.setBackgroundColor(0x80000000); // Semi-transparent black
        uiPanel.setPadding(20, 20, 20, 20);
        
        // Add status text
        TextView statusText = new TextView(context);
        statusText.setText("Clean HDMI Mode");
        statusText.setTextColor(Color.WHITE);
        statusText.setTextSize(18);
        uiPanel.addView(statusText);
        
        // Add control buttons
        Button focusButton = new Button(context);
        focusButton.setText("Toggle Focus Lock");
        focusButton.setOnClickListener(v -> {
            if (onFnPress != null) onFnPress.run();
        });
        uiPanel.addView(focusButton);
        
        // Position UI panel
        FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.WRAP_CONTENT,
            FrameLayout.LayoutParams.WRAP_CONTENT
        );
        params.gravity = Gravity.TOP | Gravity.LEFT;
        container.addView(uiPanel, params);
        
        // Initially hidden
        hideUI();
    }
    
    public void showUI() {
        uiPanel.setVisibility(LinearLayout.VISIBLE);
        isVisible = true;
    }
    
    public void hideUI() {
        uiPanel.setVisibility(LinearLayout.GONE);
        isVisible = false;
    }
    
    public void setOnMenuPressListener(Runnable listener) {
        this.onMenuPress = listener;
    }
    
    public void setOnFnPressListener(Runnable listener) {
        this.onFnPress = listener;
    }
}
