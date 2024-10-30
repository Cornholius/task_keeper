"use client"
import Link from "next/link";
import React, { useState, useEffect, SyntheticEvent } from "react"
import { useRouter } from 'next/navigation'
import LoginRequest from '@/services/LoginRequest'

export default function Auth_page() {

  const ErrorMsg = ''
  const [msg, setMsg] = useState('')
  const [email, setEmail] = useState('')
  const [pass, setPass] = useState('')
  const router = useRouter();

  const Login = async (e: SyntheticEvent) => {
    e.preventDefault();
    const result = await LoginRequest(email, pass)
    if (result == true) { router.push('/main') }
    else { setMsg(result) }
  }

  return (
    <>
      <h3 className="text-3xl font-semibold tracking-[-0.015em] text-white">Вход</h3>

      <form onSubmit={Login} className="mt-6">
        <label className="select-none text-xl text-red-500">{msg}</label>
        <div className="mt-4">
          <label className="select-none text-xl text-white">Почта</label>
          <input id="email" name="email" type="email" onChange={e => setEmail(e.target.value)} className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <div className="mt-4">
          <label className="block text-xl text-white">Пароль</label>
          <input id="pass" name="pass" type="password" onChange={e => setPass(e.target.value)} className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <Link href="/auth/restore" className="text-sm text-zinc-400 hover:underline">Забыл пароль?</Link>
        <button type="submit"
          className="mt-4 w-full px-4 py-2 text-white transition-color duration-700 bg-zinc-500 rounded-md hover:bg-zinc-700">
          Войти
        </button>
      </form>

      <p className="mt-8 text-sm font-light text-center text-zinc-400">Нет аккаунта?
        <Link href="/auth/register" className="ml-2 font-medium text-white hover:underline hover:text-green-300 hover:transition hover:duration-00">Регистрация</Link>
      </p>
    </>
  );
}
