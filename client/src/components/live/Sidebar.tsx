"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    Headset,
    HeartPulseIcon,
    HomeIcon,
    RadioIcon,
    User2Icon,
} from "lucide-react";

import { Separator } from "../ui/separator";

const Sidebar = () => {
    const pathname = usePathname();

    return (
        <div className="flex w-12 flex-col items-center border-r-2 border-[#C2C2C2] bg-[#F6F8FC] pt-1">
            <div className="flex-center aspect-square flex-col rounded-full p-2">
                <Link href="/">
                    <Headset className="m-auto" />
                </Link>
                <Separator className="mx-3 my-5 w-5 bg-[#6C6C6C] p-[1px]" />
            </div>
            <div className="flex flex-col space-y-5">
                <HomeIcon />
                <Link href="/live">
                    <RadioIcon
                        className={cn(pathname == "/live" && "text-blue-500")}
                    />
                </Link>
                <User2Icon />
            </div>
        </div>
    );
};

export default Sidebar;
