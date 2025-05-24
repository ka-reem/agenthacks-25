import { useEffect, useState } from "react";
import { CallProps } from "@/app/live/page";
import { CheckCircle2Icon, HeadsetIcon, PhoneIcon } from "lucide-react";

import { Button } from "../ui/button";
import { Separator } from "../ui/separator";
import ChatInterface from "./ChatInterface";
import EmotionCard from "./EmotionCard";

interface TranscriptPanelProps extends CallProps {
    handleTransfer: (id: string) => void;
}

const TranscriptPanel = ({
    call,
    selectedId,
    handleTransfer,
}: TranscriptPanelProps) => {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        // console.warn("X", call, selectedId);
        if (call && selectedId) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    }, [call, selectedId]);

    const emotions = call?.emotions?.sort((a, b) =>
        a.intensity < b.intensity ? 1 : -1,
    );

    if (!call) {
        return null;
    }

    return (
        <div className={`w-[400px] bg-white`}>
            <p className="px-2 py-[6px]">Live Transcript</p>
            <Separator />

            <div className="mb-3 space-y-4 p-2 pb-3">
                <div className="flex items-center space-x-1">
                    <CheckCircle2Icon className="text-green-600" size={24} />
                    <p className="text-md font-semibold text-green-600">
                        AI Operator Connected
                    </p>
                </div>

                <div className="flex h-full space-x-2">
                    <EmotionCard
                        emotion={emotions ? emotions[0].emotion : "x"}
                        percentage={emotions ? emotions[0].intensity * 100 : 0}
                        color="bg-purple-500"
                    />
                    <EmotionCard
                        emotion={emotions ? emotions[1].emotion : "x"}
                        percentage={emotions ? emotions[1].intensity * 100 : 0}
                        color="bg-purple-500"
                    />
                </div>

                <div className="mb-3 space-y-2">
                    <div>
                        <p className="text-xs font-medium uppercase leading-3 text-black text-opacity-50">
                            Call Transcript
                        </p>
                    </div>

                    <ChatInterface call={call} selectedId={selectedId} />

                    <Button
                        onClick={() => handleTransfer(call.id)}
                        className="w-full space-x-2 bg-green-500 hover:bg-green-500/80"
                    >
                        <HeadsetIcon /> <p>Transfer</p>
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default TranscriptPanel;
