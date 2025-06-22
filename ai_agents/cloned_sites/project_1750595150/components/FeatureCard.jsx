import { Star } from 'lucide-react';;
import React from 'react';
export default function FeatureCard({ title, description, icon, imageURL }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-sm">
      <div className="flex items-center mb-4">
        {icon && (
          <div className="bg-gray-100 rounded-full p-2 mr-4">
            {React.createElement(icon, { className: 'w-6 h-6 text-gray-600' })}
          </div>
        )}
        <h3 className="text-xl font-semibold text-gray-800">{title}</h3>
      </div>
      <p className="text-gray-600 mb-4">{description}</p>
      {imageURL && (
        <img
          src={imageURL}
          alt={title}
          className="rounded-lg w-full h-48 object-cover mb-4"
        />
      )}
      <div className="flex items-center">
        <Star className="w-5 h-5 text-yellow-500 mr-2" />
        <p className="text-gray-600">4.5 stars</p>
      </div>
    </div>
  );
}