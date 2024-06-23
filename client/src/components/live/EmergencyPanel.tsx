import Image from "next/image";
import { CircleEllipsisIcon } from "lucide-react";

import { Button } from "../ui/button";
import { Separator } from "../ui/separator";

const EmergencyPanel = () => {
    return (
        <div className="w-[400px] bg-white">
            <p className="px-2 py-[6px]">Emergency</p>
            <Separator />
            <div className="space-y-2 p-2">
                <div className="space-y-2">
                    <div className="flex-between">
                        <p className="text-xl font-bold">
                            House Fire in Lincoln Ave.
                        </p>
                        <CircleEllipsisIcon className="text-black text-opacity-50" />
                    </div>

                    <div className="h-6 w-fit bg-gray-300">
                        <p className="w-fit px-2 py-1 text-[12px] font-medium uppercase">
                            <b>Severity:</b> High
                        </p>
                    </div>
                </div>

                {/* Placeholder for image */}
                <div className="h-[200px] w-full bg-gray-500" />

                <div className="grid grid-cols-2 grid-rows-2">
                    <div className="border-b-[1px] border-r-[1px] px-3 py-2">
                        <p className="text-sm font-medium leading-3 text-black text-opacity-50">
                            Distance
                        </p>
                        <p className="text-lg font-semibold">22 miles</p>
                    </div>
                    <div className="border-b-[1px] border-l-[1px] px-3 py-2">
                        <p className="text-sm font-medium leading-3 text-black text-opacity-50">
                            Type
                        </p>
                        <p className="text-lg font-semibold">Fire</p>
                    </div>
                    <div className="border-r-[1px] border-t-[1px] px-3 py-2">
                        <p className="text-sm font-medium leading-3 text-black text-opacity-50">
                            Time
                        </p>
                        <p className="text-lg font-semibold">12:34 AM</p>
                    </div>
                    <div className="border-l-[1px] border-t-[1px] px-3 py-2">
                        <p className="text-sm font-medium leading-3 text-black text-opacity-50">
                            Location
                        </p>
                        <p className="text-lg font-semibold">Lincoln Ave.</p>
                    </div>
                </div>

                <Separator />

                <div className="px-3">
                    <p className="text-sm text-black text-opacity-50">
                        Summary
                    </p>
                    <p className="line-clamp-3 text-base leading-snug">
                        Qui consectetur labore voluptate ea voluptate commodo
                        nostrud sint labore consectetur qui nulla reprehenderit
                        ad. Ut mollit nisi officia laboris exercitation cillum
                        sit non eiusmod consequat. Non proident proident ad
                        Lorem. Qui ea tempor labore deserunt dolor ad proident
                        sit id nisi proident dolore. Nostrud commodo minim
                        fugiat pariatur minim irure labore aute. Adipisicing
                        mollit consequat ut id excepteur labore laboris. In
                        laborum nisi aute duis pariatur eu.
                    </p>
                </div>

                <div className="pt-4">
                    <Button variant="default" className="w-full rounded-none">
                        Dispatch Responder
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default EmergencyPanel;
