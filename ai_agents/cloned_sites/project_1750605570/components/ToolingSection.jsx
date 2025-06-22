import { React } from 'react';
// import { ReactLogo } from './ReactLogo';
import { Zap } from 'lucide-react';

export default function ToolingSection() {
  return (
    <div className="bg-fafafa py-12">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-semibold text-center mb-8 text-gray-800">
          Built on a foundation of fast, production-grade tooling
        </h2>
        <div className="text-center text-gray-600 mb-8">
          Powered By
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* React Card */}
          <div className="bg-white rounded-lg shadow-md p-6 flex flex-col items-center">
            {/* React Logo */}
            {/* <ReactLogo className="w-20 h-20 mb-4 text-blue-500" /> */}
            <h3 className="text-xl font-semibold mb-2 text-gray-800">React</h3>
            <p className="text-gray-600 text-center">
              The library for web and native user interfaces. Next.js is built on the latest React features, including Server Components and Actions.
            </p>
          </div>

          {/* Turbopack Card */}
          <div className="bg-white rounded-lg shadow-md p-6 flex flex-col items-center">
            {/* Turbopack Logo (Replace with actual Turbopack component or image) */}
            <Zap className="w-20 h-20 mb-4 text-orange-500" />
            <h3 className="text-xl font-semibold mb-2 text-gray-800">Turbopack</h3>
            <p className="text-gray-600 text-center">
              An incremental bundler optimized for JavaScript and TypeScript, written in Rust and built into Next.js.
            </p>
          </div>

          {/* Speedy Web Compiler Card */}
          <div className="bg-white rounded-lg shadow-md p-6 flex flex-col items-center">
            {/* Speedy Web Compiler Logo (Replace with actual Speedy Web Compiler component or image) */}
            <Zap className="w-20 h-20 mb-4 text-green-500" />
            <h3 className="text-xl font-semibold mb-2 text-gray-800">Speedy Web Compiler</h3>
            <p className="text-gray-600 text-center">
              An extensible Rust based platform for the next generation of fast developer tools, and can be used for both compilation and minification.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}