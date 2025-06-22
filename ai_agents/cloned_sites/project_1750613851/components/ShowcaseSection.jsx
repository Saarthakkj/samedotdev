import { Image } from 'lucide-react';;

export default function ShowcaseSection() {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto text-center">
        <h2 className="text-4xl font-bold mb-4 text-gray-800">The framework of choice when it matters</h2>
        <p className="text-lg mb-12 text-gray-600">For performance, efficiency and developer experience. Next.js is trusted by some of the biggest names on the web.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <ShowcaseCard
            image="https://images.unsplash.com/photo-1685537258455-06471aa8e432?w=400&h=300&fit=crop"
            title="Spoken Word app"
          />
          <ShowcaseCard
            image="https://images.unsplash.com/photo-1685537323089-1f8e4a687e10?w=400&h=300&fit=crop"
            title="DICE popular events"
          />
          <ShowcaseCard
            image="https://images.unsplash.com/photo-1685537388668-610d956f36e6?w=400&h=300&fit=crop"
            title="Wiki docs projects"
          />
          <ShowcaseCard
            image="https://images.unsplash.com/photo-1685537452686-71b307d8a312?w=400&h=300&fit=crop"
            title="Elevated Air Nike"
          />
          <ShowcaseCard
            image="https://images.unsplash.com/photo-1685537510475-7d95560e07f7?w=400&h=300&fit=crop"
            title="POLITICS"
          />
        </div>
        <button className="mt-12 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          View the Next.js Showcase
        </button>
      </div>
    </section>
  );
}


function ShowcaseCard({ image, title }) {
  return (
    <div className="bg-gray-100 rounded-lg shadow-md p-6">
      <Image src={image} alt={title} className="w-full h-48 object-cover rounded-t-lg mb-4" />
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 text-sm">A brief description of the showcase app.</p>
    </div>
  );
}