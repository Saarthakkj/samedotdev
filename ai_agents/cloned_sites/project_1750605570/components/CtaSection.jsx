import { ChevronRight } from 'lucide-react';;

export default function CtaSection() {
  return (
    <div className="bg-fafafa py-20">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-semibold text-gray-800 mb-4">
          For performance, efficiency and developer experience.
        </h2>
        <p className="text-gray-600 text-lg mb-8">
          Next.js is trusted by some of the biggest names on the web.
        </p>
        <button className="bg-gray-800 hover:bg-gray-900 text-white font-bold py-3 px-6 rounded-md inline-flex items-center">
          <span>View the Next.js Showcase</span>
          <ChevronRight className="w-5 h-5 ml-2" />
        </button>
      </div>
    </div>
  );
}