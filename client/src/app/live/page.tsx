import React from "react";
import dynamic from "next/dynamic";
import EmergencyPanel from "@/components/live/EmergencyPanel";
import EventPanel from "@/components/live/EventPanel";

const Map = dynamic(() => import("@/components/live/map/Map"), {
    loading: () => <p>Rendering Map...</p>,
    ssr: false,
});

const Page = () => {
    return (
        <div className="h-full max-h-[calc(100dvh-50px)]">
            <div className="h-full">
                <EventPanel />
                <div className="absolute right-80 top-24">
                    <EmergencyPanel />
                </div>
            </div>
            <Map />
        </div>
    );
};

export default Page;
