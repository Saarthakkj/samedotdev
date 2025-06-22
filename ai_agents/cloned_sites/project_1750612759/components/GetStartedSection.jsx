import { Minus, Plus } from 'lucide-react';;

export default function GetStartedSection() {
  return (
    <section className="py-16 bg-white">
      <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Get started in seconds</h2>
      <div className="flex justify-center mb-8">
        <div className="flex space-x-4">
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md">
            <Plus className="inline mr-2 h-4 w-4" /> Starter
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md">
            <Plus className="inline mr-2 h-4 w-4" /> Ecommerce
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md">
            <Plus className="inline mr-2 h-4 w-4" /> Blog
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md">
            <Minus className="inline mr-2 h-4 w-4" /> AI
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md">
            <Minus className="inline mr-2 h-4 w-4" /> Portfolio
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md">
            <Minus className="inline mr-2 h-4 w-4" /> SaaS
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md">
            <Minus className="inline mr-2 h-4 w-4" /> Multi-tenant App
          </button>
        </div>
      </div>
      <p className="text-gray-600 text-center mb-8">Vercel is a frontend cloud from the creators of Next.js, making it easy to get started with Next.js quickly. Jumpstart your Next.js development with pre-built solutions from Vercel and our community.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-medium text-gray-800 mb-2">Next.js Commerce</h3>
          <p className="text-gray-600">An all-in-one starter kit for high-performance e-commerce stores.</p>
        </div>
        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-medium text-gray-800 mb-2">Image Gallery</h3>
          <p className="text-gray-600">An image gallery with Cloudinary.</p>
        </div>
        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-medium text-gray-800 mb-2">Next.js Boilerplate</h3>
          <p className="text-gray-600">A Next.js starter from create-next-app.</p>
        </div>
      </div>
      <div className="flex justify-center mt-8">
        <button className="bg-black hover:bg-gray-900 text-white font-bold py-3 px-6 rounded-lg">Deploy a Template on Vercel</button>
      </div>
    </section>
  );
}