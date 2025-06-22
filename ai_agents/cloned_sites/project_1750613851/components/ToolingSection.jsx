import { React, Fragment } from 'react';
import { Code } from 'lucide-react';;



export default function ToolingSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">
          Built on a foundation of fast, production-grade tooling
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <ToolCard
            icon={""}
            title="React"
            description="The library for web and native user interfaces. Next.js is built on the latest React features, including Server Components and Actions."
          />
          <ToolCard
            icon={""}
            title="Turbopack"
            description="An incremental bundler optimized for JavaScript and TypeScript, written in Rust and built into Next.js."
          />
          <ToolCard
            icon={<Code className="w-12 h-12 text-green-500" />}
            title="Speedy Web Compiler"
            description="An extensible Rust based platform for the next generation of fast developer tools, and can be used for both compilation and minification."
          />
        </div>
      </div>
    </section>
  );
}

function ToolCard({ icon, title, description }) {
  return (
    <div className="bg-gray-100 p-8 rounded-lg shadow-md">
      <div className="flex items-center mb-4">
        {icon}
        <h3 className="text-xl font-medium ml-4">{title}</h3>
      </div>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}