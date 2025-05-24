"use client";

import { ChangeEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertTriangleIcon, SearchIcon } from "lucide-react";

import { Separator } from "../ui/separator";

type Detail = {
    name: string;
    value: number;
};

const DETAILS: Detail[] = [
    {
        name: "Total",
        value: 123,
    },
    {
        name: "Critical",
        value: 34,
    },
    {
        name: "Resolved",
        value: 12,
    },
];

const EventPanel = () => {
    const [searchValue, setSearchValue] = useState("");

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setSearchValue(e.currentTarget.value);
    };

    console.log(searchValue);

    return (
        <div className="h-full w-[450px] bg-gray-300 p-5">
            <Tabs defaultValue="emergencies">
                <TabsList>
                    <TabsTrigger value="emergencies">Emergencies</TabsTrigger>
                    <TabsTrigger value="alerts" disabled>
                        Alerts
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="emergencies" className="space-y-3">
                    <Separator className="my-2 w-[95%] bg-gray-400" />

                    <Input
                        startIcon={SearchIcon}
                        placeholder="Search a location"
                        className="w-[90%]"
                        onChange={handleChange}
                    />

                    <div className="grid grid-cols-3">
                        {DETAILS.map((item) => (
                            <div>
                                <p className="text-base text-black text-opacity-50">
                                    {item.name}
                                </p>
                                <p className="text-3xl font-semibold">
                                    {item.value}
                                </p>
                            </div>
                        ))}
                    </div>

                    <div className="max-h-[calc(100dvh-275px)] space-y-2 overflow-y-scroll">
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <div className="flex h-[88px] w-full space-x-4 bg-white p-2">
                            <div className="my-auto">
                                <AlertTriangleIcon className="h-12 w-12" />
                            </div>
                            <div className="w-full">
                                <div className="flex justify-between">
                                    <div>
                                        <p className="line-clamp-1 max-w-48 overflow-hidden text-ellipsis break-all text-base font-semibold">
                                            House Fire in Blair Hills
                                        </p>
                                        <p className="text-sm text-gray-400">
                                            10:31 AM
                                        </p>
                                    </div>

                                    <div className="grow" />

                                    <div className="h-6 bg-gray-300">
                                        <p className="px-2 py-1 text-[12px] font-medium uppercase">
                                            <b>Severity:</b> High
                                        </p>
                                    </div>
                                </div>

                                <div className="flex justify-end space-x-4">
                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase text-black text-opacity-50"
                                        size="sm"
                                    >
                                        Dismiss
                                    </Button>

                                    <Button
                                        variant="link"
                                        className="min-h-0 px-0 font-medium uppercase"
                                        size="sm"
                                    >
                                        Resolve
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </TabsContent>
                <TabsContent value="alerts">Alerts</TabsContent>
            </Tabs>
        </div>
    );
};

export default EventPanel;
