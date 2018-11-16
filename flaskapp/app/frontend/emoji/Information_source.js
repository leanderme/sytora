import React from 'react';

export default function Information_source(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#4fd1d9" />
      <g fill="#fff">
        <path d="m27 27.8h10v24h-10z" />
        <circle cx={32} cy="17.2" r={5} />
      </g>
    </svg>
  );
}
