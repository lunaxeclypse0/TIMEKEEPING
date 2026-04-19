from __future__ import annotations
import streamlit.components.v1 as components


# FIX: Added logo_mime param — was hardcoded "image/png", broke JPEG logos.
def render_top_banner(logo_b64: str | None, logo_mime: str = "image/png") -> None:
    if logo_b64:
        logo_html = (
            f'<img src="data:{logo_mime};base64,{logo_b64}" '
            f'alt="GoClinic Logo" class="hero-logo">'
        )
    else:
        logo_html = '<div class="hero-fallback">🏥</div>'

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; font-family: Inter, -apple-system, sans-serif; }}

  .hero {{
    width: 100%;
    height: 160px;
    background: linear-gradient(120deg, #0c1f4a 0%, #1740a0 55%, #2563eb 100%);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 28px;
    gap: 16px;
    box-shadow: 0 10px 36px rgba(21,60,160,0.32);
    position: relative;
    overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
    pointer-events: none;
  }}
  .hero::after {{
    content: '';
    position: absolute;
    bottom: -80px; left: 160px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.03);
    pointer-events: none;
  }}
  .hero-left {{
    width: 220px;
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }}
  .hero-logo {{
    max-width: 210px;
    max-height: 110px;
    object-fit: contain;
    filter: drop-shadow(0 2px 8px rgba(0,0,0,0.22));
  }}
  .hero-fallback {{
    width: 84px; height: 84px;
    border-radius: 18px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.2rem;
  }}
  .hero-center {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    z-index: 1;
  }}
  .hero-title {{
    font-size: 2.2rem;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.8px;
    line-height: 1;
    text-shadow: 0 2px 12px rgba(0,0,0,0.18);
  }}
  .hero-title span {{ color: #93c5fd; }}
  .hero-tagline {{
    font-size: 0.74rem;
    color: rgba(255,255,255,0.52);
    margin-top: 7px;
    font-weight: 500;
    letter-spacing: 0.5px;
  }}
  .hero-right {{
    width: 210px;
    display: flex;
    justify-content: flex-end;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
  }}
  .clock-card {{
    width: 196px;
    height: 110px;
    border-radius: 18px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.20);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.14), 0 4px 16px rgba(0,0,0,0.14);
  }}
  .clock-date {{
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
  }}
  .clock-time {{
    font-size: 2.3rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1;
    letter-spacing: 1.5px;
    font-variant-numeric: tabular-nums;
    font-feature-settings: 'tnum';
  }}
  .clock-label {{
    font-size: 0.60rem;
    font-weight: 800;
    letter-spacing: 3px;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
  }}
</style>
</head>
<body>
  <div class="hero">
    <div class="hero-left">{logo_html}</div>
    <div class="hero-center">
      <h1 class="hero-title">Timekeeping <span>System</span></h1>
      <div class="hero-tagline">Automated Attendance Processing &amp; DTR Generator</div>
    </div>
    <div class="hero-right">
      <div class="clock-card">
        <div class="clock-date" id="live-date">Loading...</div>
        <div class="clock-time" id="live-time">00:00:00</div>
        <div class="clock-label">Live Clock</div>
      </div>
    </div>
  </div>
  <script>
    var DAYS   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    function pad(n) {{ return String(n).padStart(2,'0'); }}
    function tick() {{
      var now = new Date();
      var timeEl = document.getElementById('live-time');
      var dateEl = document.getElementById('live-date');
      if (!timeEl) return;
      timeEl.textContent = pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds());
      dateEl.textContent = DAYS[now.getDay()] + ', ' + MONTHS[now.getMonth()] + ' ' + now.getDate();
    }}
    tick();
    setInterval(tick, 1000);
  </script>
</body>
</html>"""

    components.html(html, height=178, scrolling=False)