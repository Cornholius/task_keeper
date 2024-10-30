'use client'
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from 'next/navigation'
import IsAuthenticated from '@/services/IsAuthenticated'
import Logout from "@/services/Logout";
import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import TaskDesk from "@/components/TaskDesk";


export default function Home() {

  const router = useRouter()
  const [userName, setUserName] = useState()

  useEffect(
    () => {
      async function CheckAuth() {
        const resp = await IsAuthenticated()
        if (resp) { setUserName(resp.name) }
        else { router.push('auth/login') }
      }
      CheckAuth()
    },
    [])

  return (
    <section className="h-screen w-screen">
      <Header />
      <Sidebar />
      <TaskDesk />
      
      
      
      {/* <div>
        <div className="text-white m-8">{userName} <Link className="text-white m-8" href={'auth/login'} onClick={Logout}>Выход</Link></div>
        <Link href={'/auth/login'} className="text-white mt-8">Логин</Link>
      </div> */}

    </section>
  );
}