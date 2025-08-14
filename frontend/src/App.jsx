// App.jsx
import React, { useRef, useState } from 'react';
import axios from 'axios';
import Navigation from './components/Navigation';
import Orb from './components/Orb';
import Threads from './components/Threads';
import './styles/global.css';
import './App.css';
import Footer from './components/Footer';

const validTypes = [
  // mp3
  'audio/mpeg',
  // wav (browsers vary)
  'audio/wav',
  'audio/x-wav',
  'audio/wave',
  // mp4 (audio/video containers)
  'video/mp4',
  'audio/mp4',
  'video/quicktime', // just in case some cameras export mp4 as quicktime
];

const allowedExtensions = ['.mp3', '.wav', '.mp4'];

function App() {
  const heroSectionRef = useRef(null);
  const uploadSectionRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | uploading | processing | complete | error
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  const handleGetStarted = () => {
    uploadSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScrollToTop = () => {
    heroSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleLearnMore = () => {
    window.location.href = '#learn-more';
  };

  const isTypeAllowed = (file) => {
    const mimeOk = file.type ? validTypes.includes(file.type) : false;
    const extOk = allowedExtensions.some((ext) =>
      file.name.toLowerCase().endsWith(ext)
    );
    // accept if either MIME or extension matches (some browsers omit or vary audio MIME)
    return mimeOk || extOk;
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!isTypeAllowed(file)) {
      alert('Only .mp3, .wav, or .mp4 files are allowed.');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      alert('File size should be less than 50MB.');
      return;
    }

    setSelectedFile(file);
    setStatus('idle');
    setResult(null);
    setErrorMsg('');
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setStatus('uploading');
      setErrorMsg('');
      setResult(null);

      const form = new FormData();
      form.append('file', selectedFile);
      form.append('model_type', 'wav2vec'); // default model

      // POST to FastAPI: /api/predict
      const { data } = await axios.post(`${API_BASE}/api/predict`, form, {
        onUploadProgress: (e) => {
             if (!e.total) return;              // sometimes total is undefined
             const pct = Math.round((e.loaded * 100) / e.total);
             setStatus(pct >= 100 ? 'processing' : 'uploading');
           }
      });

      setResult(data);
      setStatus('complete');
      console.log('Prediction result:', data);
    } catch (err) {
      console.error(err);
      setStatus('error');
      setErrorMsg(
        err?.response?.data?.error ||
          err?.message ||
          'Upload failed. Please try again.'
      );
    }
  };

  return (
    <section>
      <Navigation onHomeClick={handleScrollToTop} />

      {/* Hero Section */}
      <div className="app-root" ref={heroSectionRef} style={{ minHeight: '100vh' }}>
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

      {/* Upload Section */}
      <div>
        <div ref={uploadSectionRef} className="upload-section app-root">
          <Threads amplitude={3.5} distance={0.5} />
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
                const file = e.dataTransfer.files?.[0];
                if (file) handleFileChange({ target: { files: [file] } });
              }}
            >
              {/* Hidden file input */}
              <input
                type="file"
                id="fileInput"
                style={{ display: 'none' }}
                accept="audio/*,video/mp4,video/quicktime,.mp3,.wav,.mp4,.mov"
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

            {/* Selected file + status + actions */}
            {selectedFile && (
              <div className="selected-file">
                <p>
                  📎 <strong>{selectedFile.name}</strong> (
                  {(selectedFile.size / 1024).toFixed(2)} KB)
                </p>

                {status !== 'idle' && (
                  <p className={`status-text status-${status}`}>
                    Status: {status}
                  </p>
                )}

                {status === 'error' && (
                  <p className="status-text status-error">{errorMsg}</p>
                )}

                {result && (
                  <pre
                    style={{
                      marginTop: 12,
                      padding: 12,
                      borderRadius: 8,
                      background: 'rgba(0,0,0,0.6)',
                      color: 'white',
                      overflowX: 'auto',
                    }}
                  >
                    {JSON.stringify(result, null, 2)}
                  </pre>
                )}

                <div className="button-row">
                  <button
                    className="upload-file-btn"
                    onClick={handleUpload}
                    disabled={status === 'uploading' || status === 'processing'}
                  >
                    {status === 'uploading' || status === 'processing'
                      ? 'Uploading...'
                      : 'Upload File'}
                  </button>

                  <button
                    className="cancel-btn"
                    onClick={() => {
                      setSelectedFile(null);
                      setStatus('idle');
                      setResult(null);
                      setErrorMsg('');
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Footer />
    </section>
  );
}

export default App;
