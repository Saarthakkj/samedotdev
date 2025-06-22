
import Image from 'next/image';

export default function FeaturesSection() {
  return (
    <section className="py-20 bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl text-center mb-12">Key Features</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-white shadow-lg rounded-lg overflow-hidden">
            <Image
              src="https://images.unsplash.com/photo-1506741359872-e37f7849901f?w=300&h=200&fit=crop"
              alt="Feature 1"
              width={300}
              height={200}
              className="w-full object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-medium text-gray-900">Feature 1</h3>
              <p className="text-gray-600 mt-2">Description of Feature 1.</p>
            </div>
          </div>
          <div className="bg-white shadow-lg rounded-lg overflow-hidden">
            <Image
              src="https://images.unsplash.com/photo-1496181133206-80e8a0659371?w=300&h=200&fit=crop"
              alt="Feature 2"
              width={300}
              height={200}
              className="w-full object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-medium text-gray-900">Feature 2</h3>
              <p className="text-gray-600 mt-2">Description of Feature 2.</p>
            </div>
          </div>
          <div className="bg-white shadow-lg rounded-lg overflow-hidden">
            <Image
              src="https://images.unsplash.com/photo-1504711434965-e629c1696664?w=300&h=200&fit=crop"
              alt="Feature 3"
              width={300}
              height={200}
              className="w-full object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-medium text-gray-900">Feature 3</h3>
              <p className="text-gray-600 mt-2">Description of Feature 3.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}