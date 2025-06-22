import { Mail, Globe, X, Github } from 'lucide-react';;

export default function Footer() {
  return (
    <footer className="bg-fafafa text-6a6f66 py-12">
      <div className="container mx-auto px-4 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-8">
        <div>
          <svg width="70" height="26" viewBox="0 0 70 26" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M39.349 24.896c1.141 0 1.784-.685 1.784-1.676 0-.962-.617-1.616-1.721-1.616h-2.961v3.292h2.898zM38.777 21.406c.938 0 1.499-.616 1.499-1.372 0-.756-.566-1.372-1.499-1.372h-2.589v2.744h2.589zM43.946 24.896c1.735 0 2.664-1.539 2.664-3.413 0-1.874-.929-3.413-2.664-3.413-1.735 0-2.664 1.539-2.664 3.413 0 1.874.929 3.413 2.664 3.413zm0-5.626c1.021 0 1.54 1.007 1.54 2.213 0 1.206-.519 2.213-1.54 2.213-1.021 0-1.54-1.007-1.54-2.213 0-1.206.519-2.213 1.54-2.213zM48.898 24.896c1.141 0 1.784-.685 1.784-1.676 0-.962-.617-1.616-1.721-1.616h-2.961v3.292h2.898zM48.326 21.406c.938 0 1.499-.616 1.499-1.372 0-.756-.566-1.372-1.499-1.372h-2.589v2.744h2.589zM56.262 24.896c1.552 0 2.315-1.007 2.315-2.338 0-1.331-.763-2.338-2.315-2.338-1.552 0-2.315 1.007-2.315 2.338 0 1.331.763 2.338 2.315 2.338zm0-4.426c.938 0 1.423.616 1.423 1.088 0 .471-.485 1.088-1.423 1.088-.938 0-1.423-.616-1.423-1.088 0-.471.485-1.088 1.423-1.088zM64.766 24.896c1.141 0 1.784-.685 1.784-1.676 0-.962-.617-1.616-1.721-1.616h-2.961v3.292h2.898zM64.194 21.406c.938 0 1.499-.616 1.499-1.372 0-.756-.566-1.372-1.499-1.372h-2.589v2.744h2.589zM68.71 19.076v5.82h-2.047v-5.82h2.047zM69.798 13.426c0 2.858-2.355 5.214-5.213 5.214-2.858 0-5.214-2.356-5.214-5.214 0-2.858 2.356-5.214 5.214-5.214 2.858 0 5.213 2.356 5.213 5.214zm-2.047 0c0-1.744-1.422-3.166-3.166-3.166-1.744 0-3.166 1.422-3.166 3.166 0 1.744 1.422 3.166 3.166 3.166 1.744 0 3.166-1.422 3.166-3.166zM34.883 24.896v-6.762l4.897 6.762h2.11v-19.94h-2.095v12.743l-4.897-12.743h-2.11v19.94h2.095zM28.495 19.076v5.82h-2.047v-5.82h2.047zM29.584 13.426c0 2.858-2.355 5.214-5.213 5.214-2.858 0-5.214-2.356-5.214-5.214 0-2.858 2.356-5.214 5.214-5.214 2.858 0 5.213 2.356 5.213 5.214zm-2.047 0c0-1.744-1.422-3.166-3.166-3.166-1.744 0-3.166 1.422-3.166 3.166 0 1.744 1.422 3.166 3.166 3.166 1.744 0 3.166-1.422 3.166-3.166zM2.047 19.076v5.82h-2.047v-5.82h2.047zM3.136 13.426c0 2.858-2.355 5.214-5.213 5.214-2.858 0-5.214-2.356-5.214-5.214 0-2.858 2.356-5.214 5.214-5.214 2.858 0 5.213 2.356 5.213 5.214zm-2.047 0c0-1.744-1.422-3.166-3.166-3.166-1.744 0-3.166 1.422-3.166 3.166 0 1.744 1.422 3.166 3.166 3.166 1.744 0 3.166-1.422 3.166-3.166z" fill="#000"/>
          </svg>
          <p className="mt-4 text-sm">&copy; 2025 Vercel, Inc.</p>
        </div>

        <div>
          <h6 className="font-bold mb-2">Resources</h6>
          <ul className="text-sm space-y-2">
            <li><a href="#" className="hover:underline">Docs</a></li>
            <li><a href="#" className="hover:underline">Support Policy</a></li>
            <li><a href="#" className="hover:underline">Learn</a></li>
            <li><a href="#" className="hover:underline">Showcase</a></li>
            <li><a href="#" className="hover:underline">Blog</a></li>
            <li><a href="#" className="hover:underline">Team</a></li>
            <li><a href="#" className="hover:underline">Analytics</a></li>
            <li><a href="#" className="hover:underline">Next.js Conf</a></li>
            <li><a href="#" className="hover:underline">Previews</a></li>
          </ul>
        </div>

        <div>
          <h6 className="font-bold mb-2">More</h6>
          <ul className="text-sm space-y-2">
            <li><a href="#" className="hover:underline">Next.js Commerce</a></li>
            <li><a href="#" className="hover:underline">Contact Sales</a></li>
            <li><a href="#" className="hover:underline">Community</a></li>
            <li><a href="#" className="hover:underline">GitHub</a></li>
            <li><a href="#" className="hover:underline">Releases</a></li>
            <li><a href="#" className="hover:underline">Telemetry</a></li>
            <li><a href="#" className="hover:underline">Governance</a></li>
          </ul>
        </div>

        <div>
          <h6 className="font-bold mb-2">About Vercel</h6>
          <ul className="text-sm space-y-2">
            <li><a href="#" className="hover:underline">Next.js + Vercel</a></li>
            <li><a href="#" className="hover:underline">Open Source Software</a></li>
            <li><a href="#" className="hover:underline">GitHub</a></li>
            <li><a href="#" className="hover:underline">Bluesky</a></li>
            <li><a href="#" className="hover:underline">X</a></li>
          </ul>
        </div>

        <div>
          <h6 className="font-bold mb-2">Legal</h6>
          <ul className="text-sm space-y-2">
            <li><a href="#" className="hover:underline">Privacy Policy</a></li>
          </ul>
          <div className="mt-4">
            <h6 className="font-bold mb-2">Subscribe to our newsletter</h6>
            <p className="text-sm">Stay updated on new releases and features, guides, and case studies.</p>
            <div className="mt-2 flex">
              <input type="email" placeholder="you@domain.com" className="border rounded-l py-2 px-3 w-full focus:outline-none text-black" />
              <button className="bg-ededec text-141414 py-2 px-4 rounded-r hover:bg-d8d8d7 focus:outline-none">Subscribe</button>
            </div>
          </div>
          <div className="mt-4 flex space-x-4">
            <a href="#" className="hover:text-838885"><Github className="w-5 h-5" /></a>
            <a href="#" className="hover:text-838885"><Globe className="w-5 h-5" /></a>
            <a href="#" className="hover:text-838885"><X className="w-5 h-5" /></a>
          </div>
        </div>
      </div>
    </footer>
  );
}