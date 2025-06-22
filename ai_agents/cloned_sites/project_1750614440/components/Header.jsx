import Link from 'next/link';
import { Home, Search } from 'lucide-react';;

export default function Header() {
  return (
    <header className="bg-[#fcfefe] py-4 px-6 md:px-8 lg:px-12">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="flex items-center gap-2">
          <Home className="w-6 h-6 text-[#2a2a2a]" />
          <span className="text-xl font-bold text-[#2a2a2a]">Next.js</span>
        </Link>
        <div className="flex items-center gap-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search documentation..."
              className="pl-8 pr-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 w-48 md:w-64 lg:w-80"
            />
            <Search className="absolute top-1/2 left-2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          </div>
          <Link href="/deploy" className="bg-[#2a2a2a] text-white px-4 py-2 rounded-md hover:bg-gray-800">
            Deploy
          </Link>
          <Link href="/learn" className="text-[#2a2a2a] hover:underline">
            Learn
          </Link>
        </div>
      </div>
    </header>
  );
}