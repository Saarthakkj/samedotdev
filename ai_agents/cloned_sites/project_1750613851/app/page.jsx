import Header from '../components/Header';
import HeroSection from '../components/HeroSection';
import FeatureSection from '../components/FeatureSection';
import PromoCard from '../components/PromoCard';
import ToolingSection from '../components/ToolingSection';
import GettingStartedSection from '../components/GettingStartedSection';
import ShowcaseSection from '../components/ShowcaseSection';
import TestimonialsSection from '../components/TestimonialsSection';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <div className="bg-white">
      <Header />
      <HeroSection />
      <FeatureSection />
      <PromoCard />
      <ToolingSection />
      <GettingStartedSection />
      <ShowcaseSection />
      <TestimonialsSection />
      <Footer />
    </div>
  );
}