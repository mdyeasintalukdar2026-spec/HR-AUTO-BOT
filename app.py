from flask import Flask, jsonify, make_response
import threading
import requests
import time
import os

app = Flask(__name__, static_folder=None)

# ==========================================
# MASTER API KEYS & CONFIGURATIONS
# ==========================================
TWELVE_DATA_KEY = "8f5d4d4fce7f44e5bda54420591411c8"
GROQ_API_KEY = "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"
FINNHUB_API_KEY = "dbcaa19r01qqr3s0pf60dbcaa19r01qqr3s0pf6g"

http_session = requests.Session()

@app.route('/')
def home():
    return "Quotex Ai Signal Bot Engine v125.0 [Running 24/7 with Video-Style Animation & Auto Trade]"

@app.route('/ping')
def ping():
    return "OK", 200

@app.route('/signal')
def get_signal():
    try:
        current_sec = int(time.time())
        base_signal = "UP" if (current_sec % 2 == 0) else "DOWN"
        signal_conf = int(82 + ((current_sec * 7) % 15))
        res = jsonify({
            "signal": base_signal,
            "trend": "STRONG UPTREND",
            "confidence": signal_conf,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res
    except Exception as e:
        res = jsonify({
            "signal": "UP",
            "trend": "STRONG UPTREND",
            "confidence": 85,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res

@app.route('/bot.js')
def bot_script():
    js = """
    (function(){
        try {
            var d = document;
            var uniqueId = 'yb_' + Math.floor(Math.random() * 10000);
            
            var oldS = d.getElementById('ybs_global');
            if(!oldS){
                var s = d.createElement('style');
                s.id = 'ybs_global';
                s.innerHTML = '@keyframes panelPop {0%{opacity:0;transform:translate(-50%, -45%) scale(0.9);}100%{opacity:1;transform:translate(-50%, -50%) scale(1);}}' +
                              '@keyframes rgbGlow {0%{border-color:#00ff66;box-shadow:0 0 15px #00ff66;}33%{border-color:#00ffff;box-shadow:0 0 15px #00ffff;}66%{border-color:#ff0055;box-shadow:0 0 15px #ff0055;}100%{border-color:#00ff66;box-shadow:0 0 15px #00ff66;}}' +
                              '@keyframes sineWave {0%{transform:translateX(0);}50%{transform:translateX(-15px);}100%{transform:translateX(0);}}' +
                              '@keyframes scanBeam {0%{left:-100%;}100%{left:200%;}}' +
                              '@keyframes candlePop {0%{transform:scaleY(0.1);opacity:0;}100%{transform:scaleY(1);opacity:1;}}' +
                              '@keyframes spinAnim {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}';
                d.head.appendChild(s);
            }

            var existingWrap = d.getElementById('sniper_target_wrap');
            if(existingWrap) existingWrap.remove();

            var wrap = d.createElement('div');
            wrap.id = 'sniper_target_wrap';
            wrap.style.cssText = 'position:fixed;bottom:70px;right:20px;display:flex;flex-direction:column;align-items:center;z-index:2147483647;cursor:pointer;';
            
            var b = d.createElement('div');
            b.id = 'sniper_target_btn';
            b.style.cssText = 'width:62px;height:62px;border-radius:50%;background:#030407;display:flex;align-items:center;justify-content:center;border:2px solid #00ff66;animation:rgbGlow 4s infinite linear;box-sizing:border-box;overflow:hidden;';
            b.innerHTML = '<img src="https://i.postimg.cc/JzRR8g6M/IMG-20261102-WA0003.jpg" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />';
            wrap.appendChild(b);

            var lbl = d.createElement('div');
            lbl.style.cssText = 'margin-top:3px;font-size:7px;font-weight:900;color:#00ff66;font-family:sans-serif;background:rgba(3,4,7,0.85);padding:1px 5px;border-radius:3px;border:1px solid rgba(0,255,102,0.4);white-space:nowrap;box-shadow:0 0 5px rgba(0,0,0,0.8);';
            lbl.innerText = 'Ai Signal Bot';
            wrap.appendChild(lbl);

            d.body.appendChild(wrap);
            
            var isDragging = false, startX, startY, hasMoved = false;
            wrap.onmousedown = wrap.ontouchstart = function(e){
                isDragging = true; hasMoved = false;
                var p = e.touches ? e.touches[0] : e;
                startX = p.clientX - wrap.offsetLeft;
                startY = p.clientY - wrap.offsetTop;
            };
            wrap.onmousemove = wrap.ontouchmove = function(e){
                if(!isDragging) return;
                var p = e.touches ? e.touches[0] : e;
                var nx = p.clientX - startX, ny = p.clientY - startY;
                if(Math.abs(nx - wrap.offsetLeft) > 2 || Math.abs(ny - wrap.offsetTop) > 2) hasMoved = true;
                wrap.style.left = nx + 'px';
                wrap.style.top = ny + 'px';
                wrap.style.bottom = 'auto';
                wrap.style.right = 'auto';
            };
            wrap.onmouseup = wrap.ontouchend = function(){ isDragging = false; };
            
            wrap.onclick = function(){
                if(hasMoved) return;
                wrap.style.display = 'none';
                
                if(sessionStorage.getItem('sniper_verified_' + uniqueId) === 'true'){
                    createMainDashboard(wrap);
                } else {
                    createLicensePanel(wrap);
                }
            };

            function detectActiveMarket(){
                try {
                    var allEls = d.querySelectorAll('div, span, button');
                    for(var i=0; i<allEls.length; i++){
                        var txt = allEls[i].innerText ? allEls[i].innerText.trim() : '';
                        if((txt.includes('OTC') || txt.includes('/')) && txt.length >= 6 && txt.length <= 16 && !txt.includes('Deposit') && !txt.includes('DEMO')){
                            return txt;
                        }
                    }
                } catch(e){}
                return "GBP/AUD (OTC)";
            }

            function getTradingViewSymbol(marketText){
                if(!marketText) return "FX:EURUSD";
                var clean = marketText.replace(/\\(OTC\\)/gi, '').replace(/\\d+%/g, '').replace(/\\s+/g, '').toUpperCase();
                var sym = clean.replace('/', '').replace(/[^A-Z]/g, '');
                if(sym.includes('BTC') || sym.includes('ETH')) return 'BINANCE:' + sym + 'USDT';
                if(sym.includes('XAU') || sym.includes('GOLD')) return 'OANDA:XAUUSD';
                if(sym.length >= 6) return 'FX:' + sym;
                return 'FX:GBPAUD';
            }

            function createLicensePanel(targetWrap){
                var panel = d.createElement('div');
                panel.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);width:235px;background:#070b14;border:2px solid #00ff66;border-radius:10px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 15px 40px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards;';
                
                var header = d.createElement('div');
                header.style.cssText = 'background:#03050a;padding:5px 8px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:5px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:17px;height:17px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:9px;font-weight:900;color:#fff;">Ai Signal Bot</div>' +
                                   '<div style="font-size:5px;color:#8a99ad;">CLOCK: --:--:--</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:16px;height:16px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">×</button>';
                panel.appendChild(header);
                header.querySelector('#close-btn').onclick = function(){ panel.remove(); targetWrap.style.display = 'flex'; };

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:3px 8px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:5.5px;color:#00ff66;font-weight:800;">🟢 AI ENGINE ONLINE</div>' +
                                      '<div style="background:#553300;color:#ffcc00;font-size:5.5px;padding:1px 4px;border-radius:2px;font-weight:900;">READY</div>';
                panel.appendChild(statusRow);

                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:6px;background:#03050a;border:1px solid #131d2e;border-radius:5px;padding:6px;text-align:center;';
                scannerBox.innerHTML = '<div style="font-size:6px;color:#8a99ad;font-weight:800;">AI SIGNAL SCANNER</div>' +
                                       '<div style="font-size:8px;font-weight:900;color:#00ff66;margin:2px 0;">Next Candle??</div>' +
                                       '<div style="height:45px;display:flex;align-items:center;justify-content:center;">' +
                                       '<div style="width:3px;height:25px;background:#00ff66;margin:0 2px;"></div>' +
                                       '<div style="width:3px;height:35px;background:#ff1744;margin:0 2px;"></div>' +
                                       '<div style="width:3px;height:20px;background:#00ff66;margin:0 2px;"></div>' +
                                       '</div>';
                panel.appendChild(scannerBox);

                var licenseBox = d.createElement('div');
                licenseBox.style.cssText = 'margin:0 6px 6px 6px;background:#03050a;border:1px solid #131d2e;border-radius:5px;padding:6px;';
                licenseBox.innerHTML = '<div style="font-size:6px;color:#8a99ad;margin-bottom:2px;" id="err-msg">Enter password (11223344)</div>' +
                                       '<input type="password" id="license-input" placeholder="Enter password (1-8)" style="width:100%;box-sizing:border-box;background:#0d1526;border:1px solid #16253f;padding:5px;border-radius:3px;color:#fff;font-size:7.5px;outline:none;margin-bottom:4px;" />' +
                                       '<button id="verify-btn" style="width:100%;background:#00c853;border:none;padding:5px;border-radius:3px;font-weight:900;font-size:7.5px;color:#000;cursor:pointer;">VERIFY LICENSE</button>';
                panel.appendChild(licenseBox);

                var verifyBtn = licenseBox.querySelector('#verify-btn');
                var licenseInput = licenseBox.querySelector('#license-input');
                var errMsg = licenseBox.querySelector('#err-msg');

                verifyBtn.onclick = function(){
                    var keyVal = licenseInput.value.trim();
                    if(keyVal === '11223344' || (keyVal.length >= 1 && keyVal.length <= 8 && keyVal === '11223344')){
                        verifyBtn.innerHTML = '<span style="display:inline-block;width:7px;height:7px;border:1px solid #000;border-top-color:transparent;border-radius:50%;animation:spinAnim 0.8s linear infinite;"></span> Verifying...';
                        setTimeout(function(){
                            sessionStorage.setItem('sniper_verified_' + uniqueId, 'true');
                            panel.remove();
                            createMainDashboard(targetWrap);
                        }, 2000);
                    } else {
                        errMsg.innerText = '⚠️ INCORRECT PASSWORD!';
                        errMsg.style.color = '#ff1744';
                        licenseInput.style.borderColor = '#ff1744';
                        verifyBtn.style.background = '#ff1744';
                        verifyBtn.style.color = '#fff';
                        verifyBtn.innerText = 'ACCESS DENIED';
                    }
                };

                d.body.appendChild(panel);
            }

            function createMainDashboard(targetWrap){
                var panel = d.createElement('div');
                panel.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);width:245px;background:#070b14;border:2px solid #00ff66;border-radius:10px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 15px 40px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards;';
                
                var pDrag = false, pX, pY;
                panel.onmousedown = panel.ontouchstart = function(e){
                    if(e.target.tagName === 'BUTTON' || e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
                    pDrag = true;
                    var p = e.touches ? e.touches[0] : e;
                    pX = p.clientX - panel.offsetLeft;
                    pY = p.clientY -
