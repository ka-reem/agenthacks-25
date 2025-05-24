import { useEffect, useState } from "react";
import { Call } from "@/app/live/page";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useToast } from "@/components/ui/use-toast";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import {
    Ambulance,
    CircleEllipsisIcon,
    FireExtinguisher,
    Siren,
} from "lucide-react";

import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Card, CardContent, CardFooter } from "../ui/card";
import { Separator } from "../ui/separator";

const EmergencyInfoItem = ({
    label,
    value,
    side,
}: {
    label: string;
    value: string | React.ReactNode;
    side: "left" | "right";
}) => (
    <div
        className={cn(
            "line-clamp-3 space-y-1 px-3 pt-2",
            side === "left" ? "border-l" : "border-r",
        )}
    >
        <p className="text-sm font-medium leading-3 text-black text-opacity-50">
            {label}
        </p>
        {typeof value === "string" ? (
            <p className="text-lg font-semibold leading-tight">{value}</p>
        ) : (
            value
        )}
    </div>
);

interface DetailsPanelProps {
    call: Call | undefined;
    handleResolve: (id: string) => void;
}

const DetailsPanel = ({ call, handleResolve }: DetailsPanelProps) => {
    const emergency = {
        title: "House Fire in Lincoln Ave.",
        status: "CRITICAL",
        distance: "22 miles",
        type: "Fire",
        time: "12:34 AM",
        location: "Lincoln Ave.",
        summary:
            "Qui consectetur labore voluptate ea voluptate commodo nostrud sint labore consectetur qui nulla reprehenderit ad. Ut mollit nisi officia laboris exercitation cillum sit non eiusmod consequat. Non proident proident ad Lorem. Qui ea tempor labore deserunt dolor ad proident sit id nisi proident dolore. Nostrud commodo minim fugiat pariatur minim irure labore aute. Adipisicing mollit consequat ut id excepteur labore laboris. In laborum nisi aute duis pariatur eu.",
    };

    const { toast } = useToast();
    const [clicked, setClicked] = useState<number>(1);

    if (!call) {
        return null;
    }

    return (
        <motion.div
            initial={{ x: "100%", opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: "100%", opacity: 1 }}
            transition={{ duration: 0.3, ease: "easeOut", delay: 0.2 }}
            className="fixed right-[400px]"
        >
            <Card className="h-fit w-[400px] rounded-none border-0 border-r border-gray-300">
                <p className="px-2 py-[6px]">Details</p>
                <Separator />
                <CardContent className="space-y-3 p-2">
                    <div className="space-y-1 px-2">
                        <div className="flex-between">
                            <p className="text-xl font-bold">{call?.title}</p>
                            <CircleEllipsisIcon className="text-black text-opacity-50" />
                        </div>
                        {call?.severity ? (
                            <Badge
                                className={cn(
                                    "w-fit",
                                    call.severity === "CRITICAL"
                                        ? "bg-hover:bg-red-500/80 bg-red-500"
                                        : call.severity === "MODERATE"
                                          ? "bg-yellow-500 hover:bg-yellow-500/80"
                                          : "bg-hover:bg-green-500/80 bg-green-500",
                                )}
                            >
                                {call.severity}
                            </Badge>
                        ) : null}
                    </div>
                    {/* Placeholder for image */}
                    {call?.street_view ? (
                        <img
                            src={`data:image/png;base64, ${call.street_view}`}
                            className="h-[200px] w-full bg-cover bg-no-repeat"
                        />
                    ) : (
                        <div className="duration-5000 h-[200px] w-full animate-pulse bg-gray-500" />
                    )}
                    {call && (
                        <div className="grid grid-cols-2">
                            {/* <EmergencyInfoItem
                            label="Distance"
                            // value={call.distance}
                            value={"8 miles"}
                            side="right"
                        />
                        <EmergencyInfoItem label="Type" value={call.type} /> */}
                            <EmergencyInfoItem
                                label="Time of Call"
                                value={new Date(
                                    new Date(call.time).getTime() -
                                        7 * 60 * 60 * 1000,
                                ).toLocaleTimeString("en-US", {
                                    timeZone: "America/Los_Angeles",
                                })}
                                side="right"
                            />
                            <EmergencyInfoItem
                                label="Location"
                                value={call.location_name}
                                side="left"
                            />
                        </div>
                    )}
                    <Separator />
                    <div className="px-2">
                        <p className="text-sm text-black text-opacity-50">
                            Summary
                        </p>
                        <ScrollArea
                            type="auto"
                            className="max-h-[80px] overflow-y-scroll"
                        >
                            <p className="text-base leading-snug">
                                {call?.summary}
                                {/* afdslfkajdslfjasldjlfdaslkjflaskdjflaskdjflaskjdfladksjflaskjdflaksjdflaksjdlfjsadlkfjaslkjflaskjdflkasjdflkj
                                fadsfasdf fadsfasdfasdf
                                afdslfkajdslfjasldjlfdaslkjflaskdjflaskdjflaskjdfladksjflaskjdflaksjdflaksjdlfjsadlkfjaslkjflaskjdflkasjdflkjasdf
                                addressfasdf fdas */}
                            </p>
                        </ScrollArea>
                    </div>
                </CardContent>
                <CardFooter className="px-4 pb-4 pt-2">
                    <div className="flex w-full flex-col space-y-2">
                        <p className="text-lg font-semibold">
                            Dispatch first responders:
                        </p>
                        <div className="mb-2 flex justify-between gap-1">
                            <Button
                                variant="default"
                                className="max-w-fit flex-1 items-center justify-center rounded-md bg-blue-500 px-2 hover:bg-blue-600"
                                onClick={() => {
                                    toast({
                                        title: "Dispatched: Police",
                                        description: `Officers were dispatched${call?.location_name ? ` to ${call?.location_name}` : ""}.`,
                                        variant: "police",
                                    });
                                    handleResolve(call.id);
                                    setClicked((prev) => prev * 2);
                                }}
                                disabled={clicked % 2 === 0}
                            >
                                <Siren className="mr-2" />
                                <p className="overflow-clip text-ellipsis">
                                    Police
                                </p>
                            </Button>
                            <Button
                                variant="default"
                                className="flex-1 items-center justify-center rounded-md bg-red-500 px-2 hover:bg-red-600"
                                onClick={() => {
                                    toast({
                                        title: "Dispatched: Firefighters",
                                        description: `Firefighters were dispatched${call?.location_name ? ` to ${call?.location_name}` : ""}.`,
                                        variant: "firefighter",
                                    });
                                    handleResolve(call.id);
                                    setClicked((prev) => prev * 3);
                                }}
                                disabled={clicked % 3 === 0}
                            >
                                <FireExtinguisher className="mr-2 min-w-fit" />
                                <p className="overflow-clip text-ellipsis">
                                    Firefighters
                                </p>
                            </Button>
                            <Button
                                variant="default"
                                className="flex-1 items-center justify-center rounded-md bg-green-500 px-2 hover:bg-green-600"
                                onClick={() => {
                                    toast({
                                        title: "Dispatched: Paramedics",
                                        description: `Paramedics were dispatched${call?.location_name ? ` to ${call?.location_name}` : ""}.`,
                                        variant: "paramedic",
                                    });
                                    handleResolve(call.id);
                                    setClicked((prev) => prev * 5);
                                }}
                                disabled={clicked % 5 === 0}
                            >
                                <Ambulance className="mr-2" />
                                <p className="overflow-clip text-ellipsis">
                                    Paramedics
                                </p>
                            </Button>
                        </div>
                    </div>
                </CardFooter>
            </Card>
        </motion.div>
    );
};

export default DetailsPanel;
