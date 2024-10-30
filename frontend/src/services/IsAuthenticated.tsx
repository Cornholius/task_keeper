
import { host as host } from '@/config.json'

export default async function IsAuthenticated() {
    const request = await fetch(
        host + 'auth/user',
        {
            headers: { "Authorization": "Bearer " + localStorage.getItem('Keeper') },
            credentials: "include",
        }
    )
    const response = await request.json()
    console.log(request.ok)
    if (request.ok) { return { "name": response.name, "email": response.email } }
}