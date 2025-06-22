import { Clock } from 'lucide-react';;

export default function PromoCard() {
  return (
    <div className="bg-[#272829] rounded-lg p-6 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <Clock className="w-6 h-6 text-white" />
        <span className="text-white text-sm">Next.js 13</span>
      </div>
      <h2 className="text-2xl font-bold text-white mb-2">The power of full-stack to the frontend.</h2>
      <p className="text-gray-300 text-base">Read the release notes.</p>
      <a href="#" className="text-white text-sm mt-4 hover:underline">Learn More</a>
    </div>
  );
}