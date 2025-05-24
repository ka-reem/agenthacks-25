"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import FadeIn from "react-fade-in";

export default async function Home() {
    const styles = {
        container: "max-w-4xl mx-auto px-4 py-8",
        heading:
            "text-4xl md:text-5xl font-bold font-helvetica-neue text-white mb-4",
        subheading: "text-lg md:text-xl font-inter text-gray-300",
        span: "text-[#69D2FF]",
    };
    return (
        <div>
            <nav
                className="flex items-center justify-between bg-white p-4 shadow-sm"
                style={{ position: "sticky", top: "0", zIndex: 1000 }}
            >
                <div className="flex items-center">
                    <img src="../dispatchLogo.png" alt="" />
                </div>
                <div className="space-x-4">
                    <a href="#" className="font-medium text-blue-600">
                        Home
                    </a>
                    <a href="#" className="font-medium text-gray-600">
                        Features
                    </a>
                    <a href="#" className="font-medium text-gray-600">
                        About us
                    </a>
                </div>
                <div>
                    <Button variant="outline" className="mr-2">
                        Log in
                    </Button>
                    <Button
                        style={{
                            backgroundColor: "#0075FF",
                            padding: "12px",
                        }}
                    >
                        Try now
                    </Button>
                </div>
            </nav>
            {/* hero */}
            <div className="flex min-h-screen flex-col bg-white">
                <main
                    className="flex flex-grow flex-col md:flex-row"
                    style={{ position: "relative" }}
                >
                    <div className="flex w-full flex-col justify-center px-9 md:w-2/5">
                        <FadeIn>
                            <Button
                                variant="outline"
                                className="mb-6 self-start"
                            >
                                <span>Try it out</span>
                                <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                            <h1 className="mb-6 text-5xl font-bold">
                                An AI First Responder in your pocket.
                            </h1>
                            <p className="mb-8 text-xl text-gray-600">
                                Human-in-the-loop emergency response system
                            </p>
                            <div className="space-x-4">
                                <Button
                                    variant="outline"
                                    style={{
                                        fontSize: "22px",
                                        padding: "24px 22px",
                                    }}
                                >
                                    Try demo
                                </Button>
                                <Button
                                    style={{
                                        backgroundColor: "#0075FF",
                                        fontSize: "22px",
                                        padding: "24px 22px",
                                    }}
                                >
                                    Start now
                                </Button>
                            </div>
                        </FadeIn>
                    </div>
                    <div className="flex h-full w-full items-center justify-center md:w-3/5">
                        <img src="../dispatcherHero.png" alt="" />
                    </div>
                </main>
            </div>
            {/* problem */}
            <div
                style={{
                    backgroundImage: "url('/dispatchProblem.png')",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    width: "100%",
                    height: "100vh",
                    backgroundColor: "#1E1E1E",
                    padding:"22px 0"
                }}
            >
                <div className={styles.container} style={{width: "50%", marginLeft: "600px"}}>
                    <h1 className={styles.heading}>
                        82% of 911 Call Centers are
                        <span className={styles.span}> Understaffed</span>
                    </h1>
                    <p className={styles.subheading}>
                        According to Axios, the majority of Americans do not
                        have access to emergency services that should be
                        guaranteed to them.
                    </p>
                </div>
            </div>
        </div>
    );
}
