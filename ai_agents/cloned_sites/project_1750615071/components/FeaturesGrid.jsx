import { Grid } from 'lucide-react';;

export default function FeaturesGrid({ features }) {
  return (
    <section className="py-12">
      <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">Features</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-4">
        {features.map((feature, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Grid className="w-6 h-6 text-gray-500 mr-4" />
              <h3 className="text-xl font-semibold text-gray-900">{feature.title}</h3>
            </div>
            <p className="text-gray-700">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}