import React from 'react';
import Orb from './components/Orb';
import './styles/global.css'; // optional custom styles
import './App.css'; // include this if you’re styling via App.css

function App() {
  return (
    <div className="relative w-screen h-screen overflow-hidden bg-black">
      {/* Orb Background */}
      <div className="absolute inset-0 z-0">
        <Orb
          hoverIntensity={1.0}        // change this value to increase/decrease sensitivity
          rotateOnHover={true}
          hue={250}
          forceHoverState={false}
        />
      </div>

      {/* Text Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-white text-center px-4">
        <h1 className="text-5xl font-bold mb-4 leading-tight">
          AI-Powered <br /> Deepfake <br /> Detector
        </h1>
        <p className="text-lg">Upload audio or video to detect deepfake voices.</p>
      </div>
    </div>
  );
}

export default App;
