import { useRouter } from "next/router"
import { host } from "@/config.json"


const router = useRouter

export default async function LoginRequest(email, pass) {
  const request = await fetch(
    host + "auth/login",
    {
      method: 'POST',
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      credentials: "include",
      body: new URLSearchParams({ 'username': email, 'password': pass })
    }).then(response => response.json())

  if (request.access_token) {
    localStorage.setItem('Keeper', request['access_token'])
    return true
  }
} 