;

export default function TemplatesGallery() {
  const templates = [
    {
      title: 'Ecommerce Template',
      image: 'https://images.unsplash.com/photo-1542362567-b07152d05f55?w=300&h=200&fit=crop&auto=format',
      description: 'A fully functional ecommerce template built with Next.js',
    },
    {
      title: 'Blog Template',
      image: 'https://images.unsplash.com/photo-1499654035242-a244c2665943?w=300&h=200&fit=crop&auto=format',
      description: 'A clean and simple blog template for showcasing your writing',
    },
    {
      title: 'Portfolio Template',
      image: 'https://images.unsplash.com/photo-1517487881594-2711b3b9447e?w=300&h=200&fit=crop&auto=format',
      description: 'A stunning portfolio template to showcase your work',
    },
  ];

  return (
    <section className="py-12 bg-white">
      <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
        Explore Our Templates
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-6">
        {templates.map((template, index) => (
          <div
            key={index}
            className="bg-gray-100 rounded-lg shadow-md overflow-hidden"
          >
            <img
              src={template.image}
              alt={template.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {template.title}
              </h3>
              <p className="text-gray-600 text-base">{template.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}