import React from 'react';

export default function Sparkles(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <path d="m22 0c0 16.9-9.1 32-22 32 12.9 0 22 15.1 22 32 0-16.9 9.1-32 22-32-12.9 0-22-15.1-22-32" fill="#ffe54d" />
      <path d="m53 0c0 8.4-4.6 16-11 16 6.4 0 11 7.6 11 16 0-8.4 4.6-16 11-16-6.4 0-11-7.6-11-16" fill="#6adbc6" />
      <path d="m48 32c0 8.4-4.6 16-11 16 6.4 0 11 7.6 11 16 0-8.4 4.6-16 11-16-6.4 0-11-7.6-11-16" fill="#ff73c0" />
    </svg>
  );
}
