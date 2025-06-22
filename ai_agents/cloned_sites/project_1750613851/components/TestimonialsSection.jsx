;

export default function TestimonialsSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
          What Our Customers Say
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-gray-100 rounded-lg p-8 shadow-md">
            <p className="text-gray-700 text-lg mb-4">
              "With Next.js, we now consistently average 0.09 or lower for Cumulative Layout Shift, placing our site in the top tier for user experience and Core Web Vitals."
            </p>
            <div className="flex items-center">
              <img src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=80&h=80&fit=crop" alt="Notion Logo" className="w-12 h-12 rounded-full mr-4" />
              <div>
                <p className="font-bold text-gray-900">Notion</p>
                <p className="text-gray-600 text-sm">Senior Software Engineer, Frontend</p>
              </div>
            </div>
          </div>
          <div className="bg-gray-100 rounded-lg p-8 shadow-md">
            <p className="text-gray-700 text-lg mb-4">
              "Our UI for Frame.io responds to user input within 100ms and all animations run at a consistent 60fps with Next.js."
            </p>
            <div className="flex items-center">
              <img src="https://images.unsplash.com/photo-1541364983-7661220839f7?w=80&h=80&fit=crop" alt="Adobe Logo" className="w-12 h-12 rounded-full mr-4" />
              <div>
                <p className="font-bold text-gray-900">Adobe</p>
                <p className="text-gray-600 text-sm">Charlton Roberts, Product Engineering</p>
              </div>
            </div>
          </div>
          <div className="bg-gray-100 rounded-lg p-8 shadow-md">
            <p className="text-gray-700 text-lg mb-4">
              "Next.js has been a game-changer for our agency work and team collaboration. Its powerful features have allowed us to build high-performance websites quickly and efficiently like never before."
            </p>
            <div className="flex items-center">
              <img src="https://images.unsplash.com/photo-1517849845537-4d257e12907b?w=80&h=80&fit=crop" alt="Wunderman Thompson Logo" className="w-12 h-12 rounded-full mr-4" />
              <div>
                <p className="font-bold text-gray-900">WUNDERMAN THOMPSON</p>
                <p className="text-gray-600 text-sm">Daniel Lopez, Frontend Developer</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}