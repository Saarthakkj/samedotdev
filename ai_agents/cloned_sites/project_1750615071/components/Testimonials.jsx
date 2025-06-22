import { Star } from 'lucide-react';;

export default function Testimonials() {
  const testimonials = [
    {
      quote: "With Next.js, we now consistently average 0.09 or lower for Cumulative Layout Shift, placing our site in the top tier for user experience and Core Web Vitals.",
      author: "Notion",
      title: "Senior Software Engineer, Frontend"
    },
    {
      quote: "Our UI for Frame.io responds to user input within 100ms and all animations run at a consistent 60fps with Next.js.",
      author: "Adobe",
      title: "Charlton Roberts, Product Engineering"
    },
    {
      quote: "Next.js has been a game-changer for our agency work and team collaboration. Its powerful features have allowed us to build high-performance websites quickly and efficiently like never before.",
      author: "WUNDERMAN THOMPSON",
      title: "Daniel Lopes, Frontend Developer"
    },
  ];

  return (
    <section className="py-12">
      <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">Testimonials</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {testimonials.map((testimonial, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-700 text-lg mb-4">{testimonial.quote}</p>
            <div className="flex items-center">
              <Star className="w-6 h-6 text-yellow-400 mr-2" />
              <div>
                <p className="font-medium text-gray-900">{testimonial.author}</p>
                <p className="text-gray-600 text-sm">{testimonial.title}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}