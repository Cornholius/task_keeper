import { host as path } from "@/config.json"


export default async function RegisterRequest(data: { email: string; password: string; name: string }) {
    const request = await fetch(
        path + "auth/register",
        {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                "email": data.email,
                "password": data.password,
                "name": data.name
            })
        })
    const msg = await request.json()
    if (!request.ok) { return msg.detail }
    else { return request.ok }
}