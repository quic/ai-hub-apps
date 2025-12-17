// ---------------------------------------------------------------------
// Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
package com.quicinc.chatapp;

import android.os.Bundle;
import android.system.Os;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.SimpleItemAnimator;

import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class Conversation extends AppCompatActivity {

    ArrayList<ChatMessage> messages = new ArrayList<ChatMessage>(1000);

    private static final String cWelcomeMessage = "Hi! How can I help you?";
    public static final String cConversationActivityKeyHtpConfig = "htp_config_path";
    public static final String cConversationActivityKeyModelName = "model_dir_name";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.chat);
        RecyclerView recyclerView = findViewById(R.id.chat_recycler_view);
        Message_RecyclerViewAdapter adapter = new Message_RecyclerViewAdapter(this, messages);
        recyclerView.setAdapter(adapter);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        // Disable change animations
        RecyclerView.ItemAnimator animator = recyclerView.getItemAnimator();
        if (animator instanceof SimpleItemAnimator){
            ((SimpleItemAnimator) animator).setSupportsChangeAnimations(false);
        }

        ImageButton sendUserMsgButton = (ImageButton) findViewById(R.id.send_button);
        TextView userMsg = (TextView) findViewById(R.id.user_input);

        try {
            // Make QNN libraries discoverable
            String nativeLibPath = getApplicationContext().getApplicationInfo().nativeLibraryDir;
            Os.setenv("ADSP_LIBRARY_PATH", nativeLibPath, true);
            Os.setenv("LD_LIBRARY_PATH", nativeLibPath, true);

            // Get information from MainActivity regarding
            //  - Model to run
            //  - HTP config to use
            Bundle bundle = getIntent().getExtras();
            if (bundle == null) {
                Log.e("ChatApp", "Error getting additional info from bundle.");
                Toast.makeText(this, "Unexpected error observed. Exiting app.", Toast.LENGTH_LONG).show();
                finish();
            }

            String htpExtensionsDir = bundle.getString(cConversationActivityKeyHtpConfig);
            String modelName = bundle.getString(cConversationActivityKeyModelName);
            String externalCacheDir = this.getExternalCacheDir().getAbsolutePath().toString();
            String modelDir = Paths.get(externalCacheDir, "models", modelName).toString();

            // Load Model
            GenieWrapper genieWrapper = new GenieWrapper(modelDir, htpExtensionsDir);
            Log.i("ChatApp", modelName + " Loaded.");

            messages.add(new ChatMessage(cWelcomeMessage, MessageSender.BOT));

            // Get response from Bot once user message is sent
            sendUserMsgButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {

                    if (userMsg.getTextSize() != 0) {
                        String userInputMsg = userMsg.getText().toString();
                        // Reset user message box
                        userMsg.setText("");

                        // Insert user message in the conversation
                        int start = adapter.getItemCount();
                        adapter.addMessage(new ChatMessage(userInputMsg, MessageSender.USER));
                        adapter.addMessage(new ChatMessage("", MessageSender.BOT));
                        adapter.notifyItemRangeInserted(start, 2);

                        int botResponseMsgIndex = adapter.getItemCount() - 1;
                        recyclerView.smoothScrollToPosition(botResponseMsgIndex);

                        ExecutorService service = Executors.newSingleThreadExecutor();
                        service.execute(new Runnable() {
                            @Override
                            public void run() {
                                genieWrapper.getResponseForPrompt(userInputMsg, new StringCallback() {
                                    @Override
                                    public void onNewString(String response) {
                                        runOnUiThread(() -> {
                                            // Update the last item in the adapter
                                            adapter.updateBotMessage(response);
                                            adapter.notifyItemChanged(botResponseMsgIndex);

                                            RecyclerView.LayoutManager lm = recyclerView.getLayoutManager();
                                            if (lm instanceof LinearLayoutManager) {
                                                LinearLayoutManager layoutManager = (LinearLayoutManager) lm;
                                                int lastVisible = layoutManager.findLastVisibleItemPosition();

                                                if (lastVisible == messages.size() - 1) {
                                                    recyclerView.scrollToPosition(messages.size() - 1);
                                                }
                                            }
                                        });
                                    }
                                });
                            }
                        });

                    }
                }
            });

        } catch (Exception e) {
            Log.e("ChatApp", "Error during conversation with Chatbot: " + e.toString());
            Toast.makeText(this, "Unexpected error observed. Exiting app.", Toast.LENGTH_SHORT).show();
            finish();
        }
    }
}
