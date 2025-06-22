import { Check } from 'lucide-react';;

export default function ShowcaseSection() {
  const showcaseItems = [
    {
      image: 'https://images.unsplash.com/photo-1618773928122-7d162f4d2606?w=300&h=200&fit=crop&auto=format',
      title: 'Website 1',
      description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    },
    {
      image: 'https://images.unsplash.com/photo-1620799023488-d46b40325a0c?w=300&h=200&fit=crop&auto=format',
      title: 'Website 2',
      description: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    },
    {
      image: 'https://images.unsplash.com/photo-1612510773433-a4d37916446c?w=300&h=200&fit=crop&auto=format',
      title: 'Website 3',
      description: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
    },
  ];

  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">The framework of choice when it matters</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {showcaseItems.map((item, index) => (
            <div key={index} className="bg-gray-100 rounded-lg shadow-md overflow-hidden">
              <img src={item.image} alt={item.title} className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-gray-600 text-base">{item.description}</p>
                <div className="mt-4 flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-2" />
                  <span className="text-gray-700">Built with Next.js</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        <button className="mt-12 mx-auto block bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg w-fit">View the Next.js Showcase</button>
      </div>
    </section>
  );
}