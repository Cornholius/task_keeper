import Link from "next/link";
import Logout from "@/services/Logout";
import Image from "next/image";


export default function Header(props: { user: string }) {
    return (
        <header className="absolute flex items-center justify-between top-0 left-0 w-screen h-header bg-gray-700">

            <div className="logo w-1/5"></div>

            <div className="search w-2/5 flex">
                <input className="w-full" type="text" />
                <button>Найти</button>
            </div>

            <div className="user h-header w-1/5 float-right flex items-center justify-around">
                <div className="flex items-center">
                    <Image className="bg-white/80 rounded-full p-1" src='/img/monkey6.svg' width={48} height={48} alt=""></Image>
                    <div className="text-white ml-4">{props.user}</div>
                </div>
                <Link className="text-white" href={'auth/login'} onClick={Logout}>Выход</Link>
            </div>
        </header>
    )
}