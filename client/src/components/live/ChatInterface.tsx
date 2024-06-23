"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

export interface Message {
    text: string;
    sender: "user" | "dispatcher";
}

export interface MessagesProps {
    messages: Message[];
}

interface ChatInterfaceProps extends MessagesProps {}

const ChatInterface = ({ messages }: ChatInterfaceProps) => {
    return (
        <div className="mx-auto flex h-[calc(100dvh-295px)] max-w-md flex-col bg-gray-100">
            <div className="flex-1 space-y-4 overflow-y-auto p-4">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={cn(
                            "flex",
                            message.sender === "user"
                                ? "justify-end"
                                : "justify-start",
                        )}
                    >
                        <div
                            className={cn(
                                "flex items-end",
                                message.sender === "user"
                                    ? "flex-row-reverse"
                                    : "flex-row",
                            )}
                        >
                            <div
                                className={cn(
                                    "mb-auto flex h-8 min-h-8 w-8 min-w-8 items-center justify-center rounded-full",
                                    message.sender === "user"
                                        ? "hidden bg-blue-500"
                                        : "bg-gray-500",
                                )}
                            >
                                {message.sender === "user" ? (
                                    null ?? <User size={20} color="white" />
                                ) : (
                                    <Bot size={20} color="white" />
                                )}
                            </div>
                            <div
                                className={cn(
                                    "rounded-lg px-4 py-2",
                                    message.sender === "user"
                                        ? "mr-2 max-w-[360px] bg-blue-500 text-white"
                                        : "ml-2 max-w-[250px] bg-white text-gray-800",
                                )}
                            >
                                {message.text}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatInterface;
