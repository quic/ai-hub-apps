// ---------------------------------------------------------------------
// Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
package com.quicinc.chatapp;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.Locale;

public class Message_RecyclerViewAdapter extends RecyclerView.Adapter<Message_RecyclerViewAdapter.MyViewHolder> {

    Context context;
    ArrayList<ChatMessage> messages = new ArrayList<ChatMessage>(1000);

    public Message_RecyclerViewAdapter(Context context, ArrayList<ChatMessage> messages) {
        this.context = context;
        this.messages = messages;
    }

    @NonNull
    @Override
    public Message_RecyclerViewAdapter.MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(context);
        View view = inflater.inflate(R.layout.chat_row, parent, false);

        return new Message_RecyclerViewAdapter.MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull Message_RecyclerViewAdapter.MyViewHolder holder, int position) {
        ChatMessage msg = messages.get(position);
        if (msg.isMessageFromUser()) {
            holder.mUserMessage.setText(msg.getMessage());
            holder.mLeftChatLayout.setVisibility(View.GONE);
            holder.mRightChatLayout.setVisibility(View.VISIBLE);
            holder.mTokenTimingView.setVisibility(View.GONE);
        } else {
            holder.mBotMessage.setText(msg.getMessage());
            holder.mLeftChatLayout.setVisibility(View.VISIBLE);
            holder.mRightChatLayout.setVisibility(View.GONE);
            
            // Show timing information for messages that have started generating
            if (msg.getTimeToFirstTokenSeconds() > 0) {
                holder.mTokenTimingView.setVisibility(View.VISIBLE);
                String timingText = formatTimingText(msg);
                holder.mTokenTimingView.setText(timingText);
                
                // Style the timing view differently if message is still generating
                if (msg.getTotalTimeSeconds() == 0) {
                    holder.mTokenTimingView.setAlpha(0.7f);
                } else {
                    holder.mTokenTimingView.setAlpha(1.0f);
                }
            } else {
                holder.mTokenTimingView.setVisibility(View.GONE);
            }
        }
    }

    private String formatTimingText(ChatMessage msg) {
        double firstTokenTime = msg.getTimeToFirstTokenSeconds();
        double totalTime = msg.getTotalTimeSeconds();
        double tokenRate = msg.getLength() / (totalTime > 0 ? totalTime : 1);

        return String.format(Locale.ENGLISH, "First token: %.1fs", firstTokenTime) +
                " • Total: " + String.format(Locale.ENGLISH, "%.1fs", totalTime) +
                " • " + String.format(Locale.ENGLISH, "%.0f chars/sec", tokenRate);
    }

    @Override
    public int getItemCount() {
        return messages.size();
    }

    public void addMessage(ChatMessage msg) {
        messages.add(msg);
    }

    /**
     * updateBotMessage: updates / inserts message on behalf of Bot
     *
     * @param bot_message message to update or insert
     * @param startTime the time the message was sent
     */
    public void updateBotMessage(String bot_message, long startTime) {
        boolean lastMessageFromBot = false;
        ChatMessage lastMessage;

        if (messages.size() > 1) {
            lastMessage = messages.get(messages.size() - 1);
            if (lastMessage.mSender == MessageSender.BOT) {
                lastMessageFromBot = true;
            }
        } else {
            addMessage(new ChatMessage(bot_message, MessageSender.BOT, System.currentTimeMillis() - startTime));
        }

        if (lastMessageFromBot) {
            ChatMessage msg = messages.get(messages.size() - 1);
            msg.setMessage(msg.getMessage() + bot_message);
            msg.setMsToLastToken(startTime);
        } else {
            addMessage(new ChatMessage(bot_message, MessageSender.BOT, System.currentTimeMillis() - startTime));
        }
    }

    public static class MyViewHolder extends RecyclerView.ViewHolder {

        TextView mUserMessage;
        TextView mBotMessage;
        LinearLayout mLeftChatLayout;
        LinearLayout mRightChatLayout;
        TextView mTokenTimingView;

        public MyViewHolder(@NonNull View itemView) {
            super(itemView);

            mBotMessage = itemView.findViewById(R.id.bot_message);
            mUserMessage = itemView.findViewById(R.id.user_message);
            mLeftChatLayout = itemView.findViewById(R.id.left_chat_layout);
            mRightChatLayout = itemView.findViewById(R.id.right_chat_layout);
            mTokenTimingView = itemView.findViewById(R.id.token_timing_view);
        }
    }
}
