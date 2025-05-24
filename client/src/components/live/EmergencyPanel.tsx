import Image from "next/image";
import { CircleEllipsisIcon, FireExtinguisher, Ambulance, Siren } from "lucide-react";

import { Button } from "../ui/button";
import { Separator } from "../ui/separator";
import { Badge } from "../ui/badge"
import { Card, CardContent, CardHeader, CardFooter } from "../ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";

const EmergencyInfoItem = ({ label, value }: { label: string; value: string | React.ReactNode }) => (
    <div className="px-3 py-2">
        <p className="text-sm font-medium leading-3 text-black text-opacity-50">
            {label}
        </p>
        {typeof value === 'string' ? (
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
        summary: "Qui consectetur labore voluptate ea voluptate commodo nostrud sint labore consectetur qui nulla reprehenderit ad. Ut mollit nisi officia laboris exercitation cillum sit non eiusmod consequat. Non proident proident ad Lorem. Qui ea tempor labore deserunt dolor ad proident sit id nisi proident dolore. Nostrud commodo minim fugiat pariatur minim irure labore aute. Adipisicing mollit consequat ut id excepteur labore laboris. In laborum nisi aute duis pariatur eu."
    };

    return (
        <Card className="h-fit w-[400px] border-l border-b border-gray-400 rounded-none px-2">
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
                            variant={emergency.status === 'CRITICAL' ? 'destructive' : 
                                    emergency.status === 'MODERATE' ? 'secondary' : 'default'}
                            className="ml-2"
                        >
                            {emergency.status}
                        </Badge>
                    </div>
                </div>

                {/* Placeholder for image */}
                <div className="h-[200px] w-full bg-gray-500" />

                <div className="grid grid-cols-2 grid-rows-2">
                    <EmergencyInfoItem label="Distance" value={emergency.distance} />
                    <EmergencyInfoItem 
                        label="Type" 
                        value={
                            <Select defaultValue={emergency.type}>
                                <SelectTrigger className=" text-lg font-semibold">
                                    <SelectValue placeholder="Select type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="Fire">Fire</SelectItem>
                                    <SelectItem value="Medical">Medical</SelectItem>
                                    <SelectItem value="Crime">Crime</SelectItem>
                                    <SelectItem value="Natural Disaster">Natural Disaster</SelectItem>
                                    <SelectItem value="Traffic">Traffic</SelectItem>
                                </SelectContent>
                            </Select>
                        } 
                    />
                    <EmergencyInfoItem label="Time" value={emergency.time} />
                    <EmergencyInfoItem label="Location" value={emergency.location} />
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
                <div className="flex flex-col space-y-2 w-full">
                    <Button variant="default" className="w-full rounded-md bg-blue-500 hover:bg-blue-600 flex items-center justify-start">
                        <Siren className="mr-2" />
                        Dispatch Police
                    </Button>
                    <Button variant="default" className="w-full rounded-md bg-red-500 hover:bg-red-600 flex items-center justify-start">
                        <FireExtinguisher className="mr-2" />
                        Dispatch Firefighters
                    </Button>
                    <Button variant="default" className="w-full rounded-md bg-green-500 hover:bg-green-600 flex items-center justify-start">
                        <Ambulance className="mr-2" />
                        Dispatch Paramedics
                    </Button>
                </div>
            </CardFooter>
        </Card>
    );
};

export default EmergencyPanel;
