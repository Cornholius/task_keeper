import { host } from "@/config.json"


export default async function RegisterRequest(data) {
    console.log('data: ', data)
    const request = await fetch(
        host + "auth/register",
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