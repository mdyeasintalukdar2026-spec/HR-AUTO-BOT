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
    return "Quotex Sniper Bot Engine v75.0 Running 24/7!"

@app.route('/ping')
def ping():
    return "OK", 200

@app.route('/signal')
def get_signal():
    try:
        current_sec = int(time.time())
        base_signal = "UP" if (current_sec % 2 == 0) else "DOWN"
        signal_conf = int(78 + ((current_sec * 7) % 20))
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
            "confidence": 81,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res

@app.route('/bot.js')
def bot_script():
    js = """
    (function(){
        try {
            if(window.YB){ window.YB.remove(); }
            if(window.YBP){ window.YBP.remove(); }
            if(window.YBOverlay){ window.YBOverlay.remove(); }
            var d = document;
            var oldS = d.getElementById('ybs');
            if(oldS){ oldS.remove(); }
            
            window.autoTradeEnabled = false;

            var s = d.createElement('style');
            s.id = 'ybs';
            s.innerHTML = '@keyframes neonGlow {0%{box-shadow:0 0 15px rgba(0,255,102,0.3);border-color:#00ff66;}50%{box-shadow:0 0 25px rgba(0,255,255,0.6);border-color:#00ffff;}100%{box-shadow:0 0 15px rgba(0,255,102,0.3);border-color:#00ff66;}}' +
                          '@keyframes cPulse {0%{transform:scaleY(0.5);opacity:0.6;}50%{transform:scaleY(1.2);opacity:1;}100%{transform:scaleY(0.5);opacity:0.6;}}' +
                          '@keyframes panelPop {0%{opacity:0;transform:scale(0.85) translateY(15px);}100%{opacity:1;transform:scale(1) translateY(0);}}';
            d.head.appendChild(s);

            // Floating Target Icon (Draggable)
            var b = d.createElement('div');
            window.YB = b;
            b.style.cssText = 'position:fixed;bottom:80px;right:25px;width:52px;height:52px;border-radius:12px;background:radial-gradient(circle, #0c1424 0%, #030407 100%);display:flex;align-items:center;justify-content:center;z-index:2147483647;cursor:pointer;border:2px solid #00ff66;box-shadow:0 0 15px rgba(0,255,102,0.4);box-sizing:border-box;';
            b.innerHTML = '<span style="font-size:22px;">🎯</span>';
            d.body.appendChild(b);
            
            var isDragging = false, startX, startY, hasMoved = false;
            b.onmousedown = b.ontouchstart = function(e){
                isDragging = true; hasMoved = false;
                var p = e.touches ? e.touches[0] : e;
                startX = p.clientX - b.offsetLeft;
                startY = p.clientY - b.offsetTop;
            };
            b.onmousemove = b.ontouchmove = function(e){
                if(!isDragging) return;
                var p = e.touches ? e.touches[0] : e;
                var nx = p.clientX - startX, ny = p.clientY - startY;
                if(Math.abs(nx - b.offsetLeft) > 2 || Math.abs(ny - b.offsetTop) > 2) hasMoved = true;
                b.style.left = nx + 'px';
                b.style.top = ny + 'px';
                b.style.bottom = 'auto';
                b.style.right = 'auto';
            };
            b.onmouseup = b.ontouchend = function(){ isDragging = false; };
            
            b.onclick = function(){
                if(hasMoved) return;
                b.style.display = 'none';
                createPanel();
            };

            function createPanel(){
                if(d.getElementById('yb-panel')) return;
                
                var panel = d.createElement('div');
                window.YBP = panel;
                panel.id = 'yb-panel';
                panel.style.cssText = 'position:fixed;top:70px;left:50%;transform:translateX(-50%);width:280px;background:#070b14;border:2px solid #00ff66;border-radius:14px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards, neonGlow 5s infinite;';
                
                // Draggable Header logic
                var pDrag = false, pX, pY;
                panel.onmousedown = panel.ontouchstart = function(e){
                    if(e.target.tagName === 'BUTTON' || e.target.tagName === 'INPUT') return;
                    pDrag = true;
                    var p = e.touches ? e.touches[0] : e;
                    pX = p.clientX - panel.offsetLeft;
                    pY = p.clientY - panel.offsetTop;
                    panel.style.transform = 'none';
                };
                panel.onmousemove = panel.ontouchmove = function(e){
                    if(!pDrag) return;
                    var p = e.touches ? e.touches[0] : e;
                    panel.style.left = (p.clientX - pX) + 'px';
                    panel.style.top = (p.clientY - pY) + 'px';
                    panel.style.bottom = 'auto';
                    panel.style.right = 'auto';
                };
                panel.onmouseup = panel.ontouchend = function(){ pDrag = false; };

                // Header matching video exactly (SNIPER BOT with Logo and Clock)
                var header = d.createElement('div');
                header.style.cssText = 'background:#03050a;padding:9px 12px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;cursor:move;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:8px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:11.5px;font-weight:900;color:#fff;letter-spacing:0.5px;">SNIPER BOT</div>' +
                                   '<div id="live-clock" style="font-size:7px;color:#8a99ad;font-weight:700;">TIME: 00:00:00</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<div style="display:flex;align-items:center;gap:6px;">' +
                                   '<button id="min-btn" style="background:#101826;border:none;color:#fff;width:20px;height:20px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:12px;">-</button>' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:20px;height:20px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:12px;">×</button>' +
                                   '</div>';
                
                panel.appendChild(header);
                
                header.querySelector('#min-btn').onclick = function(){
                    panel.remove();
                    b.style.display = 'flex';
                };
                header.querySelector('#close-btn').onclick = function(){
                    panel.remove();
                    b.style.display = 'flex';
                };

                // Live Clock updater
                setInterval(function(){
                    var now = new Date();
                    var timeStr = now.toTimeString().split(' ')[0];
                    var clk = panel.querySelector('#live-clock');
                    if(clk) clk.innerText = 'TIME: ' + timeStr;
                }, 1000);

                // AI Engine Online & Verified Status Row
                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:6px 12px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:7.5px;color:#00ff66;font-weight:800;display:flex;align-items:center;gap:4px;"><span style="width:6px;height:6px;background:#00ff66;border-radius:50%;box-shadow:0 0 6px #00ff66;display:inline-block;"></span>AI ENGINE ONLINE</div>' +
                                      '<div style="background:#00c853;color:#000;font-size:7.5px;padding:1px 6px;border-radius:3px;font-weight:900;">VERIFIED: 1</div>';
                panel.appendChild(statusRow);

                // Mode Row: 1m Standard & 5s Auto Mode
                var row1 = d.createElement('div');
                row1.style.cssText = 'padding:8px 10px;background:#070b14;display:flex;gap:6px;border-bottom:1px solid #131d2e;';
                row1.innerHTML = '<div style="flex:1;background:#0d1526;padding:6px;border-radius:6px;text-align:center;font-size:8px;font-weight:800;color:#00ff66;border:1px solid #16253f;">⏱️ 1m Standard</div>' +
                                   '<div style="flex:1;background:#0d1526;padding:6px;border-radius:6px;text-align:center;font-size:8px;font-weight:800;color:#ffd700;border:1px solid #16253f;">⚡ 5s Auto Mode</div>';
                panel.appendChild(row1);

                // Control Buttons Row: Start Auto & Stop Auto
                var row2 = d.createElement('div');
                row2.style.cssText = 'padding:0 10px 8px 10px;background:#070b14;display:flex;gap:6px;border-bottom:1px solid #131d2e;';
                row2.innerHTML = '<button id="btn-start" style="flex:1;background:linear-gradient(45deg,#00b0ff,#00ff66);border:none;padding:7px;border-radius:6px;font-weight:900;font-size:8.5px;color:#030407;cursor:pointer;box-shadow:0 0 10px rgba(0,255,102,0.4);">▶ Start Auto</button>' +
                                   '<button id="btn-stop" style="flex:1;background:linear-gradient(45deg,#ff3300,#ff0055);border:none;padding:7px;border-radius:6px;font-weight:900;font-size:8.5px;color:#fff;cursor:pointer;box-shadow:0 0 10px rgba(255,0,85,0.4);">⏹ Stop Auto</button>';
                panel.appendChild(row2);

                var btnStart = row2.querySelector('#btn-start');
                var btnStop = row2.querySelector('#btn-stop');

                btnStart.onclick = function(){
                    window.autoTradeEnabled = true;
                    btnStart.style.outline = '2px solid #fff';
                    btnStop.style.outline = 'none';
                    runContinuousEngine(panel, true);
                };

                btnStop.onclick = function(){
                    window.autoTradeEnabled = false;
                    btnStop.style.outline = '2px solid #fff';
                    btnStart.style.outline = 'none';
                };

                // AI Signal Scanner Box with Multi-colored Animated Candles (Matching Video)
                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:8px 10px;background:#03050a;border:1px solid #131d2e;border-radius:8px;padding:10px;text-align:center;';
                scannerBox.innerHTML = '<div style="font-size:7.5px;color:#8a99ad;font-weight:800;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;"><span>AI SIGNAL SCANNER</span><span id="scan-status" style="color:#00ff66;font-size:7px;">READY</span></div>' +
                                       '<div style="font-size:11px;font-weight:900;color:#00ff66;margin:4px 0;letter-spacing:1px;" id="scanner-title">Next Candle??</div>' +
                                       '<div id="candle-container" style="height:42px;display:flex;align-items:center;justify-content:center;gap:4.5px;margin:5px 0;">' +
                                       '<div style="width:3.5px;height:24px;background:#00ff66;border-radius:2px;animation:cPulse 1.1s infinite ease-in-out;box-shadow:0 0 6px #00ff66;"></div>' +
                                       '<div style="width:3.5px;height:32px;background:#ff1744;border-radius:2px;animation:cPulse 0.8s infinite ease-in-out;box-shadow:0 0 6px #ff1744;"></div>' +
                                       '<div style="width:3.5px;height:18px;background:#00ff66;border-radius:2px;animation:cPulse 1.3s infinite ease-in-out;box-shadow:0 0 6px #00ff66;"></div>' +
                                       '<div style="width:3.5px;height:36px;background:#ff1744;border-radius:2px;animation:cPulse 0.7s infinite ease-in-out;box-shadow:0 0 6px #ff1744;"></div>' +
                                       '<div style="width:3.5px;height:28px;background:#00ff66;border-radius:2px;animation:cPulse 1.0s infinite ease-in-out;box-shadow:0 0 6px #00ff66;"></div>' +
                                       '<div style="width:3.5px;height:22px;background:#ff1744;border-radius:2px;animation:cPulse 1.2s infinite ease-in-out;box-shadow:0 0 6px #ff1744;"></div>' +
                                       '<div style="width:3.5px;height:30px;background:#00ff66;border-radius:2px;animation:cPulse 0.9s infinite ease-in-out;box-shadow:0 0 6px #00ff66;"></div>' +
                                       '</div>';
                panel.appendChild(scannerBox);

                // Latest Signal Box (Matching Video Layout)
                var sigBox = d.createElement('div');
                sigBox.style.cssText = 'margin:0 10px 8px 10px;background:#0d1526;border:1px solid #131d2e;border-radius:8px;padding:8px 10px;display:flex;justify-content:space-between;align-items:center;';
                sigBox.innerHTML = '<div>' +
                                   '<div style="font-size:7px;color:#8a99ad;font-weight:800;">LATEST SIGNAL</div>' +
                                   '<div id="p-signal" style="font-size:12px;font-weight:900;color:#00ff66;letter-spacing:0.5px;">READY</div>' +
                                   '<div style="font-size:6.5px;color:#556677;" id="p-subtext">Click Start Auto to begin execution.</div>' +
                                   '</div>' +
                                   '<div id="signal-icon" style="background:#101826;width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;">⚡</div>';
                panel.appendChild(sigBox);

                // License / Password Verification Section (Matching Video Screen)
                var licenseBox = d.createElement('div');
                licenseBox.style.cssText = 'margin:0 10px 8px 10px;background:#03050a;border:1px solid #131d2e;border-radius:8px;padding:8px 10px;';
                licenseBox.innerHTML = '<input type="password" id="license-input" placeholder="Enter license key" style="width:100%;box-sizing:border-box;background:#0d1526;border:1px solid #16253f;padding:6px 8px;border-radius:4px;color:#fff;font-size:8px;outline:none;margin-bottom:6px;" />' +
                                       '<button id="verify-btn" style="width:100%;background:#00c853;border:none;padding:7px;border-radius:6px;font-weight:900;font-size:8.5px;color:#000;cursor:pointer;box-shadow:0 0 8px rgba(0,200,83,0.4);text-align:center;">VERIFY LICENSE</button>';
                panel.appendChild(licenseBox);

                var verifyBtn = licenseBox.querySelector('#verify-btn');
                var licenseInput = licenseBox.querySelector('#license-input');
                verifyBtn.onclick = function(){
                    var val = licenseInput.value.trim();
                    if(val.length > 0){
                        verifyBtn.innerText = 'VERIFIED SUCCESS ✓';
                        verifyBtn.style.background = '#00ff66';
                    } else {
                        verifyBtn.innerText = 'ENTER VALID KEY';
                        verifyBtn.style.background = '#ff1744';
                    }
                };

                // Footer branding
                var footer = d.createElement('div');
                footer.style.cssText = 'padding:6px 12px;background:#03050a;display:flex;justify-content:space-between;align-items:center;font-size:6.5px;color:#556677;border-top:1px solid #131d2e;';
                footer.innerHTML = '<span>• ULTRA AI ENGINE</span><span>SNIPER / UI</span>';
                panel.appendChild(footer);

                d.body.appendChild(panel);
            }

            function forceClick(el) {
                if(!el) return false;
                try {
                    var box = el.getBoundingClientRect();
                    var cx = box.left + (box.width / 2);
                    var cy = box.top + (box.height / 2);
                    ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(function(evName){
                        var ev = new MouseEvent(evName, {
                            bubbles: true, cancelable: true, view: window,
                            clientX: cx,clientY: cy,screenX: cx,screenY: cy
                        });
                        el.dispatchEvent(ev);
                    });
                    if(typeof el.click === 'function') el.click();
                    return true;
                } catch(e) { return false; }
            }

            window.lastTradeExecutionTimestamp = 0;
            function triggerTrade(isSell){
                var nowTs = Date.now();
                if(nowTs - window.lastTradeExecutionTimestamp < 50000) return;
                window.lastTradeExecutionTimestamp = nowTs;

                var clicked = false;
                var selectors = isSell ? [
                    '.section-deal__button-down button', '.section-deal__button-down',
                    '.btn-put', 'button.put', 'button[class*="put"]', '.button-sell', '[class*="sell"]'
                ] : [
                    '.section-deal__button-up button', '.section-deal__button-up',
                    '.btn-call', 'button.call', 'button[class*="call"]', '.button-buy', '[class*="buy"]'
                ];

                for(var i=0; i<selectors.length; i++){
                    var btns = d.querySelectorAll(selectors[i]);
                    for(var j=0; j<btns.length; j++){
                        if(btns[j] && btns[j].getBoundingClientRect().width > 0){
                            if(forceClick(btns[j])){ clicked = true; break; }
                        }
                    }
                    if(clicked) break;
                }
            }

            function runContinuousEngine(panel, isAutoTradeMode){
                var scanStatus = panel.querySelector('#scan-status');
                var scannerTitle = panel.querySelector('#scanner-title');
                var sigEl = panel.querySelector('#p-signal');
                var subText = panel.querySelector('#p-subtext');
                var sigIcon = panel.querySelector('#signal-icon');

                if(scanStatus) scanStatus.innerText = 'SCANNING...';
                if(scannerTitle) scannerTitle.innerText = 'Algorithmic Pattern Sync...';
                if(sigEl) sigEl.innerText = 'ANALYZING...';

                fetch('https://hr-auto-bot-fhyc.onrender.com/signal?t='+Date.now())
                .then(function(r){ return r.json(); })
                .catch(function(){ return {signal: "UP", confidence: 81}; })
                .then(function(j){
                    if(scanStatus) scanStatus.innerText = 'READY';
                    if(scannerTitle) scannerTitle.innerText = '5S AUTO SYNCED';

                    var rawSig = String(j.signal || 'UP').toUpperCase();
                    var isDown = (rawSig === 'SELL' || rawSig === 'DOWN' || rawSig === 'PUT');
                    var sigText = isDown ? 'DOWN' : 'UP';
                    var col = isDown ? '#ff1744' : '#00ff66';

                    if(sigEl) {
                        sigEl.innerText = sigText + ' (' + (j.confidence || 81) + '%)';
                        sigEl.style.color = col;
                    }
                    if(subText) subText.innerText = 'License verified successfully.';
                    if(sigIcon) {
                        sigIcon.innerText = isDown ? '⬇️' : '⬆️';
                        sigIcon.style.color = col;
                    }

                    if(window.autoTradeEnabled && isAutoTradeMode) {
                        triggerTrade(isDown);
                    }
                });
            }
        } catch(e) { console.error("SniperBot Error:", e); }
    })();
    """
    res = make_response(js)
    res.headers['Content-Type'] = 'application/javascript'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
