import React from 'react';

export default function Flag_so(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#42ade2" />
      <path fill="#fff" d="m32 39.2l9.9 7.1-3.8-11.5 9.9-7.1h-12.2l-3.8-11.4-3.8 11.4h-12.2l9.8 7.1-3.7 11.5z" />
    </svg>
  );
}
