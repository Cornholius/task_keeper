import { useRouter } from 'next/navigation'


export default async function IsAuthenticated(router, token) {
    // const router = useRouter()
    const request = await fetch(
        'http://127.0.0.1:8000/auth/user',
        {
            headers: { "Authorization": "Bearer " + token },
            credentials: "include",
        }).then(response => response.json())
    if (!request['is_active']) {
        router.push('/auth/login')
    }
}