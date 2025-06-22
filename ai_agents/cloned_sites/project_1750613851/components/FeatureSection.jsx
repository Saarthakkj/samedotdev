import { Grid } from 'lucide-react';;

export default function FeatureSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          What's in Next.js?
        </h2>
        <p className="mt-4 text-lg text-gray-600">
          Everything you need to build great products on the web.
        </p>
        <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <FeatureCard title="Built-in Optimizations" description="Automatic Image, Font, and Script Optimizations for Improved UX and Core Web Vitals." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="Dynamic HTML Streaming" description="Instantly stream UI from the server, integrated with the App Router and React Suspense." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="React Server Components" description="Add components without sending additional client-side JavaScript. Built on the latest React features." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="Data Fetching" description="Make your React component async and await your data. Next.js supports both server and client data fetching." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="CSS Support" description="Style your application with your favorite tools, including support for CSS Modules, Tailwind CSS, and popular community libraries." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="Client and Server Rendering" description="Flexible rendering and caching options, including Incremental Static Regeneration (ISR), on a per-page level." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="Server Actions" description="Run server code by calling a function. Skip the API. Then, easily revalidate cached data and update your UI in one network roundtrip." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="Route Handlers" description="Build API endpoints to securely connect with third-party services for handling auth or listening for webhooks." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="Advanced Routing & Nested Layouts" description="Create routes using the file system, including support for more advanced routing patterns and UI layouts." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
          <FeatureCard title="Middleware" description="Take control of the incoming request. Use code to define routing and access rules for authentication, experimentation, and internationalization." icon={<Grid className="h-6 w-6 text-indigo-600" />} />
        </div>
      </div>
    </section>
  );
}

function FeatureCard({ title, description, icon }) {
  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden">
      <div className="p-6">
        {icon}
        <h3 className="mt-4 text-lg font-medium text-gray-900">{title}</h3>
        <p className="mt-2 text-sm text-gray-600">{description}</p>
      </div>
    </div>
  );
}