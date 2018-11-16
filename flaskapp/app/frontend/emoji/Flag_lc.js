import React from 'react';

export default function Flag_lc(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#49c3f2" />
      <path fill="#fff" d="m32 15l-15 30h30z" />
      <path fill="#3e4347" d="m32 21l-12 24h24z" />
      <path fill="#ffce31" d="m32 33l-12 12h24z" />
    </svg>
  );
}
