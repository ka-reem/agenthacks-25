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
        sender: "user",
        text: "Hello, I need to report a power outage in my neighborhood.",
    },
    {
        sender: "dispatcher",
        text: "Hello! I'm sorry to hear that. Can you provide your address?",
    },
    {
        sender: "user",
        text: "It's 1234 Oak Street, Springfield.",
    },
    {
        sender: "dispatcher",
        text: "Thank you. When did the outage start?",
    },
    {
        sender: "user",
        text: "About 30 minutes ago, around 2:15 PM.",
    },
    {
        sender: "dispatcher",
        text: "I've found a reported outage in your area. Crews are working on it.",
    },
    {
        sender: "user",
        text: "Any estimate on when power will be restored?",
    },
    {
        sender: "dispatcher",
        text: "We estimate power will be restored by 5:00 PM. For updates, call 555-123-4567.",
    },
    {
        sender: "user",
        text: "Thanks for your help.",
    },
    {
        sender: "dispatcher",
        text: "You're welcome. Stay safe, and contact us if you need further assistance.",
    },
];

const Page = () => {
    const messages = MESSAGES;

    return (
        <div className="h-full max-h-[calc(100dvh-50px)]">
            <div className="flex h-full justify-between">
                <EventPanel />
                {/* <div className="absolute right-80 top-24">
                    <EmergencyPanel />
                </div> */}
                <TranscriptPanel messages={messages} />
            </div>
            <Map />
        </div>
    );
};

export default Page;
