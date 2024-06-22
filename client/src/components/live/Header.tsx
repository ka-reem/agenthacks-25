import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

const Header = () => {
    const currentTime = new Date();

    return (
        <div className="flex h-[50px] w-full items-center bg-gray-300 px-7">
            <div className="flex-between w-full text-sm font-bold uppercase text-gray-800">
                <h1>Location</h1>

                <div className="flex-center space-x-4 font-normal">
                    <p>{currentTime.toLocaleTimeString()} PDT</p>
                    <div className="uppercase">
                        <Select defaultValue="SF">
                            <SelectTrigger className="h-[30px] min-h-0 w-[200px] rounded-none border-[1px] border-gray-500 py-0 uppercase">
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
