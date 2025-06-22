
export default function HeroSection() {
  return (
    <section className="bg-[#fdfeff] py-24">
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-5xl font-bold text-[#0a0b0d] mb-4">
          The React Framework for the Web
        </h1>
        <p className="text-lg text-[#868d8f] mb-8">
          Used by some of the world's largest companies, Next.js enables you to
          create high-quality web applications with the power of React components.
        </p>
        <div className="flex justify-center space-x-4">
          <button className="bg-[#0a0b0d] text-white px-8 py-3 rounded-lg hover:bg-[#262929] transition-colors">
            Get Started
          </button>
          <button className="bg-[#f2af67] text-white px-8 py-3 rounded-lg hover:bg-[#928d48] transition-colors">
            Learn Next.js
          </button>
        </div>
        <p className="text-gray-500 mt-8">^ npx create-next-app@latest</p>
      </div>
    </section>
  );
}