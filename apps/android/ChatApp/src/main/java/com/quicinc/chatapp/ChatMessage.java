// ---------------------------------------------------------------------
// Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
package com.quicinc.chatapp;

/**
 * ChatMessage: Holds information about each message within Chat
 */
public class ChatMessage {

    public String mMessage;
    public int mLength;
    public MessageSender mSender;

    public ChatMessage(String msg, MessageSender sender) {
        mMessage = msg;
        mLength = msg.length();
        mSender = sender;
    }

    public boolean isMessageFromUser() {
        return mSender == MessageSender.USER;
    }

    public String getMessage() {
        return mMessage;
    }
}
