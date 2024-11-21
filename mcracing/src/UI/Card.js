import React from 'react';
import PropTypes from 'prop-types';

export function Card({ children, className = '' }) {
  return (
    <div className={`border rounded-lg shadow-sm p-4 ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '' }) {
  return (
    <div className={`border-b pb-3 mb-3 ${className}`}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className = '' }) {
  return (
    <h3 className={`text-lg font-semibold ${className}`}>
      {children}
    </h3>
  );
}

export function CardContent({ children, className = '' }) {
  return (
    <div className={`${className}`}>
      {children}
    </div>
  );
}

// Prop Types for type checking
Card.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string
};

CardHeader.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string
};

CardTitle.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string
};

CardContent.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string
};