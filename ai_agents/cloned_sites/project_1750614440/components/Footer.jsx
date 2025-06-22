import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-gray-100 py-12">
      <div className="container mx-auto px-4">
        <div className="flex flex-wrap justify-between md:flex-row flex-col gap-8">
          <div className="w-full md:w-1/3">
            <Link href="/" className="text-xl font-bold mb-4">Vercel</Link>
            <p className="text-gray-600">
              © 2025 Vercel, Inc.
            </p>
          </div>
          <div className="w-full md:w-1/3">
            <h4 className="text-lg font-medium mb-4">Resources</h4>
            <ul className="text-gray-600">
              <li className="mb-2"><Link href="/docs">Docs</Link></li>
              <li className="mb-2"><Link href="/support">Support Policy</Link></li>
              <li className="mb-2"><Link href="/learn">Learn</Link></li>
              <li className="mb-2"><Link href="/showcase">Showcase</Link></li>
            </ul>
          </div>
          <div className="w-full md:w-1/3">
            <h4 className="text-lg font-medium mb-4">About</h4>
            <ul className="text-gray-600">
              <li className="mb-2"><Link href="/team">Team</Link></li>
              <li className="mb-2"><Link href="/analytics">Analytics</Link></li>
              <li className="mb-2"><Link href="/nextjsconf">Next.js Conf</Link></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 text-center text-gray-600">
          <p>Legal Links | Privacy Policy</p>
        </div>
      </div>
    </footer>
  );
}