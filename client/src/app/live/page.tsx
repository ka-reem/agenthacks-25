"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import DetailsPanel from "@/components/live/DetailsPanel";
import EventPanel from "@/components/live/EventPanel";
import Header from "@/components/live/Header";
import TranscriptPanel from "@/components/live/TranscriptPanel";

const Map = dynamic(() => import("@/components/live/map/Map"), {
    loading: () => <p>Rendering Map...</p>,
    ssr: false,
});

interface ServerMessage {
    event: "db_response";
    data: Record<string, Call>;
}

export type Call = {
    emotions?: {
        emotion: string;
        intensity: number;
    }[];
    id: string;
    location_name: string;
    location_coords?: {
        lat: number;
        lng: number;
    };
    street_view?: string; // base 64
    name: string;
    phone: string;
    recommendation: string;
    severity?: "CRITICAL" | "MODERATE" | "RESOLVED";
    summary: string;
    time: string; // ISO Date String
    title?: string;
    transcript: {
        role: "assistant" | "user";
        content: string;
    }[];
    type: string;
};

export interface CallProps {
    call?: Call;
    selectedId: string | undefined;
}

const wss = new WebSocket("wss://3a2ee56343fd.ngrok.app/ws?client_id=1234");

const MESSAGES: Record<string, Call> = {
    "1234": {
        emotions: [
            { emotion: "Concern", intensity: 0.7 },
            { emotion: "Frustration", intensity: 0.3 },
        ],
        id: "1234",
        location_name: "1234 Oak Street, Springfield",
        location_coords: {
            lat: 37.867989,
            lng: -122.271507,
        },
        name: "John Doe",
        phone: "555-123-4567",
        recommendation: "Monitor situation and provide updates",
        severity: "MODERATE",
        summary:
            "Power outage reported in Springfield area. Estimated restoration by 5:00 PM.",
        time: "2023-07-15T14:15:00Z",
        title: "Power Outage Report",
        transcript: [
            {
                role: "user",
                content:
                    "Hello, I need to report a power outage in my neighborhood.",
            },
            {
                role: "assistant",
                content:
                    "Hello! I'm sorry to hear that. Can you provide your address?",
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
                content:
                    "I've found a reported outage in your area. Crews are working on it.",
            },
            {
                role: "user",
                content: "Any estimate on when power will be restored?",
            },
            {
                role: "assistant",
                content:
                    "We estimate power will be restored by 5:00 PM. For updates, call 555-123-4567.",
            },
            {
                role: "user",
                content: "Thanks for your help.",
            },
            {
                role: "assistant",
                content:
                    "You're welcome. Stay safe, and contact us if you need further assistance.",
            },
        ],
        type: "Power Outage",
    },
};

const emptyCall: Call = {
    emotions: [],
    id: "",
    location_name: "",
    location_coords: {
        lat: 0,
        lng: 0,
    },
    street_view: "", // base 64
    name: "",
    phone: "",
    recommendation: "",
    severity: "RESOLVED",
    summary: "",
    time: "",
    title: "",
    transcript: [],
    type: "",
};

const Page = () => {
    const [connected, setConnected] = useState(false);
    const [data, setData] = useState<Record<string, Call>>(MESSAGES);
    const [selectedId, setSelectedId] = useState<string | undefined>();

    const [center, setCenter] = useState<{ lat: number; lng: number }>({
        lat: 37.867989,
        lng: -122.271507,
    });

    const handleSelect = (id: string) => {
        setSelectedId(id === selectedId ? undefined : id);
    };

    useEffect(() => {
        if (!selectedId) return;

        if (!data[selectedId].location_coords) return;

        setCenter(
            data[selectedId].location_coords as { lat: number; lng: number }, // TS being lame, so type-cast
        );
    }, [selectedId, data]);

    useEffect(() => {
        wss.onopen = () => {
            console.log("WebSocket connection established");
            setConnected(true);

            wss.send(
                JSON.stringify({
                    event: "get_db",
                }),
            );

            wss.onmessage = (event: MessageEvent) => {
                console.log("Received message");
                const message = JSON.parse(event.data) as ServerMessage;
                console.log("message:", message);
                const data = message.data;
                console.log("data:", data);

                if (data) {
                    console.log("Got data");
                    setData(data);
                } else {
                    console.warn("Received unknown message");
                }
            };

            wss.onclose = () => {
                console.log("Closing websocket");
                setConnected(false);
            };
        };
    }, []);

    console.log(selectedId);

    return (
        <div className="h-full max-h-[calc(100dvh-50px)]">
            <Header connected={connected} />

            <div className="relative flex h-full justify-between">
                <EventPanel
                    data={data}
                    selectedId={selectedId || undefined}
                    handleSelect={handleSelect}
                />

                {selectedId && data ? (
                    <div className="absolute right-0 z-50 flex">
                        <DetailsPanel
                            selectedId={selectedId || undefined}
                            call={selectedId ? data[selectedId] : emptyCall}
                        />
                        <TranscriptPanel
                            call={selectedId ? data[selectedId] : emptyCall}
                            selectedId={selectedId || undefined}
                        />
                    </div>
                ) : null}

                <Map
                    center={center}
                    pins={
                        // {
                        //     coordinates: [37.867989, -122.271507],
                        //     popupHtml: "<b>Richard Davis</b><br>ID: #272428",
                        // },
                        // {
                        //     coordinates: [33.634023, -117.851286],
                        //     popupHtml: "<b>Sophia Jones</b><br>ID: #121445",
                        // },
                        // {
                        //     coordinates: [33.634917, -117.862744],
                        //     popupHtml: "<b>Adam Smith</b><br>ID: #920232",
                        // },
                        Object.entries(data)
                            .filter(
                                ([_, call]) =>
                                    call.location_coords && call.location_name,
                            )
                            .map(([_, call]) => {
                                return {
                                    coordinates: [
                                        call.location_coords?.lat as number, // type-cast cuz TS trolling
                                        call.location_coords?.lng as number, // type-cast cuz TS trolling
                                    ],
                                    popupHtml: `<b>${call.title}</b><br>Location: ${call.location_name}`,
                                };
                            })
                    }
                />
            </div>
        </div>
    );
};

export default Page;
