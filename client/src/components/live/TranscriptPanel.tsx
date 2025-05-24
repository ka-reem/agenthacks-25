import { CallProps } from "@/app/live/page";
import { CheckCircle2Icon } from "lucide-react";

import { Separator } from "../ui/separator";
import ChatInterface from "./ChatInterface";
import EmotionCard from "./EmotionCard";

interface TranscriptPanelProps extends CallProps {}

const TranscriptPanel = ({ call }: TranscriptPanelProps) => {
    return (
        <div className="w-[500px] bg-white">
            <p className="px-2 py-[6px]">Live Transcript</p>
            <Separator />

            <div className="space-y-8 p-2">
                <div className="-mb-2 flex items-center space-x-1">
                    <CheckCircle2Icon className="text-green-600" size={24} />
                    <p className="text-md font-semibold text-green-600">
                        AI Operator Connected
                    </p>
                </div>

                <div className="space-y-2">
                    <div className="flex h-full space-x-2">
                        <EmotionCard
                            emotion="Distress"
                            percentage={85}
                            color="bg-blue-500"
                        />
                        <EmotionCard
                            emotion="Anger"
                            percentage={25}
                            color="bg-orange-500"
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <div>
                        <p className="text-xs font-medium uppercase leading-3 text-black text-opacity-50">
                            Call Transcript
                        </p>
                    </div>

                    <ChatInterface call={call} />
                </div>
            </div>
        </div>
    );
};

export default TranscriptPanel;
