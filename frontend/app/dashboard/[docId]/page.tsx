"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import { UserButton } from "@clerk/nextjs";
import { apiUrl, useApi } from "@/lib/api";
import { SummaryCard } from "@/components/SummaryCard";
import { RiskList, Risk } from "@/components/RiskList";
import { ChatInterface } from "@/components/ChatInterface";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Scale } from "lucide-react";

interface Doc {
  _id: string;
  fileName: string;
  fileUrl: string;
  docType: string;
  status: string;
  summary: string;
  risks: Risk[];
}

function absoluteFileUrl(url: string | undefined): string | undefined {
  if (!url) return undefined;
  if (url.startsWith("/local-files/")) return `${apiUrl}${url}`;
  return url;
}

export default function DocumentDetailPage() {
  const { docId } = useParams<{ docId: string }>();
  const api = useApi();
  const [doc, setDoc] = useState<Doc | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const { data } = await api.get(`/api/documents/${docId}`);
        if (cancelled) return;
        setDoc(data);
        // Keep polling while backend is still processing the upload
        if (data.status === "processing" && !pollRef.current) {
          pollRef.current = setInterval(load, 3000);
        }
        if (data.status === "done" && pollRef.current) {
          clearInterval(pollRef.current);
          pollRef.current = null;
        }
      } catch (e: any) {
        if (cancelled) return;
        setError(e?.response?.data?.detail ?? e.message ?? "Failed to load");
      }
    }

    load();
    return () => {
      cancelled = true;
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [api, docId]);

  const pdfHref = absoluteFileUrl(doc?.fileUrl);

  return (
    <div className="min-h-screen">
      <nav className="relative z-10 border-b border-white/10 bg-slate-950/50 backdrop-blur-md">
        <div className="container mx-auto px-4 flex h-20 items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <div className="bg-slate-800/50 p-2 rounded-xl border border-slate-700/50 hidden sm:flex">
              <ArrowLeft className="w-5 h-5 text-slate-300" />
            </div>
            <div className="bg-amber-500/10 p-2 rounded-xl border border-amber-500/20">
              <Scale className="w-6 h-6 text-amber-500" />
            </div>
            <span className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              LegalSaathi<span className="text-amber-500">.</span>
            </span>
          </Link>
          <UserButton afterSignOutUrl="/" />
        </div>
      </nav>

      <main className="container py-8">
        {error && (
          <div className="rounded-md border border-destructive/40 bg-destructive/10 p-4 text-sm text-destructive">
            {error}
          </div>
        )}
        {!doc && !error && <p className="text-sm text-muted-foreground">Loading document…</p>}
        {doc && (
          <div className="grid gap-6 lg:grid-cols-5">
            <div className="space-y-6 lg:col-span-3">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">{doc.fileName}</h1>
                {pdfHref && (
                  <a href={pdfHref} target="_blank" rel="noreferrer">
                    <Button variant="outline" size="sm">
                      PDF kholein
                    </Button>
                  </a>
                )}
              </div>
              {doc.status === "processing" && (
                <div className="rounded-md border bg-muted/30 p-3 text-sm text-muted-foreground">
                  Analysis chal raha hai… 10-30 second.
                </div>
              )}
              <SummaryCard summary={doc.summary} docType={doc.docType} />
              <RiskList risks={doc.risks || []} />
            </div>
            <div className="lg:col-span-2">
              <ChatInterface documentId={doc._id} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
