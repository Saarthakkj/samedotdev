;

export default function HeroSection() {
  return (
    <section className="py-20 bg-[#fdfeff]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 className="text-8xl font-bold text-[#292a2b] mb-4">The React Framework for the Web</h1>
        <p className="text-lg text-[#737271] mb-8">Used by some of the world's largest companies, Next.js enables you to create high-quality web applications with the power of React components.</p>
        <div className="flex justify-center space-x-4">
          <button className="bg-[#171717] text-white py-3 px-6 rounded-lg hover:bg-[#1a1a1a]">Get Started</button>
          <button className="bg-white text-[#171717] py-3 px-6 rounded-lg border border-[#171717] hover:bg-[#f7faf9]">Learn Next.js</button>
        </div>
      </div>
    </section>
  );
}