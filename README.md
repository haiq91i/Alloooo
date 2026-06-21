# 🤖 ALL-IN-ONE TELEGRAM MEDIA BOT

Namaste! 👋 Ye tumhara **complete Telegram bot** hai jisme Image, PDF, Audio, Sticker, Converter, aur Utility tools sab kuch hai.

---

## 📦 **BOT ME KYA-KYA HAI**

### 🖼 Image Tools
- Image → Sticker
- Image → PNG/JPG/WebP
- Resize, Crop, Rotate, Compress
- Photo Collage Maker
- Add Text on Image
- Image → PDF / Multiple Images → PDF

### 🎵 Audio Tools
- Audio Trim
- Merge Audio Files
- Audio Speed Changer
- Volume Increase/Decrease

### 🎭 Sticker Tools
- Image → Sticker
- Sticker → Image
- Sticker Resize

### 📄 PDF Tools
- Merge PDF / Split PDF / Compress PDF
- Image → PDF / PDF → Images

### 🔄 Converters
- JPG ↔ PNG ↔ WebP

### 🛠 Utility Tools
- QR Code Generator/Scanner
- ZIP Create/Extract
- File Renamer

### ⚙ Extra
- Settings (default format/quality)
- Cancel Task (`/cancel`)
- Quick Menu Bar (har result ke sath buttons)

> ⚠️ **NOTE:** Video Tools (compress, merge, GIF banana) **jaan-bujh kar nahi rakhe** kyunki Railway free tier (512MB RAM) pe video processing se bot **crash ho jata hai**. Baaki sab kuch chalega smoothly!

---

## 🚀 **STEP-BY-STEP: BOT KAISE LIVE KARE (Mobile se)**

### **STEP 1: GitHub Account Banao** (agar nahi hai)
1. Mobile browser me jao: **github.com**
2. **Sign up** karo (free hai)
3. Email verify karo

### **STEP 2: GitHub pe Repository Banao**
1. GitHub app/website me login karo
2. **+ (plus icon)** dabao → **New repository**
3. Naam do: `my-telegram-bot` (ya kuch bhi)
4. **Public** select karo
5. **Create repository** dabao

### **STEP 3: Files Upload Karo**
1. Is zip ko apne phone me **extract** karo (koi bhi File Manager app se, ya "ZArchiver" app install karke)
2. GitHub repository me jao → **Add file** → **Upload files**
3. Saari files aur folders (handlers wala folder bhi) select karo aur upload karo
4. Niche **Commit changes** dabao

> 💡 Tip: Agar bulk upload me dikkat ho to GitHub mobile browser ke "Desktop site" mode me try karo (Chrome menu → Desktop site)

### **STEP 4: Railway Account Banao**
1. Browser me jao: **railway.app**
2. **Login with GitHub** se sign up karo (same GitHub account se)
3. Free signup hone par kuch free credit milta hai

### **STEP 5: Railway pe Deploy Karo**
1. Railway dashboard me **New Project** dabao
2. **Deploy from GitHub repo** choose karo
3. Apna `my-telegram-bot` repository select karo
4. Railway automatically detect kar lega ki ye Python project hai (nixpacks.toml se)
5. Build start ho jayega (2-3 min lagega)

### **STEP 6: BOT_TOKEN Set Karo (SABSE IMPORTANT STEP)**
1. Railway project khol ke **Variables** tab pe jao
2. **New Variable** dabao
3. Name: `BOT_TOKEN`
4. Value: apna BotFather wala token paste karo (jo tumhare paas already hai)
5. **Add** dabao
6. Bot automatically restart ho jayega naye variable ke sath

### **STEP 7: Check Karo Bot Chal Raha Hai**
1. Railway me **Deployments** tab pe jao
2. Latest deployment kholo → **View Logs**
3. Agar ye line dikhe: `🤖 Bot chalu ho gaya hai! Polling shuru...` — **MATLAB SAB THEEK HAI!** ✅
4. Ab Telegram me apne bot ko kholo aur **/start** bhejo

---

## ⚠️ **COMMON PROBLEMS AUR SOLUTIONS**

### ❌ Bot start nahi ho raha / Logs me error
- **BOT_TOKEN** sahi se daala hai check karo (extra space na ho)
- Logs me exact error padho - usually "ModuleNotFoundError" hota hai matlab requirements.txt sahi se install nahi hua

### ❌ "Module not found" error
- Railway ke **Settings** → **Redeploy** dabao
- Ya `nixpacks.toml` file check karo ki sahi se upload hui hai

### ❌ QR Scanner kaam nahi kar raha
- Ye `zbar` library maangta hai jo `nixpacks.toml` me already add hai
- Agar fir bhi error aaye to Railway logs check karo

### ❌ PDF → Images kaam nahi kar raha
- Ye `poppler` library maangta hai jo `nixpacks.toml` me already add hai

### ❌ Free credit khatam ho gaya
- Railway free tier me $5/month credit milta hai
- Agar khatam ho jaye to next month wait karo, ya paid plan lo
- Bot ko light rakhne ke liye hi humne Video Tools nikale the

### ❌ File "too large" error
- Bot ka max limit **20MB** hai (Telegram Bot API ki limitation hai, isse zyada nahi badha sakte)

---

## 📁 **FOLDER STRUCTURE** (samajhne ke liye)

```
telegram-bot/
├── bot.py                 ← Main file (sab kuch yaha se chalta hai)
├── config.py               ← Settings (token, limits)
├── keyboards.py             ← Saare buttons/menus
├── state_manager.py         ← User ka current mode track karta hai
├── helpers.py                ← Common functions
├── requirements.txt          ← Python libraries list
├── Procfile                  ← Railway ko batata hai kaise start kare
├── railway.json               ← Railway config
├── nixpacks.toml               ← System libraries (ffmpeg, poppler, zbar)
├── .env.example                 ← Token kaise set kare (example)
└── handlers/
    ├── image_tools.py            ← Image processing functions
    ├── pdf_tools.py                ← PDF processing functions
    ├── audio_tools.py               ← Audio processing functions
    └── utility_tools.py              ← QR/ZIP functions
```

---

## 🎯 **BOT KAISE USE KARE (User ke liye)**

1. Telegram me bot kholo → **/start** bhejo
2. Menu se category choose karo (Image/PDF/Audio/etc)
3. Tool choose karo (e.g. "Resize")
4. Bot maangega file → bhej do
5. Agar extra info chahiye (size, text) → bot pucheha, type kar do
6. Result mil jayega + **Quick Menu Bar** bhi sath me aayega taki turant agla kaam kar sako

**Commands:**
- `/start` — Bot shuru karo
- `/menu` — Kabhi bhi main menu pe wapas
- `/help` — Help dekho
- `/cancel` — Current task cancel karo

---

## 💡 **AAGE KYA KAR SAKTE HO (Future Improvements)**

- Agar Railway paid plan loge to **Video Tools wapas add** kar sakte hain
- Database add kar ke user history save kar sakte ho
- Multiple language support add kar sakte ho

Koi bhi dikkat aaye to Railway ke **Logs** section sabse pehle check karna — wahi se 90% problems samajh aa jaati hai! 🚀

**All the best bhai! 🔥**
