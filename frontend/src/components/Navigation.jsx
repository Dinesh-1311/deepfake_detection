import React from 'react';
import './Navigation.css';

const Navbar = ({ onHomeClick }) => {
  return (
    <nav className="navigation">
      <div className="nav-content">
        <div className="nav-left">
          <div className="logo">
            <div className="logo-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="white"/>
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="white" opacity="0.3"/>
              </svg>
            </div>
            <span className="logo-text">React Bits</span>
          </div>
        </div>
        <div className="nav-right">
          <a onClick={onHomeClick} className="nav-link" style={{ cursor: 'pointer' }}>Home</a>
          <a href="/upload" className="nav-link">Docs</a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 