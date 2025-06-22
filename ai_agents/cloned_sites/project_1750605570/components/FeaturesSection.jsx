import { Zap, Lock, Code, TrendingUp, ShieldCheck, Layout } from 'lucide-react';;

export default function FeaturesSection() {
  return (
    <div className="bg-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-orange-600 font-semibold tracking-wide uppercase">What's in Next.js?</h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need to build great products on the web.
          </p>
        </div>

        <div className="mt-10">
          <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 lg:grid-cols-4 md:gap-x-8 md:gap-y-10">
            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <Zap className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Built-in Optimizations</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Automatic Image, Font, and Script Optimizations for Improved UX and Core Web Vitals.
              </dd>
            </div>

            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <TrendingUp className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Dynamic HTML Streaming</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Instantly stream UI from the server, integrated with the App Router and React Suspense.
              </dd>
            </div>

            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <Layout className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">React Server Components</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Add components without sending additional client-side JavaScript. Built on the latest React features.
              </dd>
            </div>

            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <Lock className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Data Fetching</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Make your React component async and await your data. Next.js supports both server and client data fetching.
              </dd>
            </div>

            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <Code className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">CSS Support</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Style your application with your favorite tools, Including support for CSS Modules, Tailwind CSS, and popular community libraries.
              </dd>
            </div>

            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <ShieldCheck className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Client and Server Rendering</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Flexible rendering and caching options, including Incremental Static Regeneration (ISR), on a per-page level.
              </dd>
            </div>

            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <Code className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Server Actions</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Run server code by calling a function. Skip the API. Then, easily revalidate cached data and update your UI in one network roundtrip.
              </dd>
            </div>

            <div className="relative">
              <dt>
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                  <Code className="h-6 w-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Route Handlers</p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                Build API endpoints to securely connect with third-party services for handling auth or listening for webhooks.
              </dd>
            </div>

              <div className="relative">
                  <dt>
                      <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                          <Code className="h-6 w-6" aria-hidden="true" />
                      </div>
                      <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Next.js 15</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-500">
                      The power of full-stack to the frontend. Read the release notes.
                  </dd>
              </div>
              <div className="relative">
                  <dt>
                      <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                          <Code className="h-6 w-6" aria-hidden="true" />
                      </div>
                      <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Advanced Routing & Nested Layouts</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-500">
                      Create routes using the file system, including support for more advanced routing patterns and UI layouts.
                  </dd>
              </div>
              <div className="relative">
                  <dt>
                      <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-orange-500 text-white">
                          <Code className="h-6 w-6" aria-hidden="true" />
                      </div>
                      <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Middleware</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-500">
                      Take control of the incoming request. Use code to define routing and access rules for authentication, experimentation, and internationalization.
                  </dd>
              </div>
          </dl>
        </div>
      </div>
    </div>
  );
}