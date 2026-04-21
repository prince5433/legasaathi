"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { UserButton } from "@clerk/nextjs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
      <nav className="border-b">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="text-xl font-bold">
            LegalSaathi AI
          </Link>
          <UserButton afterSignOutUrl="/" />
        </div>
      </nav>

      <main className="container space-y-8 py-8">
        <section>
          <h1 className="text-3xl font-bold">Naya document upload karein</h1>
          <p className="mt-2 text-muted-foreground">
            PDF chunk ho kar Qdrant mein jaayega, entities Neo4j mein, aur Hindi summary + risks milenge.
          </p>
          <div className="mt-6">
            <DocumentUploader onUploaded={onUploaded} />
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold">Tumhare documents</h2>
          {loading ? (
            <p className="mt-4 text-sm text-muted-foreground">Loading…</p>
          ) : docs.length === 0 ? (
            <p className="mt-4 text-sm text-muted-foreground">Abhi koi document nahi hai.</p>
          ) : (
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              {docs.map((d) => (
                <Link key={d._id} href={`/dashboard/${d._id}`}>
                  <Card className="transition-colors hover:bg-muted/40">
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between text-base">
                        <span className="truncate">{d.fileName}</span>
                        <span className="rounded-full bg-muted px-3 py-1 text-xs uppercase">
                          {d.docType || "other"}
                        </span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="line-clamp-3 text-sm text-muted-foreground">
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
