import { Check } from 'lucide-react';;

export default function FeaturesSection() {
  const features = [
    {
      title: 'Built-in Optimizations',
      description: 'Automatic Image, Font, and Script Optimizations for Improved',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Dynamic HTML Streaming',
      description: 'Instantly stream UI from the server, integrated with the App Router and React Suspense.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'React Server Components',
      description: 'Add components without sending additional client-side JavaScript. Built on the latest React features.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Data Fetching',
      description: 'Make your React component async and await your data. Next.js supports both server and client data fetching.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'CSS Support',
      description: 'Style your application with your favorite tools, including support for CSS Modules, Tailwind CSS, and popular community libraries.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Client and Server Rendering',
      description: 'Flexible rendering and caching options, including Incremental Static Regeneration (ISR), on a per-page level.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Server Actions',
      description: 'Run server code by calling a function. Skip the API. Then, easily revalidate cached data and update your UI in one network roundtrip.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Route Handlers',
      description: 'Build API endpoints to securely connect with third-party services for handling auth or listening for webhooks.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Middleware',
      description: 'Take control of the incoming request. Use code to define routing and access rules for authentication, experimentation, and internationalization.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Advanced Routing & Nested Layouts',
      description: 'Create routes using the file system, including support for more advanced routing patterns and UI layouts.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    },
    {
      title: 'Next.js 15',
      description: 'The power of full-stack to the frontend. Read the release notes.',
      icon: <Check className="w-6 h-6 text-blue-500" />
    }
  ];

  return (
    <section className="py-16 bg-gray-50">
      <h2 className="text-3xl font-bold text-gray-800 text-center mb-8">What's in Next.js?</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-4">
        {features.map((feature) => (
          <div key={feature.title} className="bg-white shadow-md rounded-lg p-6">
            <div className="flex items-center mb-4">
              {feature.icon}
              <h3 className="text-xl font-semibold ml-4">{feature.title}</h3>
            </div>
            <p className="text-gray-600">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}