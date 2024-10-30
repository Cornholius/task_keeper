import Link from "next/link";


export default function Auth_page() {
  return (
    <>
      <h3 className="text-3xl font-semibold tracking-[-0.015em] text-white">Восстановление пароля</h3>

      <form className="mt-6">
        <div className="mt-4">
          <label className="select-none text-xl text-white">Адрес Вашей почты</label>
          <input type="email" className="block w-full px-4 py-2 mt-2 text-white bg-zinc-700 border rounded-md focus:border-zinc-300 focus:ring-zinc-300 focus:outline-none focus:ring focus:ring-opacity-40" />
        </div>
        <button
          className="mt-4 w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-zinc-500 rounded-md hover:bg-green-600 focus:outline-none focus:bg-green-600">
          Восстановить
        </button>
      </form>

      <p className="mt-8 text-sm font-light text-center text-zinc-400">Уже есть аккаунт?
        <Link href="/auth/login" className="ml-2 font-medium text-white hover:underline hover:text-green-300 hover:transition hover:duration-00">Войти</Link>
      </p>
    </>
  );
}
