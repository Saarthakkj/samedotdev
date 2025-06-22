import Header from '../components/Header';
import Footer from '../components/Footer';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import ToolingSection from '../components/ToolingSection';
import TemplateSection from '../components/TemplateSection';
import ShowcaseSection from '../components/ShowcaseSection';
import CtaSection from '../components/CtaSection';
import TestimonialSection from '../components/TestimonialSection';

export default function Home() {
  return (
    <div className="bg-white text-gray-900">
      <Header />
      <main>
        <HeroSection />
        <FeaturesSection />
        <ToolingSection />
        <TemplateSection />
        <ShowcaseSection />
        <CtaSection />
        <TestimonialSection />
      </main>
      <Footer />
    </div>
  );
}