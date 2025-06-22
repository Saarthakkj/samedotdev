import { Globe } from 'lucide-react';;

export default function ShowcaseSection() {
  const images = [
    { id: 'jK9dTbMhV_A', width: 600, height: 400 },
    { id: 'jFCViYFYcus', width: 600, height: 400 },
    { id: '9XAYSjmxoUU', width: 600, height: 400 },
    { id: '4w8ZTWZ3xCQ', width: 600, height: 400 },
    { id: '79jR2t_H57Q', width: 600, height: 400 },
    { id: '1pdmJHfHMkM', width: 600, height: 400 },
  ];

  return (
    <div className="bg-fafafa py-12">
      <div className="container mx-auto px-4">
        <h2 className="text-2xl md:text-3xl font-semibold text-gray-800 mb-8 text-center">
          The framework of choice when it matters
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {images.map((image) => (
            <div key={image.id} className="relative rounded-md overflow-hidden shadow-md">
              <img
                src={`https://images.unsplash.com/photo-${image.id}?w=${image.width}&h=${image.height}&fit=crop`}
                alt={`Showcase ${image.id}`}
                className="w-full h-full object-cover aspect-video"
              />
              <div className="absolute top-0 left-0 w-full h-full bg-black opacity-0 hover:opacity-60 transition-opacity duration-300 flex items-center justify-center">
                <Globe className="w-8 h-8 text-white" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}