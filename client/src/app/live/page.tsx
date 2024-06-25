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
        role: "assistant" | "user" | "agent";
        content: string;
    }[];
    type: string;
};

export interface CallProps {
    call?: Call;
    selectedId: string | undefined;
}

const wss = new WebSocket(
    "wss://planned-halimeda-wecracked2-c8137aa7.koyeb.app/ws?client_id=1234",
);

const MESSAGES: Record<string, Call> = {
    // "1234": {
    //     emotions: [
    //         { emotion: "Concern", intensity: 0.7 },
    //         { emotion: "Frustration", intensity: 0.3 },
    //     ],
    //     id: "1234",
    //     location_name: "1234 Oak Street, Springfield",
    //     location_coords: {
    //         lat: 37.867989,
    //         lng: -122.271507,
    //     },
    //     name: "John Doe",
    //     phone: "555-123-4567",
    //     recommendation: "Monitor situation and provide updates",
    //     severity: "MODERATE",
    //     summary:
    //         "Power outage reported in Springfield area. Estimated restoration by 5:00 PM.",
    //     time: "2023-07-15T14:15:00Z",
    //     title: "Power Outage Report",
    //     transcript: [
    //         {
    //             role: "user",
    //             content:
    //                 "Hello, I need to report a power outage in my neighborhood.",
    //         },
    //         {
    //             role: "assistant",
    //             content:
    //                 "Hello! I'm sorry to hear that. Can you provide your address?",
    //         },
    //         {
    //             role: "user",
    //             content: "It's 1234 Oak Street, Springfield.",
    //         },
    //         {
    //             role: "assistant",
    //             content: "Thank you. When did the outage start?",
    //         },
    //         {
    //             role: "user",
    //             content: "About 30 minutes ago, around 2:15 PM.",
    //         },
    //         {
    //             role: "assistant",
    //             content:
    //                 "I've found a reported outage in your area. Crews are working on it.",
    //         },
    //         {
    //             role: "user",
    //             content: "Any estimate on when power will be restored?",
    //         },
    //         {
    //             role: "assistant",
    //             content:
    //                 "We estimate power will be restored by 5:00 PM. For updates, call 555-123-4567.",
    //         },
    //         {
    //             role: "user",
    //             content: "Thanks for your help.",
    //         },
    //         {
    //             role: "assistant",
    //             content:
    //                 "You're welcome. Stay safe, and contact us if you need further assistance.",
    //         },
    //     ],
    //     type: "Power Outage",
    // },
    CA22ccebaacd73dcefa23f9b41a9bce0b3: {
        id: "CA22ccebaacd73dcefa23f9b41a9bce0b3",
        time: "2024-06-23T22:46:37.335108",
        transcript: [
            {
                role: "agent",
                content: "9-1-1, what's your emergency?",
            },
            {
                role: "user",
                content:
                    "Um, there's current earthquakes. Um, send help, please.",
            },
            {
                role: "agent",
                content: "What's your location?",
            },
            {
                role: "user",
                content:
                    "I am currently at the Golden Gate Bridge, there's a lot of people injured. Please send help.",
            },
            {
                role: "agent",
                content: "Is there immediate danger where you are?",
            },
            {
                role: "agent",
                content: "Anything changed?",
            },
            {
                role: "user",
                content:
                    "Um, I'm currently at the Golden Gate Bridge. And we need help. A lot of people here that are injured.",
            },
            {
                role: "agent",
                content: "Is there immediate danger where you are?",
            },
        ],
        emotions: [
            {
                emotion: "Fear",
                intensity: 0.3548029899331076,
            },
            {
                emotion: "Confusion",
                intensity: 0.2665824613400868,
            },
            {
                emotion: "Anxiety",
                intensity: 0.21041041083766945,
            },
        ],
        recommendation:
            "Send emergency services immediately for medical assistance and disaster relief.",
        severity: "CRITICAL",
        type: "Police",
        name: "",
        phone: "",
        title: "Earthquake Emergency at Golden Gate Bridge",
        summary:
            "Caller reports current earthquakes and requests immediate assistance. Location: Golden Gate Bridge with many people injured.",
        location_name: "Golden Gate Bridge, San Francisco, CA",
        location_coords: {
            lat: 37.8199109,
            lng: -122.4785598,
        },
        street_view:
            "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",
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
    const [resolvedIds, setResolvedIds] = useState<string[]>([]);

    const [center, setCenter] = useState<{ lat: number; lng: number }>({
        lat: 37.867989,
        lng: -122.271507,
    });

    const handleSelect = (id: string) => {
        setSelectedId(id === selectedId ? undefined : id);
    };

    const handleResolve = (id: string) => {
        setResolvedIds((prev) => {
            const newResolvedIds = [...prev, id];

            const newData = { ...data };
            Object.keys(newData).forEach((key) => {
                if (newResolvedIds.includes(newData[key].id)) {
                    newData[key].severity = "RESOLVED";
                }
            });

            setData(newData);
            return newResolvedIds;
        });
    };

    const handleTransfer = (id: string) => {
        console.log("transfer: ", id);

        wss.send(
            JSON.stringify({
                event: "transfer",
                id: id,
            }),
        );
    };

    useEffect(() => {
        if (!selectedId) return;

        if (!data[selectedId]?.location_coords) return;

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

                    Object.keys(data).forEach((key) => {
                        if (resolvedIds?.includes(data[key].id)) {
                            data[key].severity = "RESOLVED";
                        }
                    });

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
                            call={selectedId ? data[selectedId] : emptyCall}
                            handleResolve={handleResolve}
                        />
                        <TranscriptPanel
                            call={selectedId ? data[selectedId] : emptyCall}
                            selectedId={selectedId || undefined}
                            handleTransfer={handleTransfer}
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
