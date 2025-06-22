export default function HeroSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
          The React Framework for the Web
        </h1>
        <p className="mt-4 text-lg text-gray-600 sm:text-xl md:text-2xl">
          Used by some of the world's largest companies, Next.js enables you to create high-quality web applications with the power of React components.
        </p>
        <div className="mt-8 flex justify-center space-x-4">
          <button className="inline-flex items-center px-6 py-3 text-lg font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Get Started
          </button>
          <button className="inline-flex items-center px-6 py-3 text-lg font-medium text-blue-600 border border-blue-600 rounded-md hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Learn Next.js
          </button>
        </div>
        <img
          src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&h=1080&fit=crop"
          alt="Hero Image"
          className="mt-12 w-full rounded-lg shadow-lg"
        />
      </div>
    </section>
  );
}