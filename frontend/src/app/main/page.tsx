'use client'
import Image from "next/image";
import Link from "next/link";
import { useEffect } from "react";
import { useRouter } from 'next/navigation'
import IsAuthenticated from '@/services/IsAuthenticated'
import Test from '@/services/Test'

export default function Home() {
  const router = useRouter();
  useEffect(() => { IsAuthenticated(router, localStorage.getItem('Keeper')) })

  async function Test() {
    const { host } = require('@/config.json')
    const request = await fetch(
      host + 'auth/test',
      {
        headers: { "Authorization": "Bearer " + localStorage.getItem('Keeper') },
        credentials: "include",
      }
    ).then(response => response.json())
    console.log(request)
  }

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
      <button onClick={Test} className="mt-4 w-1/3 px-4 py-2 text-white transition-color duration-700 bg-zinc-500 rounded-md hover:bg-zinc-700">ololo</button>
    </section>
  );
}