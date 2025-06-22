import { Globe, Mail, Phone } from 'lucide-react';;

export default function Footer() {
  return (
    <footer className="bg-gray-100 py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-4">Resources</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Docs</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Support Policy</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Learn</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Showcase</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-4">More</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Next.js Commerce</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Contact Sales</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Community</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">GitHub</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-4">About Vercel</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Next.js + Vercel</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Open Source Software</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">GitHub</a></li>
            </ul>
          </div>
          <div className="flex flex-col space-y-4">
            <h3 className="text-lg font-medium text-gray-800 mb-4">Contact Us</h3>
            <div className="flex items-center space-x-2">
              <Globe className="w-5 h-5 text-gray-600" />
              <a href="#" className="text-gray-600 hover:text-gray-800">vercel.com</a>
            </div>
            <div className="flex items-center space-x-2">
              <Mail className="w-5 h-5 text-gray-600" />
              <a href="mailto:info@vercel.com" className="text-gray-600 hover:text-gray-800">info@vercel.com</a>
            </div>
            <div className="flex items-center space-x-2">
              <Phone className="w-5 h-5 text-gray-600" />
              <a href="tel:+15551234567" className="text-gray-600 hover:text-gray-800">+1 555 123 4567</a>
            </div>
          </div>
        </div>
        <div className="mt-12 border-t border-gray-200 pt-8 text-center text-sm text-gray-500">
          <p>&copy; 2025 Vercel, Inc.</p>
        </div>
      </div>
    </footer>
  );
}