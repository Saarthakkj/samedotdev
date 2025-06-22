import { Home, User, Mail, Phone } from 'lucide-react';;

export default function Footer() {
  return (
    <footer className="bg-gray-100 py-8">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">About Us</h3>
            <p className="text-gray-600">Learn more about Next.js and its capabilities.</p>
            <a href="#" className="text-blue-500 hover:underline">Learn More</a>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">Quick Links</h3>
            <ul className="text-gray-600">
              <li><a href="#">Documentation</a></li>
              <li><a href="#">Blog</a></li>
              <li><a href="#">Community</a></li>
              <li><a href="#">GitHub</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">Contact Us</h3>
            <div className="flex items-center space-x-4">
              <Mail className="w-6 h-6 text-gray-600" />
              <a href="mailto:info@example.com" className="text-gray-600 hover:underline">info@example.com</a>
            </div>
            <div className="flex items-center space-x-4">
              <Phone className="w-6 h-6 text-gray-600" />
              <a href="tel:+15551234567" className="text-gray-600 hover:underline">+1 (555) 123-4567</a>
            </div>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">Follow Us</h3>
            <div className="flex items-center space-x-4">
              <a href="#" className="text-blue-500 hover:underline">
                <Home className="w-6 h-6" />
                <span className="sr-only">Home</span>
              </a>
              <a href="#" className="text-blue-500 hover:underline">
                <User className="w-6 h-6" />
                <span className="sr-only">User</span>
              </a>
            </div>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-300 pt-4 text-center text-gray-600">
          <p>&copy; {new Date().getFullYear()} Next.js Website. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}