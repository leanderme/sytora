import React from 'react';

export default function Necktie(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <path d="M64,59.7c0,2.4-2.2,4.3-4.9,4.3H4.9C2.2,64,0,62.1,0,59.7V9.1c0-2.4,2.2-4.3,4.9-4.3h54.2
      		c2.7,0,4.9,1.9,4.9,4.3V59.7z" fill="#d0d0d0" />
      <g fill="#94989b">
        <path d="m48.9 9.5h-33.8l3.3-9.5h27.2z" />
        <path d="m18.4 2.9l-3.3 6.6 12 17.7v-12.1z" />
        <path d="m45.6 2.9l3.3 6.6-12 17.7v-12.1z" />
      </g>
      <g fill="#fff">
        <path d="m18.4 0l-3.3 9.5 12 14.9v-12.2z" />
        <path d="m45.6 0l3.3 9.5-12 14.9v-12.2z" />
      </g>
      <path fill="#42ade2" d="m37.7 24.4h-11.4l-3.3 32.4 9.1 7.2 8.9-7.2z" />
      <path d="m38.1 27.6l-.3-3.3h-11.5l-.3 3.3c2.4 1.8 9.5 1.7 12.1 0" fill="#428bc1" />
      <path d="m38.6 24.4c-2.2 2.2-11.2 2.4-13.1 0-2-2.5 1.6-12.2 1.6-12.2s3.7 1.4 4.9 1.4 4.9-1.4 4.9-1.4 4 9.9 1.7 12.2" fill="#42ade2" />
    </svg>
  );
}
