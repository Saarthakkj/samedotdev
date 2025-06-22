
import Image from 'next/image';

export default function ShowcaseSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">Showcase</h2>
        <p className="mt-4 text-lg text-gray-600">
          See Next.js in action with these amazing examples.
        </p>
      </div>
      <div className="mt-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <Image
            src="https://images.unsplash.com/photo-1606787366881-60291a4f490d?w=300&h=200&fit=crop"
            alt="Example 1"
            width={300}
            height={200}
            className="object-cover w-full h-48"
          />
          <div className="p-6">
            <h3 className="text-xl font-bold text-gray-900">Example 1</h3>
            <p className="mt-2 text-gray-600">A brief description of Example 1.</p>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <Image
            src="https://images.unsplash.com/photo-1612596377479-2a5d0250038a?w=300&h=200&fit=crop"
            alt="Example 2"
            width={300}
            height={200}
            className="object-cover w-full h-48"
          />
          <div className="p-6">
            <h3 className="text-xl font-bold text-gray-900">Example 2</h3>
            <p className="mt-2 text-gray-600">A brief description of Example 2.</p>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <Image
            src="https://images.unsplash.com/photo-1553642714-0282c866102b?w=300&h=200&fit=crop"
            alt="Example 3"
            width={300}
            height={200}
            className="object-cover w-full h-48"
          />
          <div className="p-6">
            <h3 className="text-xl font-bold text-gray-900">Example 3</h3>
            <p className="mt-2 text-gray-600">A brief description of Example 3.</p>
          </div>
        </div>
      </div>
    </section>
  );
}