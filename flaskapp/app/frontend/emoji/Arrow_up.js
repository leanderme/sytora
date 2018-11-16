import React from 'react';

export default function Arrow_up(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#4fd1d9" />
      <path fill="#fff" d="m48 30.3l-16-15.3-16 15.3h10.6v18.7h10.3v-18.7z" />
    </svg>
  );
}
