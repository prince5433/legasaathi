"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { UserButton } from "@clerk/nextjs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Scale } from "lucide-react";
import { DocumentUploader, UploadResult } from "@/components/DocumentUploader";
import { useApi } from "@/lib/api";

interface DocSummary {
  _id: string;
  fileName: string;
  docType: string;
  status: string;
  summary?: string;
  createdAt?: string;
}

export default function DashboardPage() {
  const api = useApi();
  const [docs, setDocs] = useState<DocSummary[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/api/documents/list");
      setDocs(data);
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const onUploaded = useCallback(
    (_r: UploadResult) => {
      refresh();
    },
    [refresh],
  );

  return (
    <div className="min-h-screen">
      <nav className="relative z-10 border-b border-white/10 bg-slate-950/50 backdrop-blur-md">
        <div className="container mx-auto px-4 flex h-20 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
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

      <main className="container space-y-8 py-8">
        <section>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">Naya document upload karein</h1>
          <p className="mt-2 text-slate-400">
            PDF chunk ho kar Qdrant mein jaayega, entities Neo4j mein, aur Hindi summary + risks milenge.
          </p>
          <div className="mt-6">
            <DocumentUploader onUploaded={onUploaded} />
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">Tumhare documents</h2>
          {loading ? (
            <p className="mt-4 text-sm text-slate-400">Loading…</p>
          ) : docs.length === 0 ? (
            <p className="mt-4 text-sm text-slate-400">Abhi koi document nahi hai.</p>
          ) : (
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              {docs.map((d) => (
                <Link key={d._id} href={`/dashboard/${d._id}`}>
                  <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm transition-colors hover:border-amber-500/50 group">
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between text-base">
                        <span className="truncate text-white group-hover:text-amber-400 transition-colors">{d.fileName}</span>
                        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs uppercase text-slate-300 border border-slate-700">
                          {d.docType || "other"}
                        </span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="line-clamp-3 text-sm text-slate-400">
                        {d.summary || "(abhi process ho raha hai…)"}
                      </p>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
