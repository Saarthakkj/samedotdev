import { ChevronLeft, ChevronRight } from 'lucide-react';;

export default function GettingStartedSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">Get started in seconds</h2>
        <p className="text-lg text-gray-600 mb-8">Deploy Next.js to Vercel</p>
        <div className="flex space-x-4 mb-8">
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md">Starter</button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md">Ecommerce</button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md">Blog</button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md">AI</button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md">Portfolio</button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md">SaaS</button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md">Multi-tenant App</button>
        </div>
        <p className="text-gray-600 mb-8">Vercel is a frontend cloud from the creators of Next.js, making it easy to get started with Next.js quickly. Jumpstart your Next.js development with pre-built solutions from Vercel and our community.</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-3 gap-6">
          <div className="bg-gray-100 rounded-lg p-6">
            <h3 className="text-xl font-medium text-gray-900 mb-2">Next.js Commerce Template</h3>
            <p className="text-gray-600">An all-in-one starter kit for high-performance eCommerce stores.</p>
          </div>
          <div className="bg-gray-100 rounded-lg p-6">
            <h3 className="text-xl font-medium text-gray-900 mb-2">Image Gallery Template</h3>
            <p className="text-gray-600">An image gallery powered by Cloudinary.</p>
          </div>
          <div className="bg-gray-100 rounded-lg p-6">
            <h3 className="text-xl font-medium text-gray-900 mb-2">Next.js Boilerplate</h3>
            <p className="text-gray-600">A Next.js starter from create-next-app.</p>
          </div>
        </div>
        <div className="mt-8 flex justify-center">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg">Deploy a Template on Vercel</button>
        </div>
        <div className="flex justify-between mt-8">
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md flex items-center">
            <ChevronLeft className="mr-2 h-5 w-5"/> Previous
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md flex items-center">
            Next <ChevronRight className="ml-2 h-5 w-5"/>
          </button>
        </div>
      </div>
    </section>
  );
}