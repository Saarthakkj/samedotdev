import Header from '../components/Header';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import FoundationSection from '../components/FoundationSection';
import GetStartedSection from '../components/GetStartedSection';
import FrameworkSection from '../components/FrameworkSection';
import CTASection from '../components/CTASection';
import TestimonialSection from '../components/TestimonialSection';
import Footer from '../components/Footer';

export default function Page() {
  return (
    <div className="bg-white">
      <Header />
      <HeroSection />
      <FeaturesSection />
      <FoundationSection />
      <GetStartedSection />
      <FrameworkSection />
      <CTASection />
      <TestimonialSection />
      <Footer />
    </div>
  );
}