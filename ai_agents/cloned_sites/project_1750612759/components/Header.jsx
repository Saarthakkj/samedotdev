import { Search } from 'lucide-react';;

export default function Header() {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-6 flex justify-between items-center">
        <img src="https://via.placeholder.com/150" alt="Next.js Logo" className="h-8" /> {/* Replace with actual logo */}
        <nav className="flex space-x-6">
          <a href="#" className="text-gray-700 hover:text-gray-900">Showcase</a>
          <a href="#" className="text-gray-700 hover:text-gray-900">Docs</a>
          <a href="#" className="text-gray-700 hover:text-gray-900">Blog</a>
          <a href="#" className="text-gray-700 hover:text-gray-900">Templates</a>
          <a href="#" className="text-gray-700 hover:text-gray-900">Enterprise</a>
        </nav>
        <div className="relative">
          <input type="text" placeholder="Search documentation..." className="pl-8 pr-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 w-48" />
          <Search className="absolute top-1/2 left-2 -translate-y-1/2 w-4 h-4 text-gray-500" />
        </div>
        <button className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">⬆️ Deploy</button>
      </div>
    </header>
  );
}