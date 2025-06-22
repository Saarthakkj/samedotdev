import Header from '../components/Header';
import Hero from '../components/Hero';
import FeatureCard from '../components/FeatureCard';
import ExampleProjectCard from '../components/ExampleProjectCard';
import Footer from '../components/Footer';

export default function Page() {
  return (
    <div className="bg-gray-100">
      <Header />
      <Hero 
        title="Next.js Landing Page"
        subtitle="A modern landing page built with Next.js, Tailwind CSS, and Lucide React icons."
        imageUrl="https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1920&h=1080&fit=crop" 
      />
      <section className="py-12 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-8">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard title="Fast Performance" description="Next.js's performance is unmatched, leading to faster load times and a better user experience." icon={<TrendingUp className="w-6 h-6 text-blue-500" />} />
            <FeatureCard title="SEO Optimization" description="Build SEO-friendly websites with Next.js's built-in support for static site generation and server-side rendering." icon={<Search className="w-6 h-6 text-green-500" />} />
            <FeatureCard title="Serverless Functions" description="Easily deploy serverless functions to handle backend logic and data processing without managing servers." icon={<Server className="w-6 h-6 text-purple-500" />} />
          </div>
        </div>
      </section>
      <section className="py-12 bg-gray-100">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-8">Example Projects</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <ExampleProjectCard title="Project 1" description="A sample project built with Next.js showcasing its capabilities." imageUrl="https://images.unsplash.com/photo-1494790106972-20038667a5e8?w=300&h=200&fit=crop" />
            <ExampleProjectCard title="Project 2" description="Another example project highlighting different aspects of Next.js." imageUrl="https://images.unsplash.com/photo-1551434678-e076c7607a61?w=300&h=200&fit=crop" />
            <ExampleProjectCard title="Project 3" description="Yet another project showcasing the versatility of Next.js." imageUrl="https://images.unsplash.com/photo-1618005155142-d29a13864074?w=300&h=200&fit=crop" />
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}