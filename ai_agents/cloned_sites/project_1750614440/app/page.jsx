import Header from '../components/Header';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import FoundationSection from '../components/FoundationSection';
import GetStartedSection from '../components/GetStartedSection';
import ShowcaseSection from '../components/ShowcaseSection';
import TestimonialsSection from '../components/TestimonialsSection';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <main className="bg-fcfefe">
      <Header />
      <HeroSection />
      <FeaturesSection />
      <FoundationSection />
      <GetStartedSection />
      <ShowcaseSection />
      <TestimonialsSection />
      <Footer />
    </main>
  );
}