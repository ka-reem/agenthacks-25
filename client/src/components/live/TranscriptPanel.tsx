import { useState } from "react";
import { CallProps } from "@/app/live/page";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
    ArrowLeftRightIcon,
    CheckCircle2Icon,
    HeadsetIcon,
    Loader2Icon,
} from "lucide-react";

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
    const [transferred, setTransferred] = useState(false);
    const [loading, setLoading] = useState(false);

    const emotions = call?.emotions?.sort((a, b) =>
        a.intensity < b.intensity ? 1 : -1,
    );

    if (!call) {
        return null;
    }

    const doTransfer = (id: string) => {
        handleTransfer(id);
        setLoading(true);

        setTimeout(() => {
            setTransferred(true);
            setLoading(false);
        }, 1000);
    };
    return (
        <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className={cn(
                "fixed right-0 top-[50px] min-h-[calc(100dvh-50px)] w-[400px] overflow-y-auto bg-white shadow-lg",
                transferred && "brightness-90",
            )}
        >
            <p className="px-2 py-[6px]">Live Transcript</p>
            <Separator />

            <div className="mb-3 space-y-4 p-2 pb-3">
                <div className="flex items-center space-x-1">
                    {transferred ? (
                        <HeadsetIcon className="text-blue-500" size={24} />
                    ) : (
                        <CheckCircle2Icon
                            className="text-green-500"
                            size={24}
                        />
                    )}
                    <p
                        className={cn(
                            "text-md font-semibold",
                            transferred ? "text-blue-500" : "text-green-500",
                        )}
                    >
                        {transferred
                            ? "Human Operator Connected"
                            : "AI Operator Connected"}
                    </p>
                </div>

                <div className="flex h-full space-x-2">
                    <EmotionCard
                        emotion={
                            emotions && emotions.length > 1
                                ? emotions[0].emotion
                                : "x"
                        }
                        percentage={
                            emotions && emotions.length > 1
                                ? emotions[0].intensity * 100
                                : 0
                        }
                        color="bg-purple-500"
                    />
                    <EmotionCard
                        emotion={
                            emotions && emotions.length > 1
                                ? emotions[1].emotion
                                : "x"
                        }
                        percentage={
                            emotions && emotions.length > 1
                                ? emotions[1].intensity * 100
                                : 0
                        }
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

                    {transferred ? (
                        <Button
                            variant={"outline"}
                            className="pointer-events-none w-full space-x-2 border-2 border-blue-500 text-black"
                        >
                            <HeadsetIcon /> <p>Transfered to Human Operator</p>
                        </Button>
                    ) : loading ? (
                        <Button className="w-full space-x-2 bg-green-500 text-white hover:bg-green-500/80">
                            <Loader2Icon className="animate-spin" />
                            <p>Transferring...</p>
                        </Button>
                    ) : (
                        <Button
                            onClick={() => doTransfer(call.id)}
                            className="w-full space-x-2 bg-green-500 text-white hover:bg-green-500/80"
                        >
                            <ArrowLeftRightIcon /> <p>Transfer</p>
                        </Button>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

export default TranscriptPanel;
