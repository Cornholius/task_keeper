'use client'
import Image from "next/image";
import Link from "next/link";
import { useEffect } from "react";
import { useRouter } from 'next/navigation'
import IsAuthenticated from '@/services/IsAuthenticated'

export default function Home() {
  const router = useRouter();

  useEffect(() => { IsAuthenticated(router, localStorage.getItem('Keeper')) })

  return (
    <section className="h-screen flex flex-col items-center justify-center">
      <div className="mx-auto w-64">
        <Image
          aria-hidden
          src="/mountain.svg"
          alt="Window icon"
          width={256}
          height={256}
        />
      </div>
      <Link href={'/auth/login'} className="text-white mt-8">Логин</Link>
    </section>
  );
}