
import { Code, Database, Server } from 'lucide-react';;

export default function ToolingCards() {
  const toolingData = [
    {
      icon: <Code className="w-6 h-6 text-gray-600" />,
      title: 'React',
      description: 'The library for web and native user interfaces. Next.js is built on the latest React features, including Server Components and Actions.',
    },
    {
      icon: <Database className="w-6 h-6 text-gray-600" />,
      title: 'Turbopack',
      description: 'An incremental bundler optimized for JavaScript and TypeScript, written in Rust and built into Next.js.',
    },
    {
      icon: <Server className="w-6 h-6 text-gray-600" />,
      title: 'Speedy Web Compiler',
      description: 'An extensible Rust-based platform for the next generation of fast developer tools, and can be used for both compilation and minification.',
    },
  ];

  return (
    <section className="py-12">
      <h2 className="text-3xl font-bold text-gray-900 mb-8">Built on a foundation of fast, production-grade tooling</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {toolingData.map((tool, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              {tool.icon}
              <h3 className="text-xl font-semibold ml-4 text-gray-900">{tool.title}</h3>
            </div>
            <p className="text-gray-600 text-base">{tool.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}