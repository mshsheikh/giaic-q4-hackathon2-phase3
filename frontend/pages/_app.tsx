import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';
import { BetterAuthProvider } from 'better-auth/react';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <BetterAuthProvider>
      <SessionProvider session={pageProps.session}>
        <Component {...pageProps} />
      </SessionProvider>
    </BetterAuthProvider>
  );
}