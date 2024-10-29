
export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // <div className="relative flex flex-col justify-center min-h-screen overflow-hidden">
    //   <div className="bg-zinc-900 w-full p-6 m-auto rounded-md shadow-md lg:max-w-md md:max-w-md sm:max-w-md">
    //     {children}
    //   </div>
    // </div>
    <div className="bg-zinc-800/90 lg:w-1/4 md:w-1/2 sm:w-10/12 mx-auto relative flex justify-center min-h-screen overflow-hidden">
      <div className="w-3/4 m-auto lg:max-w-md md:max-w-md sm:max-w-md">
        {children}
      </div>
    </div>
  );
}
