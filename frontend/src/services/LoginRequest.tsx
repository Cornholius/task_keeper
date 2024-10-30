import { host as path} from "@/config.json"


export default async function LoginRequest(email: string, pass: string) {
  const request = await fetch(
    path + "auth/login",
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
}