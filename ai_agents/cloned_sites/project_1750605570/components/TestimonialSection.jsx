import { Star } from 'lucide-react';;

export default function TestimonialSection() {
  return (
    <div className="bg-fafafa py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-f3ac6c font-semibold tracking-wide uppercase">Testimonials</h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-2a2a29 sm:text-4xl">
            What people are saying
          </p>
          <p className="mt-4 max-w-2xl text-xl text-6a6f66 lg:mx-auto">
            Hear from our satisfied customers and see how Next.js has helped them achieve their goals.
          </p>
        </div>

        <div className="mt-10">
          <div className="md:grid md:grid-cols-3 md:gap-8">

            {/* Testimonial Card 1 */}
            <div className="mt-6 md:mt-0">
              <div className="flex flex-col h-full bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="p-5 flex-grow">
                  <div className="flex items-center justify-between">
                    <img
                      className="h-8 w-auto"
                      src="https://images.unsplash.com/photo-1554151228-14d9def656e4?w=32&h=32&fit=crop"
                      alt="Company Logo"
                    />
                    <div className="flex items-center">
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c" />
                    </div>
                  </div>
                  <p className="mt-4 text-lg leading-relaxed text-2a2a29">
                    &ldquo;With Next.js, we now consistently average 0.09 or lower for Cumulative Layout Shift, placing our site in the top tier for user experience and Core Web Vitals.&rdquo;
                  </p>
                </div>
                <div className="px-5 py-4 bg-ededec">
                  <p className="text-sm font-medium text-2a2a29">N Notion</p>
                  <p className="text-sm text-6a6f66">Senior Software Engineer, Frontend</p>
                </div>
              </div>
            </div>

            {/* Testimonial Card 2 */}
            <div className="mt-6 md:mt-0">
              <div className="flex flex-col h-full bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="p-5 flex-grow">
                  <div className="flex items-center justify-between">
                    <img
                      className="h-8 w-auto"
                      src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=32&h=32&fit=crop"
                      alt="Company Logo"
                    />
                    <div className="flex items-center">
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c" />
                    </div>
                  </div>
                  <p className="mt-4 text-lg leading-relaxed text-2a2a29">
                    &ldquo;Our UI for Frame.io responds to user input within 100ms and all animations run at a consistent 60fps with Next.js.&rdquo;
                  </p>
                </div>
                <div className="px-5 py-4 bg-ededec">
                  <p className="text-sm font-medium text-2a2a29">Adobe</p>
                  <p className="text-sm text-6a6f66">Charlton Roberts, Product Engineering</p>
                </div>
              </div>
            </div>

            {/* Testimonial Card 3 */}
            <div className="mt-6 md:mt-0">
              <div className="flex flex-col h-full bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="p-5 flex-grow">
                  <div className="flex items-center justify-between">
                    <img
                      className="h-8 w-auto"
                      src="https://images.unsplash.com/photo-1534528741702-a0c87c2e3f49?w=32&h=32&fit=crop"
                      alt="Company Logo"
                    />
                    <div className="flex items-center">
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c mr-1" />
                      <Star className="h-5 w-5 text-f3ac6c" />
                    </div>
                  </div>
                  <p className="mt-4 text-lg leading-relaxed text-2a2a29">
                    &ldquo;Next.js has been a game-changer for our agency work and team collaboration. Its powerful features have allowed us to build high-performance websites quickly and efficiently like never before.&rdquo;
                  </p>
                </div>
                <div className="px-5 py-4 bg-ededec">
                  <p className="text-sm font-medium text-2a2a29">WUNDERMAN THOMPSON</p>
                  <p className="text-sm text-6a6f66">Daniel Lopes, Frontend Developer</p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}