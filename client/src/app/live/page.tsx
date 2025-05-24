import React from "react";
import dynamic from "next/dynamic";
import { Message } from "@/components/live/ChatInterface";
import EmergencyPanel from "@/components/live/EmergencyPanel";
import EventPanel from "@/components/live/EventPanel";
import TranscriptPanel from "@/components/live/TranscriptPanel";

const Map = dynamic(() => import("@/components/live/map/Map"), {
    loading: () => <p>Rendering Map...</p>,
    ssr: false,
});

const MESSAGES: Message[] = [
    {
        role: "user",
        content: "Hello, I need to report a power outage in my neighborhood.",
    },
    {
        role: "assistant",
        content: "Hello! I'm sorry to hear that. Can you provide your address?",
    },
    {
        role: "user",
        content: "It's 1234 Oak Street, Springfield.",
    },
    {
        role: "assistant",
        content: "Thank you. When did the outage start?",
    },
    {
        role: "user",
        content: "About 30 minutes ago, around 2:15 PM.",
    },
    {
        role: "assistant",
        content: "I've found a reported outage in your area. Crews are working on it.",
    },
    {
        role: "user",
        content: "Any estimate on when power will be restored?",
    },
    {
        role: "assistant",
        content: "We estimate power will be restored by 5:00 PM. For updates, call 555-123-4567.",
    },
    {
        role: "user",
        content: "Thanks for your help.",
    },
    {
        role: "assistant",
        content: "You're welcome. Stay safe, and contact us if you need further assistance.",
    },
];

const Page = () => {
    const messages = MESSAGES;

    return (
        <div className="h-full max-h-[calc(100dvh-50px)]">
            <div className="flex h-full">
                <EventPanel />
                <div className="flex flex-grow justify-end">
                    <EmergencyPanel />
                    <TranscriptPanel messages={messages} />
                </div>
            </div>
            <Map />
        </div>
    );
};

export default Page;
