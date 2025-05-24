"use client";

import React, { useEffect, useRef } from "react";
import { CallProps } from "@/app/live/page";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

import { ScrollArea } from "../ui/scroll-area";

interface ChatInterfaceProps extends CallProps {}

const ChatInterface = ({ call }: ChatInterfaceProps) => {
    const ref = useRef<HTMLDivElement>(null);
    useEffect(() => {
        const scrollIntoViewInterval = () => {
            if (ref.current) {
                ref.current.scrollIntoView({
                    behavior: "smooth",
                    block: "end",
                });
            }
        };

        scrollIntoViewInterval();

        return () => scrollIntoViewInterval();
    }, [call]);

    return (
        <ScrollArea className="mx-auto flex h-[calc(100dvh-308px)] flex-col bg-gray-100">
            <div
                className="flex-1 space-y-4 overflow-y-auto p-4 pb-5"
                ref={ref}
            >
                {call?.transcript.map((message, index) => {
                    return (
                        <div
                            key={index}
                            className={cn(
                                "flex",
                                message.role === "user"
                                    ? "justify-end"
                                    : "justify-start",
                            )}
                        >
                            <div
                                className={cn(
                                    "flex items-end",
                                    message.role === "user"
                                        ? "flex-row-reverse"
                                        : "flex-row",
                                )}
                            >
                                <div
                                    className={cn(
                                        "mb-auto flex h-8 min-h-8 w-8 min-w-8 items-center justify-center rounded-full",
                                        message.role === "user"
                                            ? "hidden bg-blue-500"
                                            : "bg-gray-500",
                                    )}
                                >
                                    {message.role === "user" ? (
                                        null ?? <User size={20} color="white" />
                                    ) : (
                                        <Bot size={20} color="white" />
                                    )}
                                </div>
                                <div
                                    className={cn(
                                        "rounded-lg px-4 py-2",
                                        message.role === "user"
                                            ? "mr-2 max-w-[360px] bg-blue-500 text-white"
                                            : "ml-2 max-w-[250px] bg-white text-gray-800",
                                    )}
                                >
                                    {message.content}
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </ScrollArea>
    );
};

export default ChatInterface;
