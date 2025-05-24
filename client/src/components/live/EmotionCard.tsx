import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const EmotionCard = ({
    emotion,
    percentage,
    color,
}: {
    emotion: string;
    percentage: number;
    color: string;
}) => {
    return (
        <Card className="h-full w-[50%]">
            <CardHeader className="p-2 pb-0 pt-3">
                <CardTitle className="text-gray-500">
                    <p className="text-xs leading-3">CALLER EMOTION</p>
                    <h2 className="line-clamp-1 text-xl font-bold text-black">
                        {emotion}
                    </h2>
                </CardTitle>
            </CardHeader>
            <CardContent className="p-2 pt-0">
                <div className="flex items-center space-x-2">
                    <div className="h-2.5 w-full rounded-full bg-gray-200">
                        <div
                            className={`h-2.5 rounded-full ${color}`}
                            style={{ width: `${percentage}%` }}
                        />
                    </div>
                    <span className="pr-2 text-sm font-medium text-gray-500">
                        {percentage.toFixed(0)}%
                    </span>
                </div>
            </CardContent>
        </Card>
    );
};
export default EmotionCard;
