"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { HeartPulseIcon, HomeIcon, RadioIcon, User2Icon } from "lucide-react";

const Sidebar = () => {
    const pathname = usePathname();

    return (
        <div className="flex w-12 flex-col items-center space-y-5 border-r-2 border-gray-400 bg-gray-200 py-4">
            <div className="flex-center aspect-square h-8 w-8 flex-col bg-black">
                <HeartPulseIcon className="m-auto text-white" />
            </div>
            <div className="flex flex-col space-y-3">
                <HomeIcon />
                <Link href="/live">
                    <RadioIcon
                        className={cn(pathname == "/live" && "bg-red-500")}
                    />
                </Link>
                <User2Icon />
            </div>
        </div>
    );
};

export default Sidebar;
