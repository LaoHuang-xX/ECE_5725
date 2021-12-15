/*
    ECE 5725 final project
    RPi Robot Mover
    Fall 2021
    Authors: Xu Hai (xh357), Yaqun Niu (yn232)
*/

package com.example.ece_5725;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.graphics.Color;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import java.net.HttpURLConnection;


public class MainActivity extends AppCompatActivity implements SensorEventListener {

    private static final String TAG = "MainActivity";

    private SensorManager sensorManager;
    Sensor accelerometer;

    Server server;
    TextView infoip, msg;
    String x_axis;
    String y_axis;
    String z_axis;
    int i=1;
    int j=0;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Mode-switch button
        Button btn = (Button) this.findViewById(R.id.button1);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                // Increase i by 1 when we press the button every time
                i+=1;
                // Auto mode
                if(i == 2){
                    btn.setText("quit");
                    j=1;
                    // Change the color of the button to be red
                    btn.setBackgroundColor(Color.parseColor("#FF0000"));
                }
                else if(i == 3){
                    j=2;
                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    android.os.Process.killProcess(android.os.Process.myPid());
                }
                // Manual mode
                else{
                    j=0;
                }
            }
        });

        // Set the port and IP address
        WebView webView = (WebView) findViewById(R.id.webview);
        webView.loadUrl("http://10.49.12.138:8050/");

        // Accelerometer setting
        Log.d(TAG, "onCreate: Initializing Sensor Services");
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        sensorManager.registerListener(MainActivity.this, accelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        Log.d(TAG, "onCreate: Registered accelerometer listener");

        infoip = (TextView) findViewById(R.id.infoip);
        msg = (TextView) findViewById(R.id.msg);

        // Initialize the server and print the server IP and port address
        server = new Server(this);
        infoip.setText(server.getIpAddress() + ":" + server.getPort());
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i){

    }

    // Print the accelerometer information on the terminal
    @Override
    public void onSensorChanged(SensorEvent sensorEvent){
        Log.d(TAG, "OnSensorChanged: X: " + sensorEvent.values[0] + "Y: " + sensorEvent.values[1] + "Z: " + sensorEvent.values[2] + "//" + j);
        x_axis = String.valueOf(sensorEvent.values[0]);
        y_axis = String.valueOf(sensorEvent.values[1]);
        z_axis = String.valueOf(sensorEvent.values[2]);
    }

    // Destroy thr server
    @Override
    protected void onDestroy() {
        super.onDestroy();
        server.onDestroy();
    }
}