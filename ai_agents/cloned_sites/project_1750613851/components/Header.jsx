import { Menu, Search } from 'lucide-react';;

export default function Header() {
  return (
    <header className="bg-white py-4 px-6 md:px-8 lg:px-12">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <img
            src="/vercel.svg"
            alt="Vercel Logo"
            className="h-8 w-auto"
          /> {/* Replace with actual Vercel logo */}
          <span className="ml-4 text-xl font-bold text-gray-800">NEXT.js</span>
        </div>
        <div className="flex items-center space-x-4">
          <nav className="hidden md:flex space-x-6">
            <a href="#" className="text-gray-600 hover:text-gray-800">Showcase</a>
            <a href="#" className="text-gray-600 hover:text-gray-800">Docs</a>
            <a href="#" className="text-gray-600 hover:text-gray-800">Blog</a>
            <a href="#" className="text-gray-600 hover:text-gray-800">Templates</a>
            <a href="#" className="text-gray-600 hover:text-gray-800">Enterprise</a>
          </nav>
          <div className="relative">
            <Search className="w-6 h-6 text-gray-600 cursor-pointer" />
          </div>
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Deploy
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded">
            Learn
          </button>
          <button className="md:hidden">
            <Menu className="w-6 h-6 text-gray-600" />
          </button>
        </div>
      </div>
    </header>
  );
}