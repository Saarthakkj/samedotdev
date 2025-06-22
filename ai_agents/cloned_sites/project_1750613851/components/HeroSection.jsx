import { TrendingUp } from 'lucide-react';;

export default function HeroSection() {
  return (
    <section className="bg-white py-20">
      <div className="container mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4 text-gray-800">The React Framework for the Web</h1>
        <p className="text-lg mb-8 text-gray-600">Used by some of the world's largest companies, Next.js enables you to create high-quality web applications with the power of React components.</p>
        <div className="flex justify-center space-x-4">
          <button className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-full">Get Started</button>
          <a href="#" className="text-orange-500 font-medium hover:underline">Learn Next.js</a>
        </div>
        <div className="mt-12">
          <div className="flex justify-center items-center">
            <span className="text-gray-500 font-mono text-sm mr-2">^</span>
            <span className="text-gray-500 font-mono text-sm">npx create-next-app@latest</span>
          </div>
        </div>
        <div className="mt-8">
          <TrendingUp className="mx-auto w-12 h-12 text-orange-500 animate-pulse"/>
        </div>
      </div>
    </section>
  );
}