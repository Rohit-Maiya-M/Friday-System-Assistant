import {
    useState,
    useRef,
    useEffect
} from "react";


export default function App() {

    const [messages, setMessages] = useState([

        {
            role: "assistant",
            text: "Hello, I am Friday."
        }
    ]);

    const [input, setInput] =
        useState("");

    const [voiceState, setVoiceState] =
        useState("idle");

    const [transcript, setTranscript] =
        useState("");

    const [toast, setToast] =
        useState(null);

    const messagesEndRef =
        useRef(null);


    useEffect(() => {

        messagesEndRef.current?.scrollIntoView({

            behavior: "smooth"
        });

    }, [messages]);


    useEffect(() => {

        const interval = setInterval(

            async () => {

                try {

                    const response =
                        await fetch(

                            "http://127.0.0.1:8000/voice-state"
                        );

                    const data =
                        await response.json();

                    setVoiceState(
                        data.state
                    );

                    setTranscript(
                        data.transcript
                    );

                } catch {

                }

            },

            1500
        );

        return () => {

            clearInterval(
                interval
            );
        };

    }, []);


    useEffect(() => {

        const interval = setInterval(

            async () => {

                try {

                    const response =
                        await fetch(

                            "http://127.0.0.1:8000/toast"
                        );

                    const data =
                        await response.json();

                    if (data.visible) {

                        setToast(
                            data.message
                        );

                    } else {

                        setToast(null);
                    }

                } catch {

                }

            },

            1500
        );

        return () => {

            clearInterval(
                interval
            );
        };

    }, []);


    async function sendMessage() {

        if (!input.trim()) {
            return;
        }

        const userMessage = {

            role: "user",

            text: input
        };

        setMessages(prev => [

            ...prev,
            userMessage
        ]);

        const currentInput = input;

        setInput("");

        try {

            const response = await fetch(

                "http://127.0.0.1:8000/chat",

                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        message: currentInput
                    })
                }
            );

            const data =
                await response.json();

            setMessages(prev => [

                ...prev,

                {
                    role: "assistant",

                    text: data.response
                }
            ]);

        } catch {

            setMessages(prev => [

                ...prev,

                {
                    role: "assistant",

                    text:
                        "❌ Backend connection failed."
                }
            ]);
        }
    }

    return (

        <div className="h-screen w-screen bg-transparent flex items-end justify-end p-4">

            <div className="relative w-[400px] h-[700px] rounded-[28px] border border-white/10 bg-zinc-900/80 backdrop-blur-2xl shadow-2xl flex flex-col overflow-hidden">

                <div className="h-[60px] border-b border-white/10 flex items-center justify-between px-5">

                    <div className="flex items-center gap-3">

                        <div className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse" />

                        <h1 className="text-white text-lg font-semibold">

                            Friday
                        </h1>
                    </div>

                    <button
                        onClick={() => {

                            window
                                .electronAPI
                                .hideWindow();
                        }}
                        className="text-zinc-400 hover:text-white transition"
                    >
                        ▼
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto px-4 py-5 space-y-4 flex flex-col">

                    {messages.map(

                        (message, index) => (

                            <div
                                key={index}
                                className={`max-w-[85%] px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                                    message.role === "assistant"

                                        ? "bg-zinc-800 text-white self-start"

                                        : "bg-cyan-500 text-black self-end"
                                }`}
                            >
                                {message.text}
                            </div>
                        )
                    )}

                    <div ref={messagesEndRef} />
                </div>

                <div className="p-4 border-t border-white/10">

                    <div className="flex items-center gap-3 bg-zinc-800 rounded-2xl px-4 py-3">

                        <input
                            type="text"

                            value={input}

                            onChange={(e) => {

                                setInput(
                                    e.target.value
                                );
                            }}

                            onKeyDown={(e) => {

                                if (
                                    e.key === "Enter"
                                ) {

                                    sendMessage();
                                }
                            }}

                            placeholder="Message Friday..."

                            className="flex-1 bg-transparent outline-none text-white placeholder:text-zinc-500 text-sm"
                        />

                        <button
                            onClick={sendMessage}
                            className="text-cyan-400 hover:text-cyan-300 transition"
                        >
                            ↑
                        </button>
                    </div>
                </div>

                {voiceState !== "idle" && (

                    <div className="absolute inset-0 bg-black/70 backdrop-blur-xl flex flex-col items-center justify-center z-50">

                        <div className="w-24 h-24 rounded-full bg-cyan-400/20 flex items-center justify-center animate-pulse">

                            <div className="w-12 h-12 rounded-full bg-cyan-400" />
                        </div>

                        <div className="mt-8 text-white text-lg font-medium">

                            {voiceState === "listening" &&
                                "🎤 Listening..."}

                            {voiceState === "processing" &&
                                "🧠 Understanding..."}

                            {voiceState === "executing" &&
                                "⚡ Executing..."}
                        </div>

                        <div className="mt-4 text-zinc-300 text-center px-8 text-sm">

                            {transcript}
                        </div>
                    </div>
                )}
            </div>

            {toast && (

                <div className="absolute bottom-6 right-6 z-[100] animate-pulse">

                    <div className="w-[320px] rounded-2xl border border-white/10 bg-zinc-900/95 backdrop-blur-xl shadow-2xl px-5 py-4">

                        <div className="text-sm text-zinc-300">

                            {toast}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}