// src/components/PopupModal.jsx
import React from 'react';
import './PopupModal.css';

const PopupModal = ({ message, onClose }) => {
  return (
    <div className="popup-overlay">
      <div className="popup-box">
        <p>{message}</p>
        <button onClick={onClose}>OK</button>
      </div>
    </div>
  );
};

export default PopupModal;
