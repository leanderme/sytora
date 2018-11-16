import React from 'react';

export default function Gem(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <path fill="#9450e0" d="M41 4 23 4 2 20.1 32 60 62 20.1z" />
      <g fill="#c28fef">
        <path d="m32 60l12.5-39.9h-25.7z" />
        <path d="M9.5 9.5 2 20.1 18.8 20.1 23 4z" />
        <path d="M54.5 9.5 41 4 44.5 20.1 62 20.1z" />
      </g>
    </svg>
  );
}
