import { TrendingUp } from 'lucide-react';;

export default function Hero() {
  return (
    <section className="bg-gray-100 py-20">
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-5xl font-bold mb-4 text-gray-800">
          Welcome to the Next.js Landing Page
        </h1>
        <p className="text-xl mb-8 text-gray-600">
          Build amazing web applications with the power of Next.js.
        </p>
        <div className="flex flex-col md:flex-row justify-center space-y-4 md:space-y-0 md:space-x-8">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg">
            Get Started
          </button>
          <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-3 px-6 rounded-lg">
            Learn More
          </button>
        </div>
        <div className="mt-12">
          <TrendingUp className="mx-auto w-16 h-16 text-blue-500 animate-spin" />
        </div>
      </div>
    </section>
  );
}