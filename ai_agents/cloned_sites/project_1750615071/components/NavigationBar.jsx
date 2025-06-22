'use client'
import React from 'react';
import { Home, Menu, Search } from 'lucide-react';


export default function NavigationBar() {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  return (
    <nav className="bg-white shadow-md px-6 py-4">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <Home className="w-6 h-6 text-gray-800 mr-4" />
          <h1 className="text-2xl font-bold text-gray-800">Next.js</h1>
        </div>
        <div className="hidden md:flex space-x-6">
          <a href="#" className="text-gray-600 hover:text-gray-800">Showcase</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Docs</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Blog</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Templates</a>
          <a href="#" className="text-gray-600 hover:text-gray-800">Enterprise</a>
        </div>
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-600 mr-4" />
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-md hover:bg-gray-100"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <Menu className="w-6 h-6 text-gray-600" /> : <Menu className="w-6 h-6 text-gray-600" />}
          </button>
        </div>
      </div>
      {isMenuOpen && (
        <div className="md:hidden mt-4 bg-white shadow-lg">
          <ul className="p-4">
            <li><a href="#" className="block px-4 py-2 text-gray-600 hover:bg-gray-100">Showcase</a></li>
            <li><a href="#" className="block px-4 py-2 text-gray-600 hover:bg-gray-100">Docs</a></li>
            <li><a href="#" className="block px-4 py-2 text-gray-600 hover:bg-gray-100">Blog</a></li>
            <li><a href="#" className="block px-4 py-2 text-gray-600 hover:bg-gray-100">Templates</a></li>
            <li><a href="#" className="block px-4 py-2 text-gray-600 hover:bg-gray-100">Enterprise</a></li>
          </ul>
        </div>
      )}
    </nav>
  );
}