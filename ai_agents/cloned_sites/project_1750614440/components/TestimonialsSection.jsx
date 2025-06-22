export default function TestimonialsSection() {
  return (
    <section className="py-20 bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
          What Our Customers Say
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <TestimonialCard
            imageUrl="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=200&fit=crop"
            name="Notion"
            title="Senior Software Engineer, Frontend"
            testimonial="\With Next.js, we now consistently average 0.09 or lower for Cumulative Layout Shift, placing our site in the top tier for user experience and Core Web Vitals.\"
          />
          <TestimonialCard
            imageUrl="https://images.unsplash.com/photo-1611162617594-e4a0293a9931?w=300&h=200&fit=crop"
            name="Adobe"
            title="Charlton Roberts, Product Engineering"
            testimonial="\Our UI for Frame.io responds to user input within 100ms and all animations run at a consistent 60fps with Next.js.\"
          />
          <TestimonialCard
            imageUrl="https://images.unsplash.com/photo-1550525811-e5869dd03032?w=300&h=200&fit=crop"
            name="Wunderman Thompson"
            title="Daniel Lopes, Frontend Developer"
            testimonial="\Next.js has been a game-changer for our agency work and team collaboration. Its powerful features have allowed us to build high-performance websites quickly and efficiently like never before.\"
          />
        </div>
      </div>
    </section>
  );
}

function TestimonialCard({ imageUrl, name, title, testimonial }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <img src={imageUrl} alt={name} className="rounded-full w-16 h-16 mb-4 mx-auto" />
      <p className="text-gray-700 text-lg mb-4">{testimonial}</p>
      <h3 className="text-gray-900 text-xl font-bold mb-1">{name}</h3>
      <p className="text-gray-600 text-sm">{title}</p>
    </div>
  );
}