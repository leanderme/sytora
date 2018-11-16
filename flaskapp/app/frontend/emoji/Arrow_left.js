import React from 'react';

export default function Arrow_left(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#4fd1d9" />
      <path fill="#fff" d="m30.3 16l-15.3 16 15.3 16v-10.6h18.7v-10.3h-18.7z" />
    </svg>
  );
}
