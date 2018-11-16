import React from 'react';

export default function Pause_button(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#4fd1d9" />
      <g fill="#fff">
        <path d="m20 14h8v36h-8z" />
        <path d="m36 14h8v36h-8z" />
      </g>
    </svg>
  );
}
