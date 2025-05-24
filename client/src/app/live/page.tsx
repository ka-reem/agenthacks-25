"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import EmergencyPanel from "@/components/live/EmergencyPanel";
import EventPanel from "@/components/live/EventPanel";
import Header from "@/components/live/Header";
import TranscriptPanel from "@/components/live/TranscriptPanel";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const Map = dynamic(() => import("@/components/live/map/Map"), {
    loading: () => <p>Rendering Map...</p>,
    ssr: false,
});

interface ServerMessage {
    event: "db_response";
    data: Call[];
}

export type Call = {
    emotions: {
        emotion: string;
        intensity: number;
    }[];
    id: string;
    location: string;
    name: string;
    phone: string;
    recommendation: string;
    severity: string;
    summary: string;
    time: string; // ISO Date String
    title: string;
    transcript: {
        role: "assistant" | "user";
        content: string;
    }[];
    type: string;
};

export interface CallProps {
    call: Call;
}

const wss = new WebSocket("wss://3a2ee56343fd.ngrok.app/ws?client_id=1234");

const Page = () => {
    const [connected, setConnected] = useState(false);
    const [data, setData] = useState<Call[]>([]);
    const [selectedIndex, setSelectedIndex] = useState<number | undefined>();

    const handleClick = () => {
        console.log("clicked");
        wss.send(
            JSON.stringify({
                event: "get_db",
            }),
        );
    };

    useEffect(() => {
        wss.onopen = () => {
            console.log("WebSocket connection established");
            setConnected(true);

            wss.onmessage = (event: MessageEvent) => {
                console.log("Received message");
                const message = JSON.parse(event.data) as ServerMessage;
                const data = message.data;

                console.log(data);

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

    return (
        <div className="h-full max-h-[calc(100dvh-50px)]">
            <Header connected={connected} />
            <Button onClick={handleClick}>click me!</Button>

            <div className="flex h-full justify-between">
                <EventPanel data={data} />
                {selectedIndex ? (
                    <div className="flex">
                        <EmergencyPanel />
                        <TranscriptPanel call={data[selectedIndex]} />
                    </div>
                ) : (
                    <div />
                )}
            </div>
            <Map />
        </div>
    );
};

export default Page;
