'use client'
import Image from "next/image";
import Link from "next/link";
import { useEffect } from "react";


export default function Home() {

  useEffect(() => {
    (
      async () => {
        const response = await fetch(
          'http://127.0.0.1:8000/auth/user2', {method: 'GET', credentials: "include"})
        const content = await response.json()
        console.log(content)
      }
    )()
  })


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