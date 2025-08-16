import React, { useRef } from "react";
import Navigation from "./components/Navigation/Navigation";
import "./components/styles/global.css";
import "./App.css";
import Footer from "./components/Footer/Footer";
import HeroSection from "./Pages/Home/HeroSection";
import PopupModal from "./Pages/PopupMsg/PopupModal";
import UploadSection from "./Pages/UploadSection/UploadSection";

function App() {
  const heroSectionRef = useRef(null);
  const uploadSectionRef = useRef(null);

  const handleGetStarted = () => {
    uploadSectionRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleScrollToTop = () => {
    heroSectionRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleLearnMore = () => {
    window.location.href = "#learn-more";
  };

  return (
    <section>
      <Navigation onHomeClick={handleScrollToTop} />
      <HeroSection
        heroSectionRef={heroSectionRef}
        handleGetStarted={handleGetStarted}
        handleLearnMore={handleLearnMore}
      />
      <UploadSection uploadSectionRef={uploadSectionRef} />
      <Footer />
    </section>
  );
}

export default App;
