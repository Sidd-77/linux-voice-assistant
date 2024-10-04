import React, { useState, useEffect, useCallback } from 'react';
import IdleState from './components/idle';
import ListeningState from './components/listening';
import ProcessingState from './components/processing';
import OutputState from './components/output';
import axios from 'axios';

const App = () => {
  const [state, setState] = useState('idle');
  const [output, setOutput] = useState('');
  const [recognition, setRecognition] = useState(null);
  const [transcript, setTranscript] = useState('');

  useEffect(() => {
    if ('webkitSpeechRecognition' in window) {
      const recognitionInstance = new window.webkitSpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onresult = (event) => {
        const last = event.results.length - 1;
        const text = event.results[last][0].transcript;
        setTranscript(text);
        setState('processing');
        processCommand(text);
      };

      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        setState('idle');
      };

      recognitionInstance.onend = () => {
        if (state === 'listening') {
          setState('idle');
        }
      };

      setRecognition(recognitionInstance);
    } else {
      console.error('Speech recognition not supported');
    }
  }, []);

  const processCommand = useCallback((command) => {
    setState('processing');
    axios.post('http://127.0.0.1:8000/query', { query: command })
      .then(response => {
        console.log('Command processed', response.data);
        let data = JSON.parse(response.data);
        console.log('json data',data);
        setOutput(data.description);
        setState('output');
      })
      .catch(error => {
        console.error('Error processing command', error);
        setOutput('Sorry, there was an error processing your request.');
        setState('output');
      });
  }, []);


  const handleMicClick = useCallback(() => {
    if (recognition && state === 'idle') {
      recognition.start();
      setState('listening');
    }
  }, [recognition, state]);

  const handleTryAgain = useCallback(() => {
    setState('idle');
    setOutput('');
    setTranscript('');
  }, []);

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-br from-blue-100 to-purple-100">
      <div className="w-96 h-144 bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col transform transition-all duration-500 ease-in-out hover:scale-105">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6">
          <h2 className="text-2xl font-bold">Voice Assistant</h2>
        </div>
        
        <div className="flex-grow p-8 flex flex-col items-center justify-center bg-gray-50">
          {state === 'idle' && <IdleState onMicClick={handleMicClick} />}
          {state === 'listening' && <ListeningState transcript={transcript} />}
          {state === 'processing' && <ProcessingState />}
          {state === 'output' && <OutputState output={output} onTryAgain={handleTryAgain} />}
        </div>
        
        <div className="bg-gray-100 p-4 text-center">
          <p className="text-sm text-gray-600 font-medium">
            {state === 'idle' ? 'Click the mic to start' : `Status: ${state}`}
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;