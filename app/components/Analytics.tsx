import Script from 'next/script';

/**
 * Google Analytics 4 tracking.
 * Measurement ID is public — safe to hardcode.
 * Override via NEXT_PUBLIC_GA_ID env var if needed.
 */
const GA_ID = process.env.NEXT_PUBLIC_GA_ID || 'G-7BXF6SHQXQ';

export default function Analytics() {
  if (!GA_ID) return null;
  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
        strategy="afterInteractive"
      />
      <Script id="gtag-init" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${GA_ID}', {
            anonymize_ip: true,
            page_path: window.location.pathname,
          });
        `}
      </Script>
    </>
  );
}
