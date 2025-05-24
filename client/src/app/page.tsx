"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import FadeIn from "react-fade-in";

export default function Home() {
    const styles = {
        container: "max-w-4xl mx-auto px-4 py-8",
        heading:
            "text-3xl md:text-4xl font-semibold font-helvetica-neue text-white mb-4",
        subheading: "text-lg md:text-xl font-inter text-gray-300",
        span: "text-[#69D2FF]",
        tealsubheading: "text-[#69D2FF] text-md font-semibold",
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
                            <h1 className="mb-4 text-5xl font-bold">
                                The AI dispatcher eliminating 911 wait times
                            </h1>
                            <p className="mb-8 text-xl text-gray-600">
                                Human-in-the-loop emergency response system
                            </p>
                            <div className="space-x-4">
                                <Link href="/live">
                                    <Button
                                        variant="outline"
                                        style={{
                                            fontSize: "22px",
                                            padding: "24px 22px",
                                        }}
                                    >
                                        Try demo
                                    </Button>
                                </Link>
                                <Link href="/live">
                                    <Button
                                        style={{
                                            backgroundColor: "#0075FF",
                                            fontSize: "22px",
                                            padding: "24px 22px",
                                        }}
                                    >
                                        Start now
                                    </Button>
                                </Link>
                            </div>
                        </FadeIn>
                    </div>
                    <FadeIn
                        className="flex h-full w-full items-center justify-center md:w-3/5"
                        transitionDuration={1000}
                    >
                        {/* <div className="flex h-full w-full items-center justify-center md:w-3/5"> */}
                        <img src="../dispatcherHero.png" alt="" />
                        {/* </div>{" "} */}
                    </FadeIn>
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
                    padding: "22px 0",
                }}
            >
                <div
                    className={styles.container}
                    style={{ width: "50%", marginLeft: "600px" }}
                >
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
            {/* features */}

            <div
                style={{
                    height: "120vh",
                    width: "100vw",
                    backgroundColor: "#1E1E1E",
                    alignContent: "center",
                    justifyContent: "center",
                }}
            >
                <hr
                    style={{
                        border: "1px solid #3B3B3B",
                        width: "100%",
                        marginBottom: "56px",
                    }}
                />
                <p
                    className={styles.tealsubheading}
                    style={{ textAlign: "center" }}
                >
                    THE SOLUTION
                </p>
                <h1 className={styles.heading} style={{ textAlign: "center" }}>
                    We offer personalized support that everyone deserves.
                </h1>{" "}
                <FadeIn>
                    <div
                        style={{
                            display: "flex",
                            flexDirection: "row",
                            gap: "12px",
                            padding: "56px",
                        }}
                    >
                        <img src="/action.png" style={{ width: "100%" }} />

                        <img src="/communicate.png" style={{ width: "100%" }} />
                        <img src="/moderate.png" style={{ width: "100%" }} />
                    </div>
                </FadeIn>
            </div>
            {/* ending */}
            <div
                className={styles.container}
                style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "12px",
                    alignContent: "center",
                    justifyContent: "center",
                }}
            >
                <h1
                    className={styles.heading}
                    style={{ color: "black", textAlign: "center" }}
                >
                    Start personalizing your emergency response system. Start
                    with Dispatch.
                </h1>
                <div
                    className="space-x-4"
                    style={{
                        display: "flex",
                        alignContent: "center",
                        justifyContent: "center",
                    }}
                >
                    <Link href="/live">
                        <Button
                            variant="outline"
                            style={{
                                fontSize: "22px",
                                padding: "24px 22px",
                            }}
                        >
                            Try demo
                        </Button>
                    </Link>
                    <Link href="/live">
                        <Button
                            style={{
                                backgroundColor: "#0075FF",
                                fontSize: "22px",
                                padding: "24px 22px",
                            }}
                        >
                            Start now
                        </Button>
                    </Link>
                </div>
            </div>
        </div>
    );
}
