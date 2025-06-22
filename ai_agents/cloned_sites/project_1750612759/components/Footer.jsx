import { X,Github } from 'lucide-react';;

export default function Footer() {
  return (
    <footer className="bg-white py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2">
            <img src="/vercel-logo.svg" alt="Vercel Logo" className="h-8" /> {/* Replace with actual logo */}
            <p className="text-gray-500 mt-4 text-sm">© 2025 Vercel, Inc.</p>
          </div>
          <div className="space-y-4">
            <h3 className="text-gray-700 text-lg font-medium">Resources</h3>
            <ul className="text-gray-500">
              <li><a href="#">Docs</a></li>
              <li><a href="#">Support Policy</a></li>
              <li><a href="#">Learn</a></li>
              <li><a href="#">Showcase</a></li>
              <li><a href="#">Blog</a></li>
              <li><a href="#">Team</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-gray-700 text-lg font-medium">More</h3>
            <ul className="text-gray-500">
              <li><a href="#">Next.js Commerce</a></li>
              <li><a href="#">Contact Sales</a></li>
              <li><a href="#">Community</a></li>
              <li><a href="#">GitHub</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-gray-700 text-lg font-medium">Legal</h3>
            <ul className="text-gray-500">
              <li><a href="#">Privacy Policy</a></li>
            </ul>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-500 hover:text-gray-700">
                <Github className="w-6 h-6" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}