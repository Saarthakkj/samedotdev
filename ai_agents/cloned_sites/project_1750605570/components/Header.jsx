import { Search, Menu } from 'lucide-react';;

export default function Header() {
  return (
    <header className="bg-fafafa text-2a2a29 py-4 shadow-md">
      <div className="container mx-auto px-4 flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="font-bold text-xl">
          <img src="https://assets.vercel.com/image/upload/v1677845815/nextjs/assets/components/icons/nextjs-logo.svg" alt="Next.js Logo" className="h-6 inline-block mr-2" />
          NEXT.js
        </a>

        {/* Navigation Links (Hidden on smaller screens) */}
        <nav className="hidden md:flex space-x-6">
          <a href="/showcase" className="hover:text-f3ac6c">Showcase</a>
          <a href="/docs" className="hover:text-f3ac6c">Docs</a>
          <a href="/blog" className="hover:text-f3ac6c">Blog</a>
          <a href="/templates" className="hover:text-f3ac6c">Templates</a>
          <a href="/enterprise" className="hover:text-f3ac6c">Enterprise</a>
        </nav>

        {/* Search Bar and Deploy Button (Flex container on smaller screens) */}
        <div className="flex items-center space-x-4">
          {/* Search Bar (Hidden on smaller screens) */}
          <div className="hidden md:flex items-center border border-d8d8d7 rounded-md px-3 py-1">
            <Search className="w-5 h-5 text-6a6f66 mr-2" />
            <input type="text" placeholder="Search documentation..." className="bg-transparent outline-none text-sm" />
          </div>

          {/* Deploy Button */}
          <button className="bg-141414 text-fafafa py-2 px-4 rounded-md hover:bg-2a2a29 font-medium">
            ▲ Deploy
          </button>

          {/* Learn Button */}
          <button className="bg-f3ac6c text-fafafa py-2 px-4 rounded-md hover:bg-c27739 font-medium hidden md:block">
            Learn
          </button>

          {/* Mobile Menu Button (Visible on smaller screens) */}
          <button className="md:hidden">
            <Menu className="w-6 h-6" />
          </button>
        </div>
      </div>
    </header>
  );
}