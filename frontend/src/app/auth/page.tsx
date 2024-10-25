import Link from "next/link";

export default function Auth_page() {
    return (
        <div>
            <div className="relative flex flex-col justify-center min-h-screen overflow-hidden">
                <div className="bg-zinc-900 w-full p-6 m-auto rounded-md shadow-md lg:max-w-md">
                    <h3 className="text-3xl font-semibold tracking-[-0.015em] text-white">Вход</h3>
                    <form className="mt-6">
                        <div>
                            <label className="select-none text-xl text-white">Почта</label>
                            <input type="email" className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
                        </div>
                        <div className="mt-4">
                            <div>
                                <label className="block text-xl text-white">Пароль</label>
                                <input type="password" className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
                            </div>
                            <a href="#" className="text-sm text-zinc-400 hover:underline">Забыл пароль?</a>
                            <div className="mt-6">
                                <button
                                    className="w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-zinc-500 rounded-md hover:bg-purple-600 focus:outline-none focus:bg-purple-600">
                                    Войти
                                </button>
                            </div>
                        </div>
                    </form>
                    <p className="mt-8 text-sm font-light text-center text-zinc-400">Нет аккаунта? 
                        <a href="#" className="font-medium text-white hover:underline"> Регистрация</a>
                    </p>
                </div>
            </div>
        </div>
    );
}
