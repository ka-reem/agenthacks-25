import { CheckCircle2Icon } from "lucide-react";

import { Progress } from "../ui/progress";
import { Separator } from "../ui/separator";
import ChatInterface, { MessagesProps } from "./ChatInterface";

interface TranscriptPanelProps extends MessagesProps {}

const TranscriptPanel = ({ messages }: TranscriptPanelProps) => {
    return (
        <div className="w-[400px] bg-white">
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
                    <div>
                        <p className="text-xs font-medium uppercase leading-3 text-black text-opacity-50">
                            Caller Emotions
                        </p>
                    </div>
                    <div className="w-[85%] space-y-2">
                        <div className="space-y-1">
                            <div className="flex-between">
                                <p className="text-base font-semibold">
                                    Distress
                                </p>
                                <p className="text-sm font-semibold text-black text-opacity-50">
                                    85%
                                </p>
                            </div>
                            <Progress value={85} className="h-2 rounded-none" />
                        </div>
                        <div className="space-y-1">
                            <div className="flex-between">
                                <p className="text-base font-semibold">Anger</p>
                                <p className="text-sm font-semibold text-black text-opacity-50">
                                    25%
                                </p>
                            </div>
                            <Progress value={25} className="h-2 rounded-none" />
                        </div>
                    </div>
                </div>

                <div className="space-y-2">
                    <div>
                        <p className="text-xs font-medium uppercase leading-3 text-black text-opacity-50">
                            Call Transcript
                        </p>
                    </div>

                    <ChatInterface messages={messages} />
                </div>
            </div>
        </div>
    );
};

export default TranscriptPanel;
