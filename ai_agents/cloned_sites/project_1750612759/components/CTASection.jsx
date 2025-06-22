import { ArrowRight } from 'lucide-react';

export default function CTASection() {
  return (
    <section className="py-20 bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Ready to get started?
        </h2>
        <p className="mt-4 text-lg text-gray-600">
          For performance, efficiency and developer experience. Next.js is trusted by some of the biggest names on the web.
        </p>
        <div className="mt-8 flex justify-center">
          <button className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10">
            View the Next.js Showcase <ArrowRight className="ml-3 h-5 w-5" />
          </button>
        </div>
      </div>
    </section>
  );
}