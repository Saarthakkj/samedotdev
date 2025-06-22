import { Home, User, Settings, Search , Menu} from 'lucide-react';;

export default function Header() {
  return (
    <header className="bg-white shadow-md py-4 px-6 lg:px-8">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Home className="w-6 h-6 text-gray-600" />
          <h1 className="text-xl font-bold text-gray-800">Next.js Landing Page</h1>
        </div>
        <nav className="hidden lg:flex items-center space-x-6">
          <a href="#" className="text-gray-600 hover:text-gray-800">Features</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Use Cases</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Get Started</a>
          <Search className="w-6 h-6 text-gray-600 cursor-pointer"/>
        </nav>
        <button className="lg:hidden p-2 rounded-md text-gray-600 hover:bg-gray-100">
          <Menu className="w-6 h-6" />
        </button>
      </div>
    </header>
  );
}