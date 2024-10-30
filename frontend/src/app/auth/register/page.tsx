"use client"
import Link from "next/link";
import React, { useState, useEffect, SyntheticEvent } from "react"
import { useRouter } from 'next/navigation'
import RegisterRequest from '@/services/RegisterRequest'
import LoginRequest from "@/services/LoginRequest";

export default function Auth_page() {
  const [email, setEmail] = useState('')
  const [pass, setPass] = useState('')
  const [pass2, setPass2] = useState('')
  const [name, setName] = useState('')
  const [lastname, setLastName] = useState('')
  const [msg, setMsg] = useState()
  const router = useRouter();

  const Register = async (e: SyntheticEvent) => {
    e.preventDefault();
    const data = {
      "email": email,
      "password": pass,
      "name": name
    }
    if (lastname) { data.name = name + ' ' + lastname }
    if (pass == pass2) { setMsg(await RegisterRequest(data)) }
    if (msg == true) {
      await LoginRequest(email, pass)
      router.push('/main')
    }
  }

  return (
    <>
      <h3 className="text-3xl font-semibold tracking-[-0.015em] text-white">Регистрация</h3>

      <form onSubmit={Register} className="mt-6">
        <label className="select-none text-xl text-red-500">{msg}</label>
        <div className="mt-4">
          <label className="select-none text-xl text-white">Почта</label>
          <input id="email" name="email" type="email" onChange={e => setEmail(e.target.value)} className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <div className="mt-4">
          <label className="select-none text-xl text-white">Имя</label>
          <input id="name" name="name" type="text" onChange={e => setName(e.target.value)} className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <div className="mt-4">
          <label className="select-none text-xl text-white">Фамилия <span className="text-sm text-zinc-400">не обязательно</span></label>
          <input id="lastname" name="lastname" type="text" onChange={e => setLastName(e.target.value)} className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <div className="mt-4">
          <label className="block text-xl text-white">Пароль</label>
          <input id="pass" name="pass" type="password" onChange={e => setPass(e.target.value)} className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <div className="mt-4">
          <label className="block text-xl text-white">Пароль ещё раз</label>
          <input id="pass2" name="pass2" type="password" onChange={e => setPass2(e.target.value)} className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <button type="submit" className="mt-8 w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-zinc-500 rounded-md hover:bg-green-600 focus:outline-none focus:bg-green-600">
          Регистрация
        </button>
      </form>

      <p className="mt-8 text-sm font-light text-center text-zinc-400">Уже есть аккаунт?
        <Link href="/auth/login" className="ml-2 font-medium text-white hover:underline hover:text-green-300 hover:transition hover:duration-00">Войти</Link>
      </p>
    </>

  );
}