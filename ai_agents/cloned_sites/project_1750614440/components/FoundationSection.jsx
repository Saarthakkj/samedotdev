import Image from 'next/image';

export default function FoundationSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">
          Built on a foundation of fast, production-grade tooling
        </h2>
        <p className="mt-4 text-lg text-gray-600">
          Next.js is built with speed and developer experience in mind.
        </p>
      </div>
      <div className="mt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-gray-100 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">React</h3>
          <p className="text-gray-600">
            The library for web and native user interfaces. Next.js is built on the latest React features, including Server Components and Actions.
          </p>
        </div>
        <div className="bg-gray-100 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Turbopack</h3>
          <p className="text-gray-600">
            An incremental bundler optimized for JavaScript and TypeScript, written in Rust and built into Next.js.
          </p>
        </div>
        <div className="bg-gray-100 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Speedy Web Compiler</h3>
          <p className="text-gray-600">
            An extensible Rust based platform for the next generation of fast developer tools, and can be used for both compilation and minification.
          </p>
        </div>
      </div>
    </section>
  );
}