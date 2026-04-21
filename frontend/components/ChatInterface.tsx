"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2, Send } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { useApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ChatInterface({ documentId }: { documentId: string }) {
  const api = useApi();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [language, setLanguage] = useState<"hindi" | "english">("hindi");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get(`/api/chat/history/${documentId}`);
        setMessages(data.messages || []);
      } catch (e) {
        // first chat — no history yet, fine
      }
    })();
  }, [api, documentId]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function send() {
    const question = input.trim();
    if (!question || sending) return;
    setSending(true);
    setMessages((m) => [...m, { role: "user", content: question }]);
    setInput("");
    try {
      const { data } = await api.post("/api/chat/ask", {
        question,
        documentId,
        language,
      });
      setMessages((m) => [...m, { role: "assistant", content: data.answer }]);
    } catch (e: any) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `⚠️ ${e?.response?.data?.detail ?? e.message}` },
      ]);
    } finally {
      setSending(false);
    }
  }

  return (
    <Card className="flex h-[600px] flex-col">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Chat — apne document se poochho</CardTitle>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value as "hindi" | "english")}
          className="rounded-md border bg-background px-2 py-1 text-sm"
        >
          <option value="hindi">Hindi</option>
          <option value="english">English</option>
        </select>
      </CardHeader>
      <CardContent className="flex flex-1 flex-col gap-3 overflow-hidden">
        <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto pr-1">
          {messages.length === 0 && (
            <p className="text-sm text-muted-foreground">
              Example: &ldquo;Eviction clause kya hai?&rdquo; ya &ldquo;Main rent kab badhaa sakta hoon?&rdquo;
            </p>
          )}
          {messages.map((m, i) => (
            <div
              key={i}
              className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                m.role === "user"
                  ? "ml-auto bg-primary text-primary-foreground"
                  : "bg-muted"
              }`}
            >
              <ReactMarkdown>{m.content}</ReactMarkdown>
            </div>
          ))}
          {sending && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin" /> Soch raha hoon…
            </div>
          )}
        </div>
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Apna sawaal likhein…"
            rows={2}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
          />
          <Button onClick={send} disabled={sending || !input.trim()} size="icon">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
