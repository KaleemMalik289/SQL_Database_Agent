import { useState, useEffect } from 'react';

/**
 * A reusable component that animates text as if it's being typed on a keyboard.
 * Scales perfectly across the application without CSS hacks.
 */
const TypewriterText = ({ text }) => {
  const [displayText, setDisplayText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    let timeout;
    
    const typingSpeed = isDeleting ? 50 : 150;
    const pauseBeforeDelete = 2000;
    const pauseBeforeStart = 500;

    if (!isDeleting && displayText === text) {
      timeout = setTimeout(() => setIsDeleting(true), pauseBeforeDelete);
    } else if (isDeleting && displayText === '') {
      timeout = setTimeout(() => setIsDeleting(false), pauseBeforeStart);
    } else {
      timeout = setTimeout(() => {
        setDisplayText(prev => {
          if (isDeleting) {
            return prev.slice(0, -1);
          } else {
            return text.slice(0, prev.length + 1);
          }
        });
      }, typingSpeed);
    }

    return () => clearTimeout(timeout);
  }, [displayText, isDeleting, text]);

  return (
    <div className="typewriter-container">
      <h1 className="animated-header">
        {displayText}
        <span className="cursor">|</span>
      </h1>
    </div>
  );
};

export default TypewriterText;
