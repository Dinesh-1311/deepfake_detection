// src/components/Footer.js
import React from 'react';
import './Footer.css'

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Left Section - Company Info */}
        <div className="footer-left">
          <h2 className="footer-company">Thunder Tribes</h2>
          <p className="footer-tagline">
            Next-Gen IT Solutions for Your Business
          </p>
          <p className="footer-contact">
            📧 info@thundertribes.com<br />
            📞 +91 91136 88291 | +44 7405 933901
          </p>
          <p className="footer-copyright">
            © {year} Thunder Tribes. All rights reserved.
          </p>
        </div>

        {/* Right Section - Navigation */}
        <div className="footer-right">
          <nav className="footer-nav" aria-label="Footer Navigation">
            {/* <a href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
            <a href="#privacy">Privacy</a> */}
          </nav>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
