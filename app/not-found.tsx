import type { Metadata } from 'next';
import NavSearch from './components/NavSearch';

export const metadata: Metadata = {
  title: { absolute: '找不到頁面 | 精油能量圖譜' },
  description: '您訪問的頁面不存在。探索精油能量圖譜：400+ 精油化學分類、芳療應用、安全指南。',
  robots: { index: false, follow: true },
};

export default function NotFound() {
  return (
    <section style={{ maxWidth: 720, margin: '80px auto', padding: '0 24px', textAlign: 'center' }}>
      <div style={{ fontSize: 96, lineHeight: 1, marginBottom: 16 }}>🌿</div>
      <h1 style={{ fontSize: 42, marginBottom: 16, color: 'var(--green-dark)' }}>找不到這一頁</h1>
      <p style={{ fontSize: 18, color: 'var(--text-mid)', marginBottom: 40, lineHeight: 1.7 }}>
        您要找的頁面可能已搬移或不存在。<br />
        試試下方的熱門連結或搜尋精油：
      </p>

      <div style={{ marginBottom: 40 }}>
        <NavSearch />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 40 }}>
        <a href="/" style={{ padding: '20px 16px', background: 'var(--beige-light)', borderRadius: 12, textDecoration: 'none', color: 'inherit' }}>
          <div style={{ fontSize: 28, marginBottom: 6 }}>🏠</div>
          <strong>首頁</strong>
          <p style={{ fontSize: 13, color: 'var(--text-mid)', marginTop: 4 }}>從這開始認識精油</p>
        </a>
        <a href="/oils/" style={{ padding: '20px 16px', background: 'var(--beige-light)', borderRadius: 12, textDecoration: 'none', color: 'inherit' }}>
          <div style={{ fontSize: 28, marginBottom: 6 }}>🌿</div>
          <strong>精油索引</strong>
          <p style={{ fontSize: 13, color: 'var(--text-mid)', marginTop: 4 }}>400+ 精油化學分子</p>
        </a>
        <a href="/encyclopedia/" style={{ padding: '20px 16px', background: 'var(--beige-light)', borderRadius: 12, textDecoration: 'none', color: 'inherit' }}>
          <div style={{ fontSize: 28, marginBottom: 6 }}>📚</div>
          <strong>大百科</strong>
          <p style={{ fontSize: 13, color: 'var(--text-mid)', marginTop: 4 }}>系統知識體系</p>
        </a>
        <a href="/aromatherapy/" style={{ padding: '20px 16px', background: 'var(--beige-light)', borderRadius: 12, textDecoration: 'none', color: 'inherit' }}>
          <div style={{ fontSize: 28, marginBottom: 6 }}>🕯️</div>
          <strong>芳療應用</strong>
          <p style={{ fontSize: 13, color: 'var(--text-mid)', marginTop: 4 }}>擴香/按摩/DIY</p>
        </a>
        <a href="/safety/" style={{ padding: '20px 16px', background: 'var(--beige-light)', borderRadius: 12, textDecoration: 'none', color: 'inherit' }}>
          <div style={{ fontSize: 28, marginBottom: 6 }}>⚠️</div>
          <strong>安全指南</strong>
          <p style={{ fontSize: 13, color: 'var(--text-mid)', marginTop: 4 }}>使用禁忌/劑量</p>
        </a>
        <a href="/article-beginners/" style={{ padding: '20px 16px', background: 'var(--beige-light)', borderRadius: 12, textDecoration: 'none', color: 'inherit' }}>
          <div style={{ fontSize: 28, marginBottom: 6 }}>🌱</div>
          <strong>新手入門</strong>
          <p style={{ fontSize: 13, color: 'var(--text-mid)', marginTop: 4 }}>5 瓶必備精油</p>
        </a>
      </div>

      <p style={{ fontSize: 13, color: 'var(--text-mid)' }}>
        錯誤代碼：404 Not Found
      </p>
    </section>
  );
}
