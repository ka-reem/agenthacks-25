import { ChangeEvent, useEffect, useState } from "react";
import { Call } from "@/app/live/page";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { AlertCircle, AlertTriangle, Search, ShieldCheck } from "lucide-react";

interface EventPanelProps {
    data: Record<string, Call> | undefined;
    selectedId: string | undefined;
    handleSelect: (id: string) => void;
}

const EventPanel = ({ data, selectedId, handleSelect }: EventPanelProps) => {
    const [search, setSearch] = useState("");

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setSearch(e.currentTarget.value);
    };

    return (
        <div className="absolute left-0 z-50 h-full w-[360px] max-w-md rounded-none bg-white p-2 shadow-lg">
            <div className="mb-2 flex items-center justify-between px-3">
                <h2 className="text-xl font-bold">Emergencies</h2>
            </div>

            <div className="mb-4 flex items-center space-x-4 px-2">
                <Input
                    className="w-[85%]"
                    placeholder="Filter calls..."
                    startIcon={Search}
                    onChange={handleChange}
                />
                {/* <span className="pr-8 text-gray-500">Filter</span> */}
            </div>

            <div className="mb-4 flex justify-between px-3">
                <div>
                    <div className="text-2xl font-bold">
                        {data ? Object.keys(data).length : "x"}
                    </div>
                    <div className="text-sm text-gray-500">Total</div>
                </div>
                <div>
                    <div className="text-2xl font-bold">
                        {data
                            ? Object.entries(data).filter(
                                  ([_, value]) => value.severity === "CRITICAL",
                              ).length
                            : "x"}
                    </div>
                    <div className="text-sm text-gray-500">Critical</div>
                </div>
                <div>
                    <div className="text-2xl font-bold">
                        {data
                            ? Object.entries(data).filter(
                                  ([_, value]) => value.severity === "RESOLVED",
                              ).length
                            : "x"}
                    </div>
                    <div className="text-sm text-gray-500">Resolved</div>
                </div>
            </div>

            <div className="h-[calc(100dvh-250px)] space-y-2 overflow-y-scroll pb-3">
                {data &&
                    Object.entries(data)
                        .filter(([_, emergency]) =>
                            emergency.title?.includes(search),
                        )
                        .sort(([_, a], [__, b]) =>
                            new Date(a.time) < new Date(b.time) ? 1 : -1,
                        )
                        .map(([_, emergency]) => (
                            <Card
                                key={emergency.id}
                                className={cn(
                                    "m-2 flex cursor-pointer items-center p-3",
                                    selectedId === emergency.id &&
                                        "ring-2 ring-blue-500 ring-offset-2",
                                )}
                                onClick={() => handleSelect(emergency.id)}
                            >
                                {emergency.severity === "CRITICAL" && (
                                    <AlertCircle
                                        className="mr-3 min-w-6 text-red-500"
                                        size={24}
                                    />
                                )}
                                {emergency.severity === "MODERATE" && (
                                    <AlertTriangle
                                        className="mr-3 min-w-6 text-orange-500"
                                        size={24}
                                    />
                                )}
                                {emergency.severity === "RESOLVED" && (
                                    <ShieldCheck
                                        className="mr-3 min-w-6 text-green-500"
                                        size={24}
                                    />
                                )}
                                <CardContent className="flex-grow p-0">
                                    <div className="font-semibold">
                                        {emergency.title}
                                    </div>
                                    <div className="text-sm text-gray-500">
                                        {new Date(
                                            emergency.time,
                                        ).toLocaleTimeString()}
                                    </div>
                                </CardContent>
                                {emergency.severity ? (
                                    <Badge
                                        className={cn(
                                            "min-w-fit uppercase",
                                            emergency.severity === "CRITICAL"
                                                ? "bg-red-500 hover:bg-red-500/80"
                                                : emergency.severity ===
                                                    "MODERATE"
                                                  ? "bg-yellow-500 hover:bg-yellow-500/80"
                                                  : "bg-green-500 hover:bg-green-500/80",
                                        )}
                                    >
                                        {emergency.severity}
                                    </Badge>
                                ) : null}
                            </Card>
                        ))}
            </div>
        </div>
    );
};

export default EventPanel;
