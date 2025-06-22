import { ChevronDown, ChevronUp } from 'lucide-react';;

export default function TemplateSection() {
  const tabs = ["Starter", "Ecommerce", "Blog", "AI", "Portfolio", "SaaS", "Multi-tenant App"];
  const templates = [
    {
      name: "Next.js Com",
      description: "An all-in-one e performance",
      image: "https://images.unsplash.com/photo-1607252650355-f154ae625120?w=600&h=400&fit=crop",
    },
    {
      name: "Image Galler",
      description: "An image galle Cloudinary.",
      image: "https://images.unsplash.com/photo-1512112854688-e568c417bfbb?w=600&h=400&fit=crop",
    },
    {
      name: "Next.js Boilerplate",
      description: "A Next.js starter from create-next-app.",
      image: "https://images.unsplash.com/photo-1518770660439-464ef50ce903?w=600&h=400&fit=crop",
    },
  ];

  return (
    <section className="bg-fafafa py-12">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-semibold text-center text-gray-800 mb-4">Get started in seconds</h2>
        <p className="text-center text-gray-600 mb-8">Deploy Next.js to Vercel</p>

        <div className="flex justify-center space-x-4 mb-6">
          {tabs.map((tab) => (
            <button
              key={tab}
              className="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 rounded shadow"
            >
              {tab}
            </button>
          ))}
        </div>

        <p className="text-center text-gray-600 mb-8">Vercel is a frontend cloud from the creators of Next.js, making it easy to get started with Next.js quickly.</p>
        <p className="text-center text-gray-600 mb-8">Jumpstart your Next.js development with pre-built solutions from Vercel and our community.</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <img src={template.image} alt={template.name} className="w-full h-48 object-cover" />
              <div className="p-4">
                <h3 className="text-lg font-semibold text-gray-800">{template.name}</h3>
                <p className="text-gray-600">{template.description}</p>
                <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">
                  Deploy a Template on Vercel
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-center mt-8">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Deploy a Template on Vercel
          </button>
        </div>
      </div>
    </section>
  );
}