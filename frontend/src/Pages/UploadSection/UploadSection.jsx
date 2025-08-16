import React, { useState } from "react";
import Threads from "../../components/ReactBit_Bgs/Threads";
import PopupModal from '../PopupMsg/PopupModal';
import '../UploadSection/UploadSection.css'

const validTypes = [
  "audio/mpeg",
  "audio/wav",
  "video/mp4",
  "image/jpeg",
  "image/png",
  "image/gif",
  "video/quicktime"
];

export default function UploadSection({ uploadSectionRef }) {
  const [selectedModel, setSelectedModel] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showModal, setShowModal] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!validTypes.includes(file.type)) {
        setShowModal(true);
        return;
      }
      if (file.size > 50 * 1024 * 1024) {
        alert("File size exceeds 50MB");
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleUpload = () => {
    setStatus("uploading");
    setUploadProgress(0);
    let progress = 0;

    const interval = setInterval(() => {
      progress += 10;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        setStatus("processing");
        setTimeout(() => {
          setStatus("complete");
        }, 2000);
      }
    }, 2000);
  };

  return (
    <div ref={uploadSectionRef} className="upload-section app-root">
      <Threads amplitude={3.5} distance={0.5} />
      <div className="upload-foreground">
        <h2 className="upload-title">Upload your file</h2>
        <p className="upload-subtitle">Drag and drop or browse from your device</p>

        <div
          className="upload-box"
          onClick={() => document.getElementById("fileInput").click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            const file = e.dataTransfer.files[0];
            handleFileChange({ target: { files: [file] } });
          }}
        >
          <input
            type="file"
            id="fileInput"
            style={{ display: "none" }}
            accept=".mp3, .wav, .mp4, .jpg, .jpeg, .png, .gif"
            onChange={handleFileChange}
          />
          {showModal && (
            <PopupModal
              message="Invalid file type! Please select a valid file."
              onClose={() => setShowModal(false)}
            />
          )}
          <div className="upload-icon">📤</div>
          <p>
            Select files to upload <br /> Only supported formats are allowed
          </p>
          <button
            className="browse-btn"
            onClick={(e) => {
              e.stopPropagation();
              document.getElementById("fileInput").click();
            }}
          >
            Browse Files
          </button>
        </div>

        {selectedFile && (
          <div className="selected-file">
            {status === "uploading" && (
              <div className="mt-4 w-full">
                <p className="text-blue-500 mb-2">Uploading... {uploadProgress}%</p>
                <div className="w-full bg-gray-300 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
              </div>
            )}

            <p>
              📎 <strong>{selectedFile.name}</strong> (
              {(selectedFile.size / 1024).toFixed(2)} KB)
            </p>

            {status !== "idle" && (
              <p className={`status-text status-${status}`}>Status: {status}</p>
            )}

            <div className="button-row">
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
                  setSelectedFile(null);
                  setSelectedModel("");
                  setStatus("idle");
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
