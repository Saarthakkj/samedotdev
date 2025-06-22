import NavigationBar from '../components/NavigationBar'
import HeroSection from '../components/HeroSection'
import FeaturesGrid from '../components/FeaturesGrid'
import ToolingCards from '../components/ToolingCards'
import TemplatesGallery from '../components/TemplatesGallery'
import ShowcaseSection from '../components/ShowcaseSection'
import Testimonials from '../components/Testimonials'
import Footer from '../components/Footer'

export default function Home() {
  const features = [
    {
      title: 'Next.js',
      description: 'Next.js is a React framework for building server-side rendered applications.'
    },
    {
      title: 'React',
      description: 'React is a JavaScript library for building user interfaces.'
    },
    {
      title: 'Tailwind CSS',
      description: 'Tailwind CSS is a utility-first CSS framework for rapidly building custom user interfaces.'
    }
  ]
  return (
    <div className="bg-fdfeff">
      <NavigationBar />
      <HeroSection />
      <FeaturesGrid features={features}/>
      <ToolingCards />
      <TemplatesGallery />
      <ShowcaseSection />
      <Testimonials />
      <Footer />
    </div>
  )
}