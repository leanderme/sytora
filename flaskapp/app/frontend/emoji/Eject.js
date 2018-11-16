import React from 'react';

export default function Eject(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#4fd1d9" />
      <g fill="#fff">
        <path d="m16 33.6l16-19 16 19z" />
        <path d="m16 37.6h32v5.7h-32z" />
      </g>
    </svg>
  );
}
