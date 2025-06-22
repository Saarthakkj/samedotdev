

export default function FoundationSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">
          Built on a foundation of fast, production-grade tooling
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-gray-100 rounded-lg p-6 shadow-md">
            <div className="flex items-center mb-4">
              {/* <ReactIcon className="w-6 h-6 text-blue-500 mr-2" /> */}
              <h3 className="text-lg font-medium text-gray-900">React</h3>
            </div>
            <p className="text-gray-600 text-base">
              The library for web and native user interfaces. Next.js is built on
              the latest React features, including Server Components and Actions.
            </p>
          </div>
          <div className="bg-gray-100 rounded-lg p-6 shadow-md">
            <div className="flex items-center mb-4">
              <img src="/turbopack-icon.svg" alt="Turbopack Icon" className="w-6 h-6 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">Turbopack</h3>
            </div>
            <p className="text-gray-600 text-base">
              An incremental bundler optimized for JavaScript and TypeScript,
              written in Rust and built into Next.js.
            </p>
          </div>
          <div className="bg-gray-100 rounded-lg p-6 shadow-md">
            <div className="flex items-center mb-4">
              <img src="/speedy-web-compiler-icon.svg" alt="Speedy Web Compiler Icon" className="w-6 h-6 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">
                Speedy Web Compiler
              </h3>
            </div>
            <p className="text-gray-600 text-base">
              An extensible Rust based platform for the next generation of fast
              developer tools, and can be used for both compilation and
              minification.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}