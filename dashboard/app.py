"""
NEXARA Kontrol Paneli v1.1
Çalıştır: streamlit run app.py
"""

import os
import sys
import json
import subprocess
import streamlit as st
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ─── Path & Env ───────────────────────────────────────────────────────────────
AGENTS_DIR = Path(__file__).parent.parent / "agents"
sys.path.insert(0, str(AGENTS_DIR))
load_dotenv(AGENTS_DIR / ".env")

# ─── Sayfa Ayarları ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXARA Dashboard",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0a0a0f; color: #e0e0e0; }
    .block-container { padding-top: 1.5rem; }

    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #4fc3f7; }
    .metric-label { font-size: 0.8rem; color: #90a4ae; margin-top: 4px; }

    .agent-running {
        background: #0d2b1e;
        border-left: 4px solid #66bb6a;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 8px;
    }
    .agent-offline {
        background: #1a1a1a;
        border-left: 4px solid #ef5350;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 8px;
    }
    .log-box {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 12px;
        font-family: monospace;
        font-size: 0.78rem;
        max-height: 280px;
        overflow-y: auto;
    }
    .post-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 14px;
        white-space: pre-wrap;
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 8px 0;
    }
    .key-ok   { color: #56d364; font-weight: 600; }
    .key-miss { color: #f85149; font-weight: 600; }
    h1, h2, h3 { color: #4fc3f7 !important; }
    div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "agents": {
            "telegram": {"status": "offline", "pid": None},
            "twitter":  {"status": "offline", "pid": None},
            "growth":   {"status": "offline", "pid": None},
        },
        "logs":         [],
        "news":         [],
        "gen_content":  {},   # {platform: content_text}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def log(msg: str, level: str = "INFO"):
    color = {"INFO":"#58a6ff","OK":"#56d364","WARN":"#d29922","ERR":"#f85149"}.get(level,"#58a6ff")
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.insert(0, f'<span style="color:{color}">[{ts}] {msg}</span>')
    st.session_state.logs = st.session_state.logs[:80]

def start_agent(name: str):
    """Gerçek subprocess olarak ajanı başlat."""
    script = str(AGENTS_DIR / f"{name}_agent.py")
    if not Path(script).exists():
        log(f"{name}_agent.py bulunamadı", "ERR")
        return
    try:
        p = subprocess.Popen(
            ["python", script],
            cwd=str(AGENTS_DIR),
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
        )
        st.session_state.agents[name]["status"] = "running"
        st.session_state.agents[name]["pid"] = p.pid
        log(f"{name} ajanı başlatıldı (PID {p.pid})", "OK")
    except Exception as e:
        log(f"{name} başlatılamadı: {e}", "ERR")

def stop_agent(name: str):
    """Ajanı durdur."""
    pid = st.session_state.agents[name].get("pid")
    if pid:
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
        except Exception:
            pass
    st.session_state.agents[name]["status"] = "offline"
    st.session_state.agents[name]["pid"] = None
    log(f"{name} ajanı durduruldu", "WARN")

def get_engine():
    """ContentEngine'i yükle, hata varsa None döndür."""
    try:
        from content_engine import ContentEngine
        return ContentEngine()
    except Exception as e:
        st.error(f"ContentEngine yüklenemedi: {e}")
        return None

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔷 NEXARA")
    st.markdown("**Kontrol Paneli v1.1**")
    st.divider()
    page = st.radio("Sayfa", [
        "📊 Dashboard", "🤖 Ajanlar",
        "✍️ İçerik",   "📰 Haberler", "⚙️ Ayarlar"
    ], label_visibility="collapsed")
    st.divider()
    addr = "0xa14F7e4DE163Bc05297AF005B6cD44A770842187"
    st.markdown(f"**Token:** `{addr[:10]}...{addr[-6:]}`")
    st.markdown(f"[Etherscan →](https://sepolia.etherscan.io/address/{addr})")
    st.divider()
    st.caption(f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}")

# ══════════════════════════════════════════════════════════
# SAYFA 1 — DASHBOARD
# ══════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown("# 📊 NEXARA Dashboard")

    # Metrik kartları
    cols = st.columns(5)
    for col, (val, label) in zip(cols, [
        ("100,000,000", "Toplam Arz"),
        ("—",           "Yakılan NXR"),
        ("—",           "Stake Edilen"),
        ("—",           "Holder"),
        ("4",           "Sözleşme"),
    ]):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div>'
                        f'<div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.divider()
    left, right = st.columns([2, 1])

    with left:
        st.markdown("### 🤖 Ajan Durumu")
        icons = {"telegram":"✈️ TELEGRAM","twitter":"🐦 TWITTER","growth":"📈 GROWTH"}
        for name, info in st.session_state.agents.items():
            s = info["status"]
            css = "agent-running" if s == "running" else "agent-offline"
            dot = "🟢 ÇALIŞIYOR" if s == "running" else "🔴 KAPALI"
            pid = f" — PID {info['pid']}" if info.get("pid") else ""
            st.markdown(
                f'<div class="{css}"><strong>{icons[name]}</strong> &nbsp; {dot}{pid}</div>',
                unsafe_allow_html=True
            )

    with right:
        st.markdown("### ⚡ Hızlı Eylemler")
        if st.button("🚀 Tüm Ajanları Başlat", use_container_width=True, type="primary"):
            for k in ["telegram","twitter","growth"]:
                start_agent(k)
            st.rerun()
        if st.button("⏹ Tüm Ajanları Durdur", use_container_width=True):
            for k in ["telegram","twitter","growth"]:
                stop_agent(k)
            st.rerun()

        st.divider()
        st.markdown("**📅 Bugünkü Takvim**")
        now_h = int(datetime.now().strftime("%H"))
        for t, lbl in [("08:00","☀️ Sabah"),("10:00","📰 Haber"),
                       ("13:00","📚 Eğitim"),("16:00","📰 Haber"),
                       ("17:00","💬 Etkileşim"),("21:00","📰 Akşam")]:
            h = int(t.split(":")[0])
            icon = "✅" if h < now_h else ("🔄" if h == now_h else "⏳")
            st.caption(f"{icon} {t} — {lbl}")

    st.divider()
    st.markdown("### 📋 Son Loglar")
    html = "<br>".join(st.session_state.logs[:20]) or "<i style='color:#555'>Henüz log yok</i>"
    st.markdown(f'<div class="log-box">{html}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SAYFA 2 — AJANLAR
# ══════════════════════════════════════════════════════════
elif page == "🤖 Ajanlar":
    st.markdown("# 🤖 Ajan Yönetimi")

    info_map = {
        "telegram": ("✈️","Telegram Community Manager",
                     ["Sorulara AI cevap","Yeni üye karşılama","/tier /stake /contract komutları","Spam filtresi","Günlük istatistik"]),
        "twitter":  ("🐦","Twitter Engagement Bot",
                     ["Mention'lara AI cevap","Otomatik tweetler","Airdrop katılımcı takibi"]),
        "growth":   ("📈","Growth & Content Agent",
                     ["RSS haber çekme","AI ile içerik üretimi","Kripto topluluğu yorumları","Haftalık rapor"]),
    }

    for name, (icon, desc, feats) in info_map.items():
        st.markdown(f"### {icon} {name.upper()} Ajanı")
        c1, c2, c3 = st.columns([3,1,1])
        with c1:
            s = st.session_state.agents[name]["status"]
            pid = st.session_state.agents[name].get("pid")
            st.markdown(f"{'🟢' if s=='running' else '🔴'} **{desc}** — {'ÇALIŞIYOR' if s=='running' else 'KAPALI'}"
                        + (f" (PID {pid})" if pid else ""))
            for f in feats:
                st.caption(f"  ✓ {f}")
        with c2:
            if st.button("▶ Başlat", key=f"st_{name}", use_container_width=True,
                         disabled=st.session_state.agents[name]["status"]=="running"):
                start_agent(name)
                st.rerun()
        with c3:
            if st.button("⏹ Durdur", key=f"sp_{name}", use_container_width=True,
                         disabled=st.session_state.agents[name]["status"]=="offline"):
                stop_agent(name)
                st.rerun()
        st.divider()

    st.markdown("### 💻 Manuel Başlatma (Terminal)")
    st.code("cd C:\\Users\\gokha\\Desktop\\nexara-token\\agents\npip install -r requirements.txt\npython start_all.py", language="bash")
    st.info("API keyleri .env dosyasına girilmeden ajanlar çalışmaz → ⚙️ Ayarlar sayfasına bak.")

# ══════════════════════════════════════════════════════════
# SAYFA 3 — İÇERİK
# ══════════════════════════════════════════════════════════
elif page == "✍️ İçerik":
    st.markdown("# ✍️ İçerik Yönetimi")

    tab1, tab2, tab3 = st.tabs(["🆕 İçerik Üret", "📤 Manuel Paylaş", "📅 Takvim"])

    # ── TAB 1: Üret ──────────────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            ctype = st.selectbox("İçerik Türü", [
                "Sabah Motivasyonu","Eğitim İçeriği",
                "Etkileşim Sorusu","Airdrop Duyurusu"
            ])
        with c2:
            platform = st.selectbox("Platform", ["Twitter","Telegram","Her İkisi"])

        if st.button("🔮 AI ile Üret", type="primary", use_container_width=True):
            engine = get_engine()
            if engine:
                type_map = {
                    "Sabah Motivasyonu":  engine.generate_morning_hype,
                    "Eğitim İçeriği":     engine.generate_educational_post,
                    "Etkileşim Sorusu":   engine.generate_engagement_post,
                }
                platforms = ["twitter","telegram"] if platform == "Her İkisi" else [platform.lower()]
                st.session_state.gen_content = {}
                with st.spinner("Claude AI yazıyor..."):
                    for p in platforms:
                        if ctype in type_map:
                            try:
                                txt = type_map[ctype](p)
                            except Exception as e:
                                txt = f"Hata: {e}"
                        else:
                            txt = f"[{ctype} — {p}]\nBu içerik türü yakında eklenecek."
                        st.session_state.gen_content[p] = txt

        # İçerikleri göster (session_state'den — buton sonrası kaybolmaz)
        if st.session_state.gen_content:
            for p, txt in st.session_state.gen_content.items():
                st.markdown(f"**{p.upper()}:**")
                st.markdown(f'<div class="post-box">{txt}</div>', unsafe_allow_html=True)
                st.caption(f"Karakter sayısı: {len(txt)}" + (" ⚠️ Twitter 280 limiti!" if len(txt)>280 and p=="twitter" else ""))
                if st.button(f"📋 Kopyala ({p})", key=f"copy_{p}"):
                    st.toast("Kopyalandı! (Ctrl+C ile alabilirsin)")
            log(f"İçerik üretildi: {ctype}", "OK")

    # ── TAB 2: Manuel ────────────────────────────────────────────────────────
    with tab2:
        st.markdown("### Manuel Post Gönder")
        manual = st.text_area("İçeriği yaz:", height=150,
                              placeholder="NXR hakkında bir şeyler yaz...\nMax 280 karakter Twitter için.")
        char_count = len(manual)
        st.caption(f"{'🔴' if char_count > 280 else '🟢'} {char_count}/280 karakter")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🐦 Twitter'da Paylaş", use_container_width=True, disabled=not manual):
                if not os.getenv("TWITTER_ACCESS_TOKEN"):
                    st.error("Twitter API keyleri .env dosyasında eksik!")
                elif char_count > 280:
                    st.error("280 karakteri aşıyor, kısalt!")
                else:
                    try:
                        import tweepy
                        tw = tweepy.Client(
                            consumer_key=os.getenv("TWITTER_API_KEY"),
                            consumer_secret=os.getenv("TWITTER_API_SECRET"),
                            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
                        )
                        tw.create_tweet(text=manual)
                        log(f"Tweet gönderildi: {manual[:50]}...", "OK")
                        st.success("✅ Tweet gönderildi!")
                    except Exception as e:
                        st.error(f"Twitter hatası: {e}")
        with c2:
            if st.button("✈️ Telegram'da Paylaş", use_container_width=True, disabled=not manual):
                if not os.getenv("TELEGRAM_BOT_TOKEN"):
                    st.error("Telegram bot token .env dosyasında eksik!")
                elif not os.getenv("TELEGRAM_CHANNEL_ID"):
                    st.error("Telegram kanal ID .env dosyasında eksik!")
                else:
                    try:
                        import asyncio
                        from telegram import Bot
                        async def send():
                            bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
                            await bot.send_message(chat_id=os.getenv("TELEGRAM_CHANNEL_ID"), text=manual)
                        asyncio.run(send())
                        log(f"Telegram mesajı gönderildi: {manual[:50]}...", "OK")
                        st.success("✅ Telegram'a gönderildi!")
                    except Exception as e:
                        st.error(f"Telegram hatası: {e}")

    # ── TAB 3: Takvim ────────────────────────────────────────────────────────
    with tab3:
        st.markdown("### 📅 Otomatik Paylaşım Takvimi")
        now_h = int(datetime.now().strftime("%H"))
        rows = [
            ("08:00","Sabah motivasyonu","Twitter + Telegram"),
            ("10:00","Haber + AI yorum","Twitter + Telegram"),
            ("13:00","Eğitim içeriği","Twitter"),
            ("16:00","Haber + AI yorum","Twitter + Telegram"),
            ("17:00","Etkileşim sorusu","Twitter + Telegram"),
            ("21:00","Akşam haberi","Twitter + Telegram"),
        ]
        for saat, icerik, platform in rows:
            h = int(saat.split(":")[0])
            icon = "✅" if h < now_h else ("🔄 ŞİMDİ" if h == now_h else "⏳")
            c1, c2, c3 = st.columns([1,2,2])
            with c1: st.write(f"**{saat}**")
            with c2: st.write(icerik)
            with c3: st.caption(f"{icon} {platform}")

# ══════════════════════════════════════════════════════════
# SAYFA 4 — HABERLER
# ══════════════════════════════════════════════════════════
elif page == "📰 Haberler":
    st.markdown("# 📰 Kripto Haberleri")
    st.caption("CoinTelegraph, CoinDesk, Decrypt — canlı RSS akışı")

    if st.button("🔄 Haberleri Yenile", type="primary"):
        engine = get_engine()
        if engine:
            with st.spinner("Haberler çekiliyor..."):
                try:
                    news = engine.fetch_latest_news(max_per_feed=3)
                    st.session_state.news = news
                    log(f"{len(news)} haber çekildi", "OK")
                    st.success(f"{len(news)} haber bulundu!")
                except Exception as e:
                    st.error(f"Haber çekme hatası: {e}")
        else:
            st.warning("ANTHROPIC_API_KEY .env dosyasına ekle.")

    if st.session_state.news:
        for i, item in enumerate(st.session_state.news[:12]):
            title = item.get("title","")[:75]
            source = item.get("source","?")
            with st.expander(f"📰 [{source}] {title}"):
                st.caption(item.get("date",""))
                summary = item.get("summary","")[:300]
                st.write(summary + ("..." if len(item.get("summary","")) > 300 else ""))
                link = item.get("link","#")
                if link != "#":
                    st.markdown(f"[Haberi Oku →]({link})")
                st.divider()
                c1, c2 = st.columns(2)
                for col, plat, key in [(c1,"twitter",f"tw_{i}"), (c2,"telegram",f"tg_{i}")]:
                    with col:
                        if st.button(f"{'🐦' if plat=='twitter' else '✈️'} {plat.capitalize()} Yorumu Üret",
                                     key=key, use_container_width=True):
                            engine = get_engine()
                            if engine:
                                with st.spinner("AI yazıyor..."):
                                    try:
                                        post = engine.generate_news_post(item, plat)
                                        st.markdown(f'<div class="post-box">{post}</div>', unsafe_allow_html=True)
                                        st.caption(f"{len(post)} karakter")
                                        log(f"Haber yorumu üretildi ({plat})", "OK")
                                    except Exception as e:
                                        st.error(str(e))
    else:
        st.info("👆 'Haberleri Yenile' butonuna bas")

# ══════════════════════════════════════════════════════════
# SAYFA 5 — AYARLAR
# ══════════════════════════════════════════════════════════
elif page == "⚙️ Ayarlar":
    st.markdown("# ⚙️ Ayarlar")
    tab1, tab2 = st.tabs(["🔑 API Keyleri", "📋 Sistem Bilgisi"])

    with tab1:
        st.markdown("### API Key Durumu")
        keys = {
            "ANTHROPIC_API_KEY":      ("Claude AI — İçerik üretimi",  "console.anthropic.com"),
            "TELEGRAM_BOT_TOKEN":     ("Telegram Bot Token",           "@BotFather"),
            "TELEGRAM_CHANNEL_ID":    ("Telegram Kanal/Grup ID",       "Grupta /start yaz"),
            "TWITTER_BEARER_TOKEN":   ("Twitter Bearer Token",         "developer.twitter.com"),
            "TWITTER_API_KEY":        ("Twitter API Key",              "developer.twitter.com"),
            "TWITTER_API_SECRET":     ("Twitter API Secret",           "developer.twitter.com"),
            "TWITTER_ACCESS_TOKEN":   ("Twitter Access Token",         "developer.twitter.com"),
            "TWITTER_ACCESS_SECRET":  ("Twitter Access Secret",        "developer.twitter.com"),
        }
        all_ok = True
        for key, (label, source) in keys.items():
            val = os.getenv(key)
            ok = bool(val)
            if not ok: all_ok = False
            c1, c2, c3 = st.columns([3,1,2])
            with c1: st.write(f"**{label}**")
            with c2: st.markdown(
                f'<span class="{"key-ok" if ok else "key-miss"}">{"✅ Var" if ok else "❌ Eksik"}</span>',
                unsafe_allow_html=True)
            with c3: st.caption(f"→ {source}")

        st.divider()
        if all_ok:
            st.success("✅ Tüm API keyleri mevcut — Ajanlar çalışmaya hazır!")
        else:
            st.warning("⚠️ Eksik keyler var. Ajanlar tam çalışmaz.")

        st.markdown("### .env Dosyası")
        st.code(str(AGENTS_DIR / ".env"))
        st.info("Bu dosyayı Notepad ile aç, API keylerini gir, kaydet, dashboard'u yenile.")

        if st.button("📂 .env Klasörünü Aç"):
            subprocess.Popen(f'explorer "{AGENTS_DIR}"')

    with tab2:
        st.markdown("### 📦 Proje Durumu")
        files = [
            ("contracts/NexaraToken.sol",    "✅","Ana token sözleşmesi"),
            ("contracts/NexaraStaking.sol",  "✅","Staking sözleşmesi"),
            ("contracts/NexaraAccess.sol",   "✅","Bot erişim sistemi"),
            ("contracts/NexaraTreasury.sol", "✅","Gelir paylaşımı"),
            ("agents/telegram_agent.py",     "✅","Telegram botu"),
            ("agents/twitter_agent.py",      "✅","Twitter botu"),
            ("agents/growth_agent.py",       "✅","Growth motoru"),
            ("agents/content_engine.py",     "✅","AI içerik üretimi"),
            ("WHITEPAPER.md",                "✅","Whitepaper"),
        ]
        for path, status, desc in files:
            full = Path(__file__).parent.parent / path
            exists = "✅" if full.exists() else "❌"
            st.markdown(f"{exists} `{path}` — {desc}")

        st.divider()
        st.markdown("### 🔷 Deploy Edilen Sözleşmeler (Sepolia)")
        st.code(
            "Token:    0xa14F7e4DE163Bc05297AF005B6cD44A770842187\n"
            "Staking:  0xa589014ee01E4F4f473ABD5587d304fA4879F5E4\n"
            "Ağ:       Ethereum Sepolia Testnet"
        )
        st.markdown("[Etherscan'da Gör →](https://sepolia.etherscan.io/address/0xa14F7e4DE163Bc05297AF005B6cD44A770842187)")
