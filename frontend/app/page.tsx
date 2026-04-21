import Link from "next/link";
import {
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/nextjs";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function LandingPage() {
  return (
    <main className="min-h-screen">
      <nav className="border-b">
        <div className="container flex h-16 items-center justify-between">
          <div className="text-xl font-bold">LegalSaathi AI</div>
          <div className="flex items-center gap-2">
            <SignedOut>
              <SignInButton mode="redirect">
                <Button variant="ghost">Sign in</Button>
              </SignInButton>
              <SignUpButton mode="redirect">
                <Button>Get started</Button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <Link href="/dashboard">
                <Button variant="outline">Dashboard</Button>
              </Link>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
          </div>
        </div>
      </nav>

      <section className="container py-20 text-center">
        <h1 className="text-5xl font-bold tracking-tight">
          India ka AI Legal Saathi
        </h1>
        <p className="mt-6 text-lg text-muted-foreground">
          Rent agreement, FIR, court notice — sab samjho free mein, Hindi mein, 24/7.
          <br />
          Vakeel ke Rs.5,000 bachao.
        </p>
        <div className="mt-10 flex justify-center gap-3">
          <SignedOut>
            <SignUpButton mode="redirect">
              <Button size="lg">Shuru karo — Free</Button>
            </SignUpButton>
            <SignInButton mode="redirect">
              <Button size="lg" variant="outline">
                Sign in
              </Button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <Link href="/dashboard">
              <Button size="lg">Dashboard kholo</Button>
            </Link>
          </SignedIn>
        </div>
      </section>

      <section className="container grid gap-6 pb-20 md:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-semibold">PDF upload</div>
            <p className="mt-2 text-sm text-muted-foreground">
              Rent agreement ya koi bhi legal PDF drag &amp; drop.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-semibold">Hindi summary + risks</div>
            <p className="mt-2 text-sm text-muted-foreground">
              5 bullet summary, risky clauses highlighted — instant.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-semibold">AI chat</div>
            <p className="mt-2 text-sm text-muted-foreground">
              Apne document ke baare mein kuch bhi poochho — AI memory yaad rakhta hai.
            </p>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}
