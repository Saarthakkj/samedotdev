import { Image } from 'lucide-react';;

export default function ImageCard({ image, altText, description }) {
  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <img
        src={image}
        alt={altText}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="text-xl font-bold mb-2">{altText}</h3>
        <p className="text-gray-600">{description}</p>
        <div className="mt-4 flex justify-end">
          <Image className="w-6 h-6 text-gray-500" />
        </div>
      </div>
    </div>
  );
}