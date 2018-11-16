import React from 'react';

export default function Flag_tn(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#ed4c5c" />
      <circle cx={32} cy={32} r="17.3" fill="#fff" />
      <circle cx={32} cy={32} r={13} fill="#ed4c5c" />
      <circle cx="35.5" cy={32} r="10.4" fill="#fff" />
      <path fill="#ed4c5c" d="m38.4 32l3.4-4.6-5.4 1.8-3.3-4.6v5.7l-5.4 1.7 5.4 1.7v5.7l3.3-4.6 5.4 1.8z" />
    </svg>
  );
}
