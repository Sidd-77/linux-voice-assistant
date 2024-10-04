import React from 'react';
import { Mic } from 'lucide-react';

const ListeningState = ({ transcript }) => (
  <div className="text-center">
    <div className="relative">
      <Mic size={64} className="text-blue-500 mx-auto" />
      <div className="absolute top-0 left-0 w-full h-full animate-ping bg-blue-400 rounded-full opacity-75"></div>
      <div className="absolute top-0 left-0 w-full h-full animate-pulse bg-purple-400 rounded-full opacity-75" style={{animationDelay: '0.5s'}}></div>
    </div>
    <p className="mt-6 text-xl font-semibold text-gray-700">Listening...</p>
    {transcript && (
      <p className="mt-2 text-sm text-gray-600 italic">{transcript}</p>
    )}
  </div>
);

export default ListeningState;