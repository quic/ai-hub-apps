// ---------------------------------------------------------------------
// Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
package com.quicinc.chatapp;

/**
 * ChatMessage: Holds information about each message within Chat
 */
public class ChatMessage {

    private String mMessage;
    private int mLength;
    public MessageSender mSender;
    private double msToFirstToken;
    private double msToLastToken;
    private boolean isFirstTokenTimeSet = false;

    public ChatMessage(String msg, MessageSender sender) {
        mMessage = msg;
        mSender = sender;
        mLength = msg.length();
    }

    /**
     * ChatMessage: Constructor for a message from the user
     * @param msg: the message
     * @param sender: the sender of the message
     * @param timeUntilFirstToken: the time it took to generate the first token
     */
    public ChatMessage(String msg, MessageSender sender, double timeUntilFirstToken) {
        mMessage = msg;
        mLength = msg.length();
        mSender = sender;
        msToFirstToken = timeUntilFirstToken;
        isFirstTokenTimeSet = timeUntilFirstToken > 0;
    }

    /**
     * isMessageFromUser: Check if the message is from the user
     *
     * @return true if the message is from the user, false otherwise
     */
    public boolean isMessageFromUser() {
        return mSender == MessageSender.USER;
    }

    /**
     * getMessage: Get the message
     *
     * @return the message
     */
    public String getMessage() {
        return mMessage;
    }

    /**
     * getLength: Get the length of the message
     *
     * @return the length of the message
     */
    public int getLength() {
        return mLength;
    }

    /**
     * setMessage: Set the message and update the length
     * @param message: the message to set
     */
    public void setMessage(String message) {
        mMessage = message;
        mLength = message.length();
    }

    /**
     * getMsToFirstToken: Get the time it took to generate the first token
     *
     * @return time in milliseconds
     */
    public double getMsToFirstToken() {
        return msToFirstToken;
    }

    /**
     * setMsToFirstToken: Set the time it took to generate the first token
     */
    public void setMsToFirstToken() {
        if (!isFirstTokenTimeSet) {
            msToFirstToken = System.currentTimeMillis();
            isFirstTokenTimeSet = true;
        }
    }

    /**
     * getMsToLastToken: Get the time it took to generate the last token
     *
     * @return time in milliseconds
     */ 
    public double getMsToLastToken() {
        return msToLastToken;
    }

    /**
     * setMsToLastToken: Set the time it took to generate the last token
     * @param origin: the time the message was sent
     */
    public void setMsToLastToken(long origin) {
        msToLastToken = System.currentTimeMillis() - origin;
    }

    /**
     * timeBetweenTokens: Get the time it took to generate the last token
     *
     * @return time in milliseconds
     */
    public double timeBetweenTokens() {
        if (!isFirstTokenTimeSet || msToLastToken == 0) {
            return 0;
        }
        return msToLastToken - msToFirstToken;
    }

    /**
     * getTimeToFirstTokenSeconds: Get the time it took to generate the first token
     *
     * @return time in seconds
     */
    public double getTimeToFirstTokenSeconds() {
        return msToFirstToken / 1000.0;
    }

    /**
     * Returns total generation time in seconds
     */
    public double getTotalTimeSeconds() {
        return timeBetweenTokens() / 1000.0;
    }

}
