export default async function IsAuthenticated(router, token) {
    const { host } = require('@/config.json')
    const request = await fetch(
        host + 'auth/user',
        {
            headers: { "Authorization": "Bearer " + token },
            credentials: "include",
        }
    ).then(response => response.json())
    if (!request['is_active']) {
        router.push('/auth/login')
    }
}