import React, { useRef, useState } from 'react';
import Navigation from './components/Navigation';
import Orb from './components/Orb';
import Threads from './components/Threads';
import './styles/global.css';
import './App.css';
import Footer from './components/Footer';


const validTypes = [
  "image/jpeg",
  "image/png",
  "image/gif",
  "video/mp4",
  "video/quicktime"
];


function App() {
  const heroSectionRef = useRef(null);
  const uploadSectionRef = useRef(null);
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState('idle'); // 'idle'

  const handleGetStarted = () => {
    uploadSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScrollToTop = () => {
    heroSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleLearnMore = () => {
    window.location.href = '#learn-more';
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!validTypes.includes(file.type)) {
        alert('Only .mp3, .wav, or .mp4 files are allowed.');
        return;
      }

      if (file.size > 50 * 1024 * 1024) {
        alert('File size should be less than 50MB.');
        return;
      }

      setSelectedFile(file);
    }
  };

  const handleUpload = () => {
    setStatus('uploading');
    setTimeout(() => {
      setStatus('processing');
      setTimeout(() => {
        setStatus('complete');
      }, 2000);
    }, 2000);
  };

  return (
    <section>
      <Navigation onHomeClick={handleScrollToTop} />

      {/* Hero Section */}
      <div className="app-root" ref={heroSectionRef} style={{ minHeight: '100vh' }}>
        <Orb
          hoverIntensity={5}
          rotateOnHover={true}
          hue={5}
          forceHoverState={false}
        />
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

      {/* Upload Section */}
      {/* <div className="threads-bg"> */}
      {/* content */}
      <div>
        <div ref={uploadSectionRef} className="upload-section app-root">
          <Threads
            amplitude={3.5}
            distance={0.5}
          // disableMouse={true}
          />
          <div className="upload-foreground">
            <h2 className="upload-title">Upload your file</h2>
            <p className="upload-subtitle">Drag and drop or browse from your device</p>

            {/* Upload box */}
            <div
              className="upload-box"
              onClick={() => document.getElementById('fileInput').click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const file = e.dataTransfer.files[0];
                handleFileChange({ target: { files: [file] } });
              }}
            >
              {/* Hidden file input  */}
              <input
                type="file"
                id="fileInput"
                style={{ display: 'none' }}
                accept=".mp3, .wav, .mp4"
                onChange={handleFileChange}
              />
              <div className="upload-icon">📤</div>
              <p>Select files to upload</p>
              <button
                className="browse-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  document.getElementById('fileInput').click();
                }}
              >
                Browse Files
              </button>
            </div>

            {/* Selected file name */}
            {selectedFile && (
              <div className="selected-file">
                <p>
                  📎 <strong>{selectedFile.name}</strong> (
                  {(selectedFile.size / 1024).toFixed(2)} KB)
                </p>

                {status !== 'idle' && (
                  <p className={`status-text status-${status}`}>Status: {status}</p>
                )}

                <div className='button-row'>
                  <button
                    className="upload-file-btn"
                    onClick={handleUpload}
                    disabled={!selectedFile || !selectedModel}
                  >
                    Upload File
                  </button>

                  <button
                    className="cancel-btn"
                    onClick={() => {
                      setSelectedFile(null)
                      setSelectedModel('');
                      setStatus('idle');
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
            {selectedFile && <p>Selected file: {selectedFile.name}</p>}
          </div>
        </div>
      </div>
      <Footer />
      {/* </div> */}
    </section>
  );
}

export default App;
