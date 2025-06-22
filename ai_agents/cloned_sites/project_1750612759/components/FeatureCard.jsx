import { Check } from 'lucide-react';;

export default function FeatureCard({ title, description }) {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 flex flex-col items-start space-y-4">
      <div className="flex items-center space-x-2">
        <Check className="w-6 h-6 text-blue-500" />
        <h3 className="text-xl font-bold text-gray-800">{title}</h3>
      </div>
      <p className="text-gray-600 text-base">{description}</p>
    </div>
  );
}