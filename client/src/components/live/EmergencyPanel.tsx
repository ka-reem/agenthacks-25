import Image from "next/image";
import {
    Ambulance,
    CircleEllipsisIcon,
    FireExtinguisher,
    Siren,
} from "lucide-react";

import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "../ui/card";
import { Separator } from "../ui/separator";

const EmergencyInfoItem = ({
    label,
    value,
}: {
    label: string;
    value: string | React.ReactNode;
}) => (
    <div className="px-3 py-2">
        <p className="text-sm font-medium leading-3 text-black text-opacity-50">
            {label}
        </p>
        {typeof value === "string" ? (
            <p className="text-lg font-semibold">{value}</p>
        ) : (
            value
        )}
    </div>
);

const EmergencyPanel = () => {
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

    return (
        <Card className="h-fit w-[500px] rounded-none border-b border-l border-gray-400 px-2">
            <CardHeader className="px-2 py-[6px]">
                <p>Emergency</p>
                <Separator />
            </CardHeader>
            <CardContent className="space-y-2 p-2">
                <div className="space-y-2">
                    <div className="flex-between">
                        <p className="text-xl font-bold">{emergency.title}</p>
                        <CircleEllipsisIcon className="text-black text-opacity-50" />
                    </div>

                    <div className="h-6 w-fit">
                        <Badge
                            variant={
                                emergency.status === "CRITICAL"
                                    ? "destructive"
                                    : emergency.status === "MODERATE"
                                      ? "secondary"
                                      : "default"
                            }
                            className="ml-2"
                        >
                            {emergency.status}
                        </Badge>
                    </div>
                </div>

                {/* Placeholder for image */}
                <div className="h-[200px] w-full bg-gray-500" />

                <div className="grid grid-cols-2 grid-rows-2">
                    <EmergencyInfoItem
                        label="Distance"
                        value={emergency.distance}
                    />
                    <EmergencyInfoItem label="Type" value={emergency.type} />
                    <EmergencyInfoItem label="Time" value={emergency.time} />
                    <EmergencyInfoItem
                        label="Location"
                        value={emergency.location}
                    />
                </div>

                <Separator />

                <div className="px-3">
                    <p className="text-sm text-black text-opacity-50">
                        Summary
                    </p>
                    <p className="line-clamp-3 text-base leading-snug">
                        {emergency.summary}
                    </p>
                </div>
            </CardContent>
            <CardFooter className="pt-4">
                <div className="flex w-full flex-col space-y-2">
                    <p className="text-lg font-semibold">
                        Dispatch first responders:
                    </p>
                    <div className="mb-2 flex justify-between gap-1">
                        <Button
                            variant="default"
                            className="flex-1 items-center justify-center rounded-md bg-blue-500 hover:bg-blue-600"
                        >
                            <Siren className="mr-2" />
                            Police
                        </Button>
                        <Button
                            variant="default"
                            className="flex-1 items-center justify-center rounded-md bg-red-500 hover:bg-red-600"
                        >
                            <FireExtinguisher className="mr-2" />
                            Firefighters
                        </Button>
                        <Button
                            variant="default"
                            className="flex-1 items-center justify-center rounded-md bg-green-500 hover:bg-green-600"
                        >
                            <Ambulance className="mr-2" />
                            Paramedics
                        </Button>
                    </div>
                </div>
            </CardFooter>
        </Card>
    );
};

export default EmergencyPanel;
