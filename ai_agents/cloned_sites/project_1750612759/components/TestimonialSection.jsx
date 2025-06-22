export default function TestimonialSection() {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">What Our Customers Say</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-gray-100 p-6 rounded-lg shadow-md">
            <p className="text-lg text-gray-700 mb-4">
              "With Next.js, we now consistently average 0.09 or lower for Cumulative Layout Shift, placing our site in the top tier for user experience and Core Web Vitals."
            </p>
            <p className="text-gray-600 font-medium">Notion</p>
            <p className="text-gray-600">Senior Software Engineer, Frontend</p>
          </div>
          <div className="bg-gray-100 p-6 rounded-lg shadow-md">
            <p className="text-lg text-gray-700 mb-4">
              "Our UI for Frame.io responds to user input within 100ms and all animations run at a consistent 60fps with Next.js."
            </p>
            <p className="text-gray-600 font-medium">Adobe</p>
            <p className="text-gray-600">Charlton Roberts, Product Engineering</p>
          </div>
          <div className="bg-gray-100 p-6 rounded-lg shadow-md">
            <p className="text-lg text-gray-700 mb-4">
              "Next.js has been a game-changer for our agency work and team collaboration. Its powerful features have allowed us to build high-performance websites quickly and efficiently like never before."
            </p>
            <p className="text-gray-600 font-medium">WUNDERMAN THOMPSON</p>
            <p className="text-gray-600">Daniel Lopes, Frontend Developer</p>
          </div>
        </div>
      </div>
    </section>
  );
}