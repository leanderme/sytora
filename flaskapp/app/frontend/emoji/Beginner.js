import React from 'react';

export default function Beginner(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width={64} height={64} {...props}>
      <path fill="#24bac5" d="m32 20.8v41.2l20-18.8v-41.2z" />
      <path fill="#ffce31" d="m12 2v41.2l20 18.8v-41.2z" />
      <path fill="none" stroke="#3e4347" strokeLinejoin="round" strokeLinecap="round" strokeWidth={3} strokeMiterlimit={10} d="M32 20.8 12 2 12 43.2 32 62 52 43.2 52 2z" />
    </svg>
  );
}
