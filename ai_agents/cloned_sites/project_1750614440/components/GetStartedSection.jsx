import { Plus } from 'lucide-react';;

export default function GetStartedSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Get Started
        </h2>
        <p className="mt-4 text-lg text-gray-600">
          Jumpstart your Next.js development with pre-built solutions.
        </p>
      </div>
      <div className="mt-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <TemplateCard
          title="Starter"
          description="A basic Next.js starter template."
          imageUrl="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=300&h=200&fit=crop"
        />
        <TemplateCard
          title="Ecommerce"
          description="A template for building e-commerce websites."
          imageUrl="https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=300&h=200&fit=crop"
        />
        <TemplateCard
          title="Blog"
          description="A template for creating blogs with Next.js."
          imageUrl="https://images.unsplash.com/photo-1517862378502-18b499f300a5?w=300&h=200&fit=crop"
        />
          <TemplateCard
          title="AI"
          description="A template for building AI-powered applications."
          imageUrl="https://images.unsplash.com/photo-1555096464-775414901e46?w=300&h=200&fit=crop"
        />
          <TemplateCard
          title="Portfolio"
          description="A template for showcasing your work."
          imageUrl="https://images.unsplash.com/photo-1497215728101-856f3ea21c49?w=300&h=200&fit=crop"
        />
          <TemplateCard
          title="SaaS"
          description="A template for building SaaS applications."
          imageUrl="https://images.unsplash.com/photo-1531403009284-e963660096bd?w=300&h=200&fit=crop"
        />
      </div>
      <div className="mt-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <button className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          <Plus className="mr-2 w-5 h-5" />
          Deploy a Template
        </button>
      </div>
    </section>
  );
}


function TemplateCard({ title, description, imageUrl }) {
  return (
    <div className="bg-gray-100 rounded-lg shadow-md p-6">
      <img src={imageUrl} alt={title} className="rounded-lg mb-4" />
      <h3 className="text-xl font-medium text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}