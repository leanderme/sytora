import React from 'react';

export default function Arrow_up_down(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <circle cx={32} cy={32} r={30} fill="#4fd1d9" />
      <path fill="#fff" d="m32 52l16-15.5h-11.4v-9h11.4l-16-15.5-16 15.5h11.4v9h-11.4z" />
    </svg>
  );
}
