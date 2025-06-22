;

export default function FrameworkSection() {
  return (
    <section className="py-20 bg-white">
      <h2 className="text-3xl font-bold text-gray-800 text-center mb-10">The framework of choice when it matters</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto px-4">
        <div className="bg-gray-100 rounded-lg shadow-md p-6">
          <img src="https://images.unsplash.com/photo-1596508533583-7b2f247c5f76?w=300&h=200&fit=crop" alt="Spoken Word" className="mb-4 rounded-lg" />
          <h3 className="text-lg font-medium text-gray-800 mb-2">Effortless listening</h3>
        </div>
        <div className="bg-gray-100 rounded-lg shadow-md p-6">
          <img src="https://images.unsplash.com/photo-1516468878394-8c2c0204b323?w=300&h=200&fit=crop" alt="Dice" className="mb-4 rounded-lg" />
          <h3 className="text-lg font-medium text-gray-800 mb-2">Popular Events in San Francisco, CA</h3>
        </div>
        <div className="bg-gray-100 rounded-lg shadow-md p-6">
          <img src="https://images.unsplash.com/photo-1593642634315-48e58216f5b9?w=300&h=200&fit=crop" alt="Wiki" className="mb-4 rounded-lg" />
          <h3 className="text-lg font-medium text-gray-800 mb-2">Your wiki, docs, & projects. Together.</h3>
        </div>
        <div className="bg-gray-100 rounded-lg shadow-md p-6">
          <img src="https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=300&h=200&fit=crop" alt="Elevated Air" className="mb-4 rounded-lg" />
        </div>
      </div>
    </section>
  );
}