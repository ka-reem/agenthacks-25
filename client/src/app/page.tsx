import Link from "next/link";

export default async function Home() {
    return (
        <main className="wrapper flex-center text-3xl md:text-5xl font-semibold min-h-[calc(100vh-6rem)]">
            <Link
                href={"https://github.com/KevinWu098/kTemp"}
                target="_blank"
                referrerPolicy="no-referrer"
                className="underline"
            >
                Hello World 💖
            </Link>
        </main>
    );
}
