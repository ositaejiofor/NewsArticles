# Favicon & App Icon Setup

This folder contains all favicon and app icon files used across different platforms.

## 📂 Files

- favicon.ico → Classic favicon (16x16, 32x32) for old browsers.
- favicon-16x16.png → Small PNG favicon for browsers.
- favicon-32x32.png → Standard PNG favicon for browsers.
- apple-touch-icon.png (180x180) → Icon used when a user saves the site to their iOS home screen.
- android-chrome-192x192.png → Icon used for Android homescreen shortcuts.
- android-chrome-512x512.png → High-res Android icon (used for Progressive Web Apps).
- mstile-150x150.png → Windows tile icon (used when pinning site to Windows start menu).
- safari-pinned-tab.svg → Monochrome icon for Safari pinned tabs.
- site.webmanifest → Web App Manifest (defines icons and colors for Android/Chrome).
- browserconfig.xml → Config file for Windows tiles.

---

## ⚙️ HTML Integration

These links are already included in base.html:

<link rel="apple-touch-icon" sizes="180x180" href="{% static 'images/apple-touch-icon.png' %}">
<link rel="icon" type="image/png" sizes="32x32" href="{% static 'images/favicon-32x32.png' %}">
<link rel="icon" type="image/png" sizes="16x16" href="{% static 'images/favicon-16x16.png' %}">
<link rel="manifest" href="{% static 'images/site.webmanifest' %}">
<link rel="mask-icon" href="{% static 'images/safari-pinned-tab.svg' %}" color="#5bbad5">
<link rel="shortcut icon" href="{% static 'images/favicon.ico' %}">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="msapplication-config" content="{% static 'images/browserconfig.xml' %}">
<meta name="theme-color" content="#ffffff">

---

## ✅ Testing Checklist

### Desktop Browsers
- Favicon visible in browser tabs & bookmarks.
- Works in Chrome, Firefox, Edge, Safari.

### iOS Safari
- Add to Home Screen → uses apple-touch-icon.png.

### Android Chrome
- Add to Home Screen → uses android-chrome-192x192.png or 512x512.png.
- Colors come from site.webmanifest.

### Windows (Edge / Start Menu)
- Pinned site tile shows mstile-150x150.png.
- Tile background color matches #da532c.

---

## 🔍 Useful Tools
- RealFaviconGenerator Checker → https://realfavicongenerator.net/favicon_checker  
- FaviconTest → https://favicon-test.org  

---

### Notes
- Browsers cache favicons heavily — test in incognito/private mode.  
- Run `python manage.py collectstatic` in production to ensure favicons are served correctly.  
