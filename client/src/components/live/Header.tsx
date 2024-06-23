"use client";

import { useEffect, useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

const Header = ({ connected }: { connected: boolean }) => {
    const [time, setTime] = useState("");

    useEffect(() => {
        const updateTime = () => {
            const now = new Date();
            setTime(now.toLocaleTimeString());
        };
        updateTime();
        const intervalId = setInterval(updateTime, 1000);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="flex h-[50px] w-full items-center border-b-2 border-[#C2C2C2] bg-white px-7">
            <div className="flex-between w-full text-sm font-bold uppercase text-gray-800">
                <div className="flex items-center space-x-3">
                    <h1>Location</h1>
                    <div
                        className={cn(
                            "h-3 w-3 rounded-full",
                            connected
                                ? "bg-green-500 ring-2 ring-green-500 ring-offset-2"
                                : "bg-red-500 ring-2 ring-red-500 ring-offset-2",
                        )}
                    />
                </div>

                <div className="flex-center space-x-4 font-normal">
                    <p>{time} PDT</p>
                    <div className="uppercase">
                        <Select defaultValue="SF">
                            <SelectTrigger className="h-[30px] min-h-0 w-[200px] rounded-md border-[1px] border-[#D7D7D7] py-0 uppercase text-[#6C6C6C]">
                                <SelectValue placeholder="Location" />
                            </SelectTrigger>
                            <SelectContent className="uppercase">
                                <SelectItem value="SF" className="uppercase">
                                    San Francisco, CA
                                </SelectItem>
                                <SelectItem value="BER" disabled>
                                    Berkeley, CA
                                </SelectItem>
                                <SelectItem value="OAK" disabled>
                                    Oakland, CA
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Header;
