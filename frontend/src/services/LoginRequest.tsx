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
    })
  const response = await request.json()

  if (request.ok) {
    localStorage.setItem('Keeper', response.access_token)
    return request.ok
  }
  else { return "Неправильный логин или пароль" }
  // else { return response.detail }
}