import React from "react";
import Orb from "../../components/ReactBit_Bgs/Orb";
import '../Home/HeroSection.css'

export default function HeroSection({ heroSectionRef, handleGetStarted, handleLearnMore }) {
  return (
    <div className="app-root" ref={heroSectionRef} style={{ minHeight: "100vh" }}>
      <Orb hoverIntensity={5} rotateOnHover={true} hue={5} forceHoverState={false} />
      <div className="text-content">
        <h1 className="heading">
          AI-Powered <br /> Deepfake Detector
        </h1>
        <div className="button-group">
          <button onClick={handleGetStarted} className="glassButton primary">
            Get Started
          </button>
          <button onClick={handleLearnMore} className="glassButton secondary">
            Learn More
          </button>
        </div>
      </div>
    </div>
  );
}
