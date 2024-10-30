export default async function Test(router, token) {
    const { host } = require('@/config.json')
    const request = await fetch(
        host + 'auth/test',
        {
            headers: { "Authorization": "Bearer " + token },
            credentials: "include",
        }
    ).then(response => response.json())
    console.log(request)
}