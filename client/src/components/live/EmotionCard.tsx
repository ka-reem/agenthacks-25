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
        <Card className="h-full w-64">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm text-gray-500">
                    CALLER EMOTION
                </CardTitle>
            </CardHeader>
            <CardContent>
                <h2 className="mb-2 text-2xl font-bold">{emotion}</h2>
                <div className="flex items-center">
                    <div className="h-2.5 w-full rounded-full bg-gray-200">
                        <div
                            className={`h-2.5 rounded-full ${color}`}
                            style={{ width: `${percentage}%` }}
                        ></div>
                    </div>
                    <span className="ml-2 text-sm font-medium text-gray-500">
                        {percentage}%
                    </span>
                </div>
            </CardContent>
        </Card>
    );
};
export default EmotionCard;
