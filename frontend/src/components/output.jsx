import React from 'react';
import { MessageSquare, RotateCcw } from 'lucide-react';

const OutputState = ({ output, onTryAgain }) => (
  <div className="text-center">
    <MessageSquare size={64} className="text-green-500 mx-auto animate-bounce" />
    <p className="mt-6 text-xl font-semibold text-gray-700">{output}</p>
    <button
      onClick={onTryAgain}
      className="mt-4 flex items-center justify-center bg-blue-500 text-white rounded-full px-4 py-2 hover:bg-blue-600 transition-colors"
    >
      <RotateCcw size={16} className="mr-2" />
      Try Again
    </button>
  </div>
);

export default OutputState;