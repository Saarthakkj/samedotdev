import { ChevronRight } from 'lucide-react';;

export default function HeroSection() {
  return (
    <div className="bg-gray-50 py-20">
      <div className="container mx-auto px-4">
        <div className="lg:flex items-center justify-between">
          <div className="lg:w-1/2">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-4">
              The React Framework for the Web
            </h1>
            <p className="text-lg text-gray-700 mb-8">
              Used by some of the world's largest companies, Next.js enables you to create high-quality web applications with the power of React components.
            </p>
            <div className="flex space-x-4">
              <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded">
                Get Started
              </button>
              <button className="bg-transparent hover:bg-gray-200 text-blue-500 font-bold py-3 px-6 rounded border border-blue-500 transition-colors duration-200">
                Learn Next.js
              </button>
            </div>
          </div>
          <div className="lg:w-1/2 mt-12 lg:mt-0">
            <div className="bg-gray-100 rounded-md p-4 font-mono text-sm text-gray-800">
              <span className="text-green-500">$</span> npx create-next-app@latest
            </div>
            <p className="mt-2 text-gray-500 text-sm">
              Copy and paste this command into your terminal to start a new Next.js project.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}