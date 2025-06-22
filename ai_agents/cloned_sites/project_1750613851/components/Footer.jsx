import { Globe, Mail, Phone } from 'lucide-react';;

export default function Footer() {
  return (
    <footer className="bg-gray-100 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <img src="/vercel.svg" alt="Vercel Logo" className="h-8" /> {/* Replace with actual Vercel logo */}
            <p className="text-gray-500 text-sm">© 2023 Vercel, Inc.</p>
          </div>
          <div className="space-y-4">
            <h3 className="text-gray-700 text-lg font-medium">Resources</h3>
            <ul className="text-gray-500 text-sm">
              <li><a href="#">Docs</a></li>
              <li><a href="#">Support Policy</a></li>
              <li><a href="#">Learn</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-gray-700 text-lg font-medium">More</h3>
            <ul className="text-gray-500 text-sm">
              <li><a href="#">Showcase</a></li>
              <li><a href="#">Blog</a></li>
              <li><a href="#">Team</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-gray-700 text-lg font-medium">Contact</h3>
            <ul className="flex space-x-4 text-gray-500 text-sm">
              <li>
                <a href="#">
                  <Globe className="w-5 h-5" />
                </a>
              </li>
              <li>
                <a href="#">
                  <Mail className="w-5 h-5" />
                </a>
              </li>
              <li>
                <a href="#">
                  <Phone className="w-5 h-5" />
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}