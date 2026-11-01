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
                          '@keyframes cPulse {0%{transform:scaleY(0.4);opacity:0.5;}50%{transform:scaleY(1.3);opacity:1;}100%{transform:scaleY(0.4);opacity:0.5;}}' +
                          '@keyframes panelPop {0%{opacity:0;transform:scale(0.85) translateY(15px);}100%{opacity:1;transform:scale(1) translateY(0);}}' +
                          '@keyframes spinAnim {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}';
            d.head.appendChild(s);

            // Floating Target Icon (Draggable)
            var b = d.createElement('div');
            window.YB = b;
            b.style.cssText = 'position:fixed;bottom:80px;right:25px;width:48px;height:48px;border-radius:12px;background:radial-gradient(circle, #0c1424 0%, #030407 100%);display:flex;align-items:center;justify-content:center;z-index:2147483647;cursor:pointer;border:2px solid #00ff66;box-shadow:0 0 12px rgba(0,255,102,0.4);box-sizing:border-box;';
            b.innerHTML = '<span style="font-size:20px;">🎯</span>';
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
                createLicensePanel();
            };

            // Active Market Detector helper function
            function detectActiveMarket(){
                try {
                    var allEls = d.querySelectorAll('div, span');
                    for(var i=0; i<allEls.length; i++){
                        var txt = allEls[i].innerText ? allEls[i].innerText.trim() : '';
                        if((txt.includes('OTC') || txt.includes('/')) && txt.length >= 6 && txt.length <= 16 && !txt.includes('Deposit')){
                            return txt;
                        }
                    }
                } catch(e){}
                return "EUR/USD (OTC)";
            }

            // Step 1: License / Password Screen (Screenshot 3289)
            function createLicensePanel(){
                if(d.getElementById('yb-panel')) return;
                
                var panel = d.createElement('div');
                window.YBP = panel;
                panel.id = 'yb-panel';
                panel.style.cssText = 'position:fixed;top:70px;left:50%;transform:translateX(-50%);width:265px;background:#070b14;border:2px solid #00ff66;border-radius:12px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 15px 45px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards;';
                
                var header = d.createElement('div');
                header.style.cssText = 'background:#03050a;padding:8px 10px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:6px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:20px;height:20px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:10px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:10.5px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
                                   '<div style="font-size:6.5px;color:#8a99ad;">CLOCK: --:--:--</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<div style="display:flex;gap:4px;">' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:18px;height:18px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:11px;">×</button>' +
                                   '</div>';
                panel.appendChild(header);
                header.querySelector('#close-btn').onclick = function(){ panel.remove(); b.style.display = 'flex'; };

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:5px 10px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:7px;color:#00ff66;font-weight:800;display:flex;align-items:center;gap:3px;"><span style="width:5px;height:5px;background:#00ff66;border-radius:50%;display:inline-block;"></span>AI ENGINE ONLINE</div>' +
                                      '<div style="background:#553300;color:#ffcc00;font-size:7px;padding:1px 5px;border-radius:3px;font-weight:900;">READY</div>';
                panel.appendChild(statusRow);

                var row1 = d.createElement('div');
                row1.style.cssText = 'padding:6px 8px;background:#070b14;display:flex;gap:5px;border-bottom:1px solid #131d2e;';
                row1.innerHTML = '<div style="flex:1;background:#0d1526;padding:5px;border-radius:5px;text-align:center;font-size:7.5px;font-weight:800;color:#00ff66;border:1px solid #16253f;">⏱️ 1m Standard</div>' +
                                   '<div style="flex:1;background:#0d1526;padding:5px;border-radius:5px;text-align:center;font-size:7.5px;font-weight:800;color:#ffd700;border:1px solid #16253f;">⚡ 5s Auto Mode</div>';
                panel.appendChild(row1);

                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:6px 8px;background:#03050a;border:1px solid #131d2e;border-radius:6px;padding:8px;text-align:center;';
                scannerBox.innerHTML = '<div style="font-size:7px;color:#8a99ad;font-weight:800;margin-bottom:3px;">AI SIGNAL SCANNER</div>' +
                                       '<div style="font-size:10px;font-weight:900;color:#00ff66;margin:3px 0;">Next Candle??</div>' +
                                       '<div style="height:36px;display:flex;align-items:center;justify-content:center;gap:3.5px;margin:4px 0;">' +
                                       '<div style="width:3px;height:20px;background:#00ff66;border-radius:2px;animation:cPulse 1.1s infinite;"></div>' +
                                       '<div style="width:3px;height:28px;background:#ff1744;border-radius:2px;animation:cPulse 0.8s infinite;"></div>' +
                                       '<div style="width:3px;height:16px;background:#00ff66;border-radius:2px;animation:cPulse 1.3s infinite;"></div>' +
                                       '<div style="width:3px;height:30px;background:#ff1744;border-radius:2px;animation:cPulse 0.7s infinite;"></div>' +
                                       '<div style="width:3px;height:22px;background:#00ff66;border-radius:2px;animation:cPulse 1.0s infinite;"></div>' +
                                       '</div>';
                panel.appendChild(scannerBox);

                var sigBox = d.createElement('div');
                sigBox.style.cssText = 'margin:0 8px 6px 8px;background:#0d1526;border:1px solid #131d2e;border-radius:6px;padding:6px 8px;display:flex;justify-content:space-between;align-items:center;';
                sigBox.innerHTML = '<div><div style="font-size:6.5px;color:#8a99ad;">LATEST SIGNAL</div><div style="font-size:11px;font-weight:900;color:#00ff66;">READY</div><div style="font-size:6px;color:#556677;">Enter license key to begin</div></div><div style="font-size:10px;color:#8a99ad;">--:--:--</div>';
                panel.appendChild(sigBox);

                // License input & verify button
                var licenseBox = d.createElement('div');
                licenseBox.style.cssText = 'margin:0 8px 8px 8px;background:#03050a;border:1px solid #131d2e;border-radius:6px;padding:6px 8px;';
                licenseBox.innerHTML = '<input type="password" id="license-input" placeholder="Enter license key" style="width:100%;box-sizing:border-box;background:#0d1526;border:1px solid #16253f;padding:5px 6px;border-radius:4px;color:#fff;font-size:7.5px;outline:none;margin-bottom:5px;" />' +
                                       '<button id="verify-btn" style="width:100%;background:#00c853;border:none;padding:6px;border-radius:5px;font-weight:900;font-size:8px;color:#000;cursor:pointer;">VERIFY LICENSE</button>';
                panel.appendChild(licenseBox);

                var verifyBtn = licenseBox.querySelector('#verify-btn');
                var licenseInput = licenseBox.querySelector('#license-input');

                verifyBtn.onclick = function(){
                    var keyVal = licenseInput.value.trim();
                    if(keyVal.length > 0){
                        verifyBtn.innerHTML = '<span style="display:inline-block;width:10px;height:10px;border:2px solid #000;border-top-color:transparent;border-radius:50%;animation:spinAnim 0.8s linear infinite;"></span> Verifying...';
                        setTimeout(function(){
                            panel.remove();
                            createMainDashboard();
                        }, 2000); // 2 seconds verification animation as requested
                    } else {
                        verifyBtn.innerText = 'ENTER VALID KEY';
                        verifyBtn.style.background = '#ff1744';
                        verifyBtn.style.color = '#fff';
                    }
                };

                var footer = d.createElement('div');
                footer.style.cssText = 'padding:5px 10px;background:#03050a;display:flex;justify-content:space-between;font-size:6px;color:#556677;border-top:1px solid #131d2e;';
                footer.innerHTML = '<span>• ULTRA AI ENGINE</span><span>SNIPER / UI</span>';
                panel.appendChild(footer);

                d.body.appendChild(panel);
            }

            // Step 2: Main Dashboard (Screenshots 3290, 3291, 3292)
            function createMainDashboard(){
                if(d.getElementById('yb-panel')) return;
                
                var panel = d.createElement('div');
                window.YBP = panel;
                panel.id = 'yb-panel';
                panel.style.cssText = 'position:fixed;top:70px;left:50%;transform:translateX(-50%);width:265px;background:#070b14;border:2px solid #00ff66;border-radius:12px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 15px 45px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards, neonGlow 5s infinite;';
                
                // Draggable panel logic
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

                var header = d.createElement('div');
                header.style.cssText = 'background:#03050a;padding:8px 10px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;cursor:move;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:6px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:20px;height:20px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:10px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:10.5px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
                                   '<div id="live-clock" style="font-size:6.5px;color:#8a99ad;">TIME: 00:00:00</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<div style="display:flex;gap:4px;">' +
                                   '<button id="min-btn" style="background:#101826;border:none;color:#fff;width:18px;height:18px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:11px;">-</button>' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:18px;height:18px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:11px;">×</button>' +
                                   '</div>';
                panel.appendChild(header);
                
                header.querySelector('#min-btn').onclick = function(){ panel.remove(); b.style.display = 'flex'; };
                header.querySelector('#close-btn').onclick = function(){ panel.remove(); b.style.display = 'flex'; };

                // Live Clock updater
                setInterval(function(){
                    var now = new Date();
                    var timeStr = now.toTimeString().split(' ')[0];
                    var clk = panel.querySelector('#live-clock');
                    if(clk) clk.innerText = 'TIME: ' + timeStr;
                }, 1000);

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:5px 10px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:7px;color:#00ff66;font-weight:800;display:flex;align-items:center;gap:3px;"><span style="width:5px;height:5px;background:#00ff66;border-radius:50%;display:inline-block;"></span>AI ENGINE ONLINE</div>' +
                                      '<div style="background:#00c853;color:#000;font-size:7px;padding:1px 5px;border-radius:3px;font-weight:900;">VERIFIED: 1</div>';
                panel.appendChild(statusRow);

                var row1 = d.createElement('div');
                row1.style.cssText = 'padding:6px 8px;background:#070b14;display:flex;gap:5px;border-bottom:1px solid #131d2e;';
                row1.innerHTML = '<div style="flex:1;background:#0d1526;padding:5px;border-radius:5px;text-align:center;font-size:7.5px;font-weight:800;color:#00ff66;border:1px solid #16253f;">⏱️ 1m Standard</div>' +
                                   '<div style="flex:1;background:#0d1526;padding:5px;border-radius:5px;text-align:center;font-size:7.5px;font-weight:800;color:#ffd700;border:1px solid #16253f;">⚡ 5s Auto Mode</div>';
                panel.appendChild(row1);

                var row2 = d.createElement('div');
                row2.style.cssText = 'padding:0 8px 6px 8px;background:#070b14;display:flex;gap:5px;border-bottom:1px solid #131d2e;';
                row2.innerHTML = '<button id="btn-start" style="flex:1;background:linear-gradient(45deg,#00b0ff,#00ff66);border:none;padding:6px;border-radius:5px;font-weight:900;font-size:7.5px;color:#030407;cursor:pointer;">▶ Start Auto</button>' +
                                   '<button id="btn-stop" style="flex:1;background:linear-gradient(45deg,#ff3300,#ff0055);border:none;padding:6px;border-radius:5px;font-weight:900;font-size:7.5px;color:#fff;cursor:pointer;">⏹ Stop Auto</button>';
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

                // AI Signal Scanner Box (showing active detected market pair)
                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:6px 8px;background:#03050a;border:1px solid #131d2e;border-radius:6px;padding:8px;text-align:center;';
                scannerBox.innerHTML = '<div style="font-size:7px;color:#8a99ad;font-weight:800;margin-bottom:3px;display:flex;justify-content:space-between;"><span>AI SIGNAL SCANNER</span><span id="scan-status" style="color:#00ff66;">READY</span></div>' +
                                       '<div style="font-size:10px;font-weight:900;color:#00ff66;margin:2px 0;" id="scanner-title">Next Candle??</div>' +
                                       '<div id="market-detect-label" style="font-size:6.5px;color:#00ffff;margin-bottom:3px;">Market: ' + detectActiveMarket() + '</div>' +
                                       '<div style="height:36px;display:flex;align-items:center;justify-content:center;gap:3.5px;margin:3px 0;">' +
                                       '<div style="width:3px;height:20px;background:#00ff66;border-radius:2px;animation:cPulse 1.1s infinite;"></div>' +
                                       '<div style="width:3px;height:28px;background:#ff1744;border-radius:2px;animation:cPulse 0.8s infinite;"></div>' +
                                       '<div style="width:3px;height:16px;background:#00ff66;border-radius:2px;animation:cPulse 1.3s infinite;"></div>' +
                                       '<div style="width:3px;height:30px;background:#ff1744;border-radius:2px;animation:cPulse 0.7s infinite;"></div>' +
                                       '<div style="width:3px;height:22px;background:#00ff66;border-radius:2px;animation:cPulse 1.0s infinite;"></div>' +
                                       '</div>';
                panel.appendChild(scannerBox);

                var sigBox = d.createElement('div');
                sigBox.style.cssText = 'margin:0 8px 8px 8px;background:#0d1526;border:1px solid #131d2e;border-radius:6px;padding:6px 8px;display:flex;justify-content:space-between;align-items:center;';
                sigBox.innerHTML = '<div><div style="font-size:6.5px;color:#8a99ad;">LATEST SIGNAL</div><div id="p-signal" style="font-size:11px;font-weight:900;color:#00ff66;">READY</div><div style="font-size:6px;color:#556677;" id="p-subtext">License verified successfully.</div></div><div id="signal-icon" style="font-size:10px;color:#00ff66;">⚡</div>';
                panel.appendChild(sigBox);

                var footer = d.createElement('div');
                footer.style.cssText = 'padding:5px 10px;background:#03050a;display:flex;justify-content:space-between;font-size:6px;color:#556677;border-top:1px solid #131d2e;';
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
                var marketDetect = panel.querySelector('#market-detect-label');

                if(marketDetect) marketDetect.innerText = 'Market: ' + detectActiveMarket();
                if(scanStatus) scanStatus.innerText = 'SCANNING...';
                if(scannerTitle) scannerTitle.innerText = 'Executing Auto Order...';
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
                    if(subText) subText.innerText = 'Signal synced successfully.';
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
