import React from 'react';

export default function Open_mouth(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#ffdd67" />
      <g fill="#664e27">
        <circle cx={32} cy="45.1" r={7} />
        <circle cx="20.2" cy={25} r="4.5" />
        <circle cx="42.7" cy={25} r="4.5" />
      </g>
    </svg>
  );
}
