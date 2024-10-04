import React from 'react';
import { Mic } from 'lucide-react';

const IdleState = ({ onMicClick }) => (
  <button
    onClick={onMicClick}
    className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full p-6 hover:from-blue-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-110 focus:outline-none focus:ring-4 focus:ring-purple-300"
  >
    <Mic size={40} />
  </button>
);

export default IdleState;