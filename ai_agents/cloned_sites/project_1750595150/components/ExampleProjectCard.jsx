import { Star, Check } from 'lucide-react';;

export default function ExampleProjectCard({ project }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-900">{project.name}</h3>
        <Star className="w-6 h-6 text-yellow-500" />
      </div>
      <img
        src={project.imageUrl}
        alt={project.name}
        className="w-full h-48 object-cover rounded-lg mb-4"
      />
      <p className="text-gray-700 text-base mb-4">{project.description}</p>
      <div className="flex items-center space-x-2">
        {project.technologies.map((tech) => (
          <span key={tech} className="bg-gray-200 text-gray-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded">
            {tech}
          </span>
        ))}
      </div>
      <div className="flex justify-between mt-4">
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          View Project
        </button>
        <Check className="w-6 h-6 text-green-500" />
      </div>
    </div>
  );
}