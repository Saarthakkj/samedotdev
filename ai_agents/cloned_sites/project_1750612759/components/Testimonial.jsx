import { Star } from 'lucide-react';;

export default function Testimonial({ quote, author, title }) {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md mx-4 md:mx-6 lg:mx-8 my-6 md:my-8 lg:my-12">
      <blockquote className="text-lg text-gray-700 mb-4 leading-relaxed">
        <p>{quote}</p>
      </blockquote>
      <div className="flex items-center">
        <Star className="w-6 h-6 text-yellow-500 mr-2" />
        <div>
          <p className="text-gray-900 font-medium">{author}</p>
          <p className="text-gray-500 text-sm">{title}</p>
        </div>
      </div>
    </div>
  );
}