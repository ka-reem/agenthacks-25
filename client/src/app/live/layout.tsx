import type { Metadata } from "next";

import Header from "./Header";
import Sidebar from "./Sidebar";

export const metadata: Metadata = {
    title: "Live — DispatcherAI",
    icons: [{ rel: "icon", url: "/favicon.ico" }],
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-[100dvh] min-w-[100dvw]">
            <Sidebar />
            <div className="w-full">
                <Header />
                {children}
            </div>
        </div>
    );
}
