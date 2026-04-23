'use client';

export default function NavSearch() {
  return (
    <input
      className="nav-search"
      type="text"
      placeholder="搜尋精油..."
      onKeyDown={(e) => {
        if (e.key === 'Enter') {
          const v = (e.target as HTMLInputElement).value.trim();
          if (v) location.href = '/search/?q=' + encodeURIComponent(v);
        }
      }}
    />
  );
}
