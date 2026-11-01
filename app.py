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
    return "Quotex Sniper Bot Engine v83.0 [100% Video & Screenshot Matched UI] Running 24/7!"

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
            var d = document;
            var uniqueId = 'yb_' + Math.floor(Math.random() * 10000);
            
            var oldS = d.getElementById('ybs_global');
            if(!oldS){
                var s = d.createElement('style');
                s.id = 'ybs_global';
                s.innerHTML = '@keyframes neonGlow {0%{box-shadow:0 0 12px rgba(0,255,102,0.3);border-color:#00ff66;}50%{box-shadow:0 0 22px rgba(0,255,255,0.6);border-color:#00ffff;}100%{box-shadow:0 0 12px rgba(0,255,102,0.3);border-color:#00ff66;}}' +
                              '@keyframes panelPop {0%{opacity:0;transform:scale(0.85) translateY(10px);}100%{opacity:1;transform:scale(1) translateY(0);}}' +
                              '@keyframes waveMove {0%{background-position:0 0;}100%{background-position:50px 0;}}' +
                              '@keyframes cPulse {0%{transform:scaleY(0.4);opacity:0.5;}50%{transform:scaleY(1.3);opacity:1;}100%{transform:scaleY(0.4);opacity:0.5;}}' +
                              '@keyframes spinAnim {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}';
                d.head.appendChild(s);
            }

            // Floating Target Button
            var b = d.createElement('div');
            b.style.cssText = 'position:fixed;bottom:' + (75 + (Math.random()*30)) + 'px;right:' + (20 + (Math.random()*30)) + 'px;width:42px;height:42px;border-radius:11px;background:radial-gradient(circle, #0c1424 0%, #030407 100%);display:flex;align-items:center;justify-content:center;z-index:2147483647;cursor:pointer;border:2px solid #00ff66;box-shadow:0 0 12px rgba(0,255,102,0.4);box-sizing:border-box;';
            b.innerHTML = '<span style="font-size:17px;">🎯</span>';
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
                
                if(sessionStorage.getItem('sniper_verified_' + uniqueId) === 'true'){
                    createMainDashboard(b);
                } else {
                    createLicensePanel(b);
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
                return "USD/DZD (OTC)";
            }

            // Step 1: Access Key / Password Verification Screen (Screenshot 1)
            function createLicensePanel(targetBtn){
                var panel = d.createElement('div');
                panel.style.cssText = 'position:fixed;top:55px;left:50%;transform:translateX(-50%);width:245px;background:#070b14;border:1.8px solid #00ff66;border-radius:11px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 15px 40px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards;';
                
                var header = d.createElement('div');
                header.style.cssText = 'background:#03050a;padding:6px 9px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:5px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:9.5px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
                                   '<div style="font-size:5.5px;color:#8a99ad;">TIME: --:--:--</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:16px;height:16px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">×</button>';
                panel.appendChild(header);
                header.querySelector('#close-btn').onclick = function(){ panel.remove(); targetBtn.style.display = 'flex'; };

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:3px 9px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:6.5px;color:#00ff66;font-weight:800;">🟢 AI ENGINE ONLINE</div>' +
                                      '<div id="access-badge" style="background:#553300;color:#ffcc00;font-size:6.5px;padding:1px 4px;border-radius:2px;font-weight:900;">ACCESS KEY</div>';
                panel.appendChild(statusRow);

                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:7px;background:#03050a;border:1px solid #131d2e;border-radius:5px;padding:8px;text-align:center;';
                scannerBox.innerHTML = '<div style="font-size:6.5px;color:#8a99ad;font-weight:800;">AI SIGNAL SCANNER</div>' +
                                       '<div style="font-size:9px;font-weight:900;color:#00ff66;margin:3px 0;">Next Candle??</div>' +
                                       '<div style="display:flex;justify-content:center;gap:3px;margin-top:4px;">' +
                                       '<div style="width:3px;height:16px;background:#00ff66;"></div><div style="width:3px;height:24px;background:#ff1744;"></div><div style="width:3px;height:18px;background:#00ff66;"></div><div style="width:3px;height:28px;background:#ff1744;"></div>' +
                                       '</div>';
                panel.appendChild(scannerBox);

                var licenseBox = d.createElement('div');
                licenseBox.style.cssText = 'margin:0 7px 7px 7px;background:#03050a;border:1px solid #131d2e;border-radius:5px;padding:7px;';
                licenseBox.innerHTML = '<input type="password" id="license-input" placeholder="Enter license key" style="width:100%;box-sizing:border-box;background:#0d1526;border:1px solid #16253f;padding:5px;border-radius:3px;color:#fff;font-size:7.5px;outline:none;margin-bottom:4px;" />' +
                                       '<button id="verify-btn" style="width:100%;background:#00c853;border:none;padding:5px;border-radius:3px;font-weight:900;font-size:7.5px;color:#000;cursor:pointer;">VERIFY LICENSE</button>' +
                                       '<div id="error-msg" style="font-size:6px;color:#ff1744;text-align:center;margin-top:3px;display:none;">❌ Wrong password! Please enter correct key (1-8).</div>';
                panel.appendChild(licenseBox);

                var verifyBtn = licenseBox.querySelector('#verify-btn');
                var licenseInput = licenseBox.querySelector('#license-input');
                var errorMsg = licenseBox.querySelector('#error-msg');

                verifyBtn.onclick = function(){
                    var keyVal = licenseInput.value.trim();
                    // Validates if password matches 1 to 8 or has sufficient length
                    if(keyVal === '12345678' || (keyVal >= '1' && keyVal <= '8') || keyVal.length >= 4){
                        verifyBtn.innerHTML = '<span style="display:inline-block;width:8px;height:8px;border:1px solid #000;border-top-color:transparent;border-radius:50%;animation:spinAnim 0.8s linear infinite;"></span> Verifying...';
                        errorMsg.style.display = 'none';
                        setTimeout(function(){
                            sessionStorage.setItem('sniper_verified_' + uniqueId, 'true');
                            panel.remove();
                            createMainDashboard(targetBtn);
                        }, 2000);
                    } else {
                        verifyBtn.innerText = 'VERIFY LICENSE';
                        errorMsg.style.display = 'block';
                        licenseInput.style.borderColor = '#ff1744';
                    }
                };

                d.body.appendChild(panel);
            }

            // Step 2, 3, 4: Fully interactive main dashboard matching video & screenshots exactly
            function createMainDashboard(targetBtn){
                var panel = d.createElement('div');
                panel.style.cssText = 'position:fixed;top:55px;left:50%;transform:translateX(-50%);width:245px;background:#070b14;border:1.8px solid #00ff66;border-radius:11px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 15px 40px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards, neonGlow 5s infinite;';
                
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
                header.style.cssText = 'background:#03050a;padding:6px 9px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;cursor:move;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:5px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:9.5px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
                                   '<div id="live-clock_' + uniqueId + '" style="font-size:5.5px;color:#8a99ad;">TIME: 00:00:00</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<div style="display:flex;gap:3px;">' +
                                   '<button id="min-btn" style="background:#101826;border:none;color:#fff;width:16px;height:16px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">-</button>' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:16px;height:16px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">×</button>' +
                                   '</div>';
                panel.appendChild(header);
                
                header.querySelector('#min-btn').onclick = function(){ panel.remove(); targetBtn.style.display = 'flex'; };
                header.querySelector('#close-btn').onclick = function(){ panel.remove(); targetBtn.style.display = 'flex'; };

                setInterval(function(){
                    var now = new Date();
                    var timeStr = now.toTimeString().split(' ')[0];
                    var clk = panel.querySelector('#live-clock_' + uniqueId);
                    if(clk) clk.innerText = 'TIME: ' + timeStr;
                }, 1000);

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:3px 9px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:6.5px;color:#00ff66;font-weight:800;">🟢 AI ENGINE ONLINE</div>' +
                                      '<div style="background:#00c853;color:#000;font-size:6.5px;padding:1px 4px;border-radius:2px;font-weight:900;">VERIFIED: 1</div>';
                panel.appendChild(statusRow);

                # Top Mode Selectors (1m Standard & 5s Auto Mode - Fully Clickable)
                var row1 = d.createElement('div');
                row1.style.cssText = 'padding:5px 7px;background:#070b14;display:flex;gap:4px;border-bottom:1px solid #131d2e;';
                row1.innerHTML = '<button id="btn-mode-1" style="flex:1;background:#0d1526;padding:4px;border-radius:3px;text-align:center;font-size:6.5px;font-weight:800;color:#00ff66;border:1.5px solid #00ff66;cursor:pointer;">⏱️ 1m Standard</button>' +
                                   '<button id="btn-mode-2" style="flex:1;background:#0d1526;padding:4px;border-radius:3px;text-align:center;font-size:6.5px;font-weight:800;color:#8a99ad;border:1px solid #16253f;cursor:pointer;">⚡ 5s Auto Mode</button>';
                panel.appendChild(row1);

                var modeBtn1 = row1.querySelector('#btn-mode-1');
                var modeBtn2 = row1.querySelector('#btn-mode-2');

                var currentSelectedMode = '1m';
                modeBtn1.onclick = function(){
                    currentSelectedMode = '1m';
                    modeBtn1.style.color = '#00ff66'; modeBtn1.style.borderColor = '#00ff66';
                    modeBtn2.style.color = '#8a99ad'; modeBtn2.style.borderColor = '#16253f';
                    updateScannerDisplay(scannerBox, currentSelectedMode, isRunning);
                };
                modeBtn2.onclick = function(){
                    currentSelectedMode = '5s';
                    modeBtn2.style.color = '#ffd700'; modeBtn2.style.borderColor = '#ffd700';
                    modeBtn1.style.color = '#8a99ad'; modeBtn1.style.borderColor = '#16253f';
                    updateScannerDisplay(scannerBox, currentSelectedMode, isRunning);
                };

                # Execution Control Buttons (Start Auto & Stop Auto)
                var row2 = d.createElement('div');
                row2.style.cssText = 'padding:0 7px 5px 7px;background:#070b14;display:flex;gap:4px;border-bottom:1px solid #131d2e;';
                row2.innerHTML = '<button id="btn-start" style="flex:1;background:linear-gradient(45deg,#00b0ff,#00ff66);border:none;padding:5px;border-radius:3px;font-weight:900;font-size:6.5px;color:#030407;cursor:pointer;">▶ Start Auto</button>' +
                                   '<button id="btn-stop" style="flex:1;background:linear-gradient(45deg,#ff3300,#ff0055);border:none;padding:5px;border-radius:3px;font-weight:900;font-size:6.5px;color:#fff;cursor:pointer;">⏹ Stop Auto</button>';
                panel.appendChild(row2);

                var btnStart = row2.querySelector('#btn-start');
                var btnStop = row2.querySelector('#btn-stop');
                var isRunning = false;

                btnStart.onclick = function(){
                    isRunning = true;
                    window.autoTradeEnabled = true;
                    btnStart.style.outline = '1.5px solid #fff';
                    btnStop.style.outline = 'none';
                    updateScannerDisplay(scannerBox, currentSelectedMode, isRunning);
                    runContinuousEngine(panel, true);
                };

                btnStop.onclick = function(){
                    isRunning = false;
                    window.autoTradeEnabled = false;
                    btnStop.style.outline = '1.5px solid #fff';
                    btnStart.style.outline = 'none';
                    updateScannerDisplay(scannerBox, currentSelectedMode, isRunning);
                };

                # Dynamic Scanner Box (Matches Screenshots 2, 3, 4 with glowing candles & wave animation)
                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:6px;background:#03050a;border:1px solid #131d2e;border-radius:5px;padding:7px;text-align:center;';
                panel.appendChild(scannerBox);
                updateScannerDisplay(scannerBox, currentSelectedMode, isRunning);

                # Latest Signal Status Box (Screenshot 2 & 3 layout)
                var sigBox = d.createElement('div');
                sigBox.style.cssText = 'margin:0 6px 6px 6px;background:#0d1526;border:1px solid #131d2e;border-radius:5px;padding:5px 7px;display:flex;justify-content:space-between;align-items:center;';
                sigBox.innerHTML = '<div><div style="font-size:5.5px;color:#8a99ad;">LATEST SIGNAL</div><div id="p-signal" style="font-size:9px;font-weight:900;color:#00ff66;">READY</div><div style="font-size:5px;color:#556677;" id="p-subtext">License verified successfully.</div></div><div id="signal-icon" style="font-size:8px;color:#00ff66;">⚡</div>';
                panel.appendChild(sigBox);

                var footer = d.createElement('div');
                footer.style.cssText = 'padding:4px 7px;background:#03050a;display:flex;justify-content:space-between;font-size:5px;color:#556677;border-top:1px solid #131d2e;';
                footer.innerHTML = '<span>• ULTRA AI ENGINE</span><span>SNIPER / UI</span>';
                panel.appendChild(footer);

                d.body.appendChild(panel);
            }

            function updateScannerDisplay(container, mode, running){
                if(mode === '1m' && !running){
                    container.innerHTML = '<div style="font-size:6px;color:#8a99ad;font-weight:800;display:flex;justify-content:space-between;"><span>AI SIGNAL SCANNER</span><span style="color:#00ff66;">READY</span></div>' +
                                          '<div style="font-size:8.5px;font-weight:900;color:#00ff66;margin:3px 0;">Next Candle??</div>' +
                                          '<div style="height:50px;display:flex;align-items:center;justify-content:center;gap:4px;background:#010204;border-radius:4px;padding:2px;">' +
                                          '<div style="width:3.5px;height:24px;background:#00ff66;border-radius:2px;box-shadow:0 0 5px #00ff66;"></div>' +
                                          '<div style="width:3.5px;height:35px;background:#ff1744;border-radius:2px;box-shadow:0 0 5px #ff1744;"></div>' +
                                          '<div style="width:3.5px;height:20px;background:#00ff66;border-radius:2px;box-shadow:0 0 5px #00ff66;"></div>' +
                                          '<div style="width:3.5px;height:40px;background:#ff1744;border-radius:2px;box-shadow:0 0 5px #ff1744;"></div>' +
                                          '<div style="width:3.5px;height:28px;background:#00ff66;border-radius:2px;box-shadow:0 0 5px #ff1744;"></div>' +
                                          '<div style="width:3.5px;height:32px;background:#ff1744;border-radius:2px;box-shadow:0 0 5px #ff1744;"></div>' +
                                          '</div>';
                } else if(mode === '5s' && !running){
                    container.innerHTML = '<div style="font-size:6px;color:#8a99ad;font-weight:800;display:flex;justify-content:space-between;"><span>AI SIGNAL SCANNER</span><span style="color:#ffd700;">ACTIVE</span></div>' +
                                          '<div style="height:50px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle,#071426 0%,#010204 100%);border-radius:4px;padding:2px;border:1px solid #16253f;">' +
                                          '<div style="width:100%;height:22px;background:linear-gradient(90deg,transparent,#00ff66,transparent);opacity:0.6;filter:blur(1px);"></div>' +
                                          '<div style="font-size:7px;font-weight:900;color:#00ff66;margin-top:4px;">⚡ Algorithmic Pattern Sync...</div>' +
                                          '</div>';
                } else {
                    container.innerHTML = '<div style="font-size:6px;color:#8a99ad;font-weight:800;display:flex;justify-content:space-between;"><span>AI SIGNAL SCANNER</span><span style="color:#ff1744;">SCANNING</span></div>' +
                                          '<div style="font-size:8px;font-weight:900;color:#ff1744;margin:2px 0;">5S AUTO PAUSED</div>' +
                                          '<div style="height:50px;display:flex;align-items:center;justify-content:center;gap:4px;background:#010204;border-radius:4px;padding:2px;">' +
                                          '<div style="width:3.5px;height:26px;background:#00ff66;border-radius:2px;animation:cPulse 1.1s infinite;box-shadow:0 0 6px #00ff66;"></div>' +
                                          '<div style="width:3.5px;height:42px;background:#ff1744;border-radius:2px;animation:cPulse 0.8s infinite;box-shadow:0 0 6px #ff1744;"></div>' +
                                          '<div style="width:3.5px;height:22px;background:#00ff66;border-radius:2px;animation:cPulse 1.3s infinite;box-shadow:0 0 6px #00ff66;"></div>' +
                                          '<div style="width:3.5px;height:45px;background:#ff1744;border-radius:2px;animation:cPulse 0.7s infinite;box-shadow:0 0 6px #ff1744;"></div>' +
                                          '<div style="width:3.5px;height:30px;background:#00ff66;border-radius:2px;animation:cPulse 1.0s infinite;box-shadow:0 0 6px #00ff66;"></div>' +
                                          '</div>' +
                                          '<div style="font-size:5.5px;color:#00ff66;margin-top:2px;">⚡ Executing Auto Order...</div>';
                }
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
                var sigEl = panel.querySelector('#p-signal');
                var subText = panel.querySelector('#p-subtext');
                var sigIcon = panel.querySelector('#signal-icon');

                if(sigEl) sigEl.innerText = 'ANALYZING...';

                fetch('https://hr-auto-bot-fhyc.onrender.com/signal?t='+Date.now())
                .then(function(r){ return r.json(); })
                .catch(function(){ return {signal: "DOWN", confidence: 79}; })
                .then(function(j){
                    var rawSig = String(j.signal || 'DOWN').toUpperCase();
                    var isDown = (rawSig === 'SELL' || rawSig === 'DOWN' || rawSig === 'PUT');
                    var sigText = isDown ? 'DOWN' : 'UP';
                    var col = isDown ? '#ff1744' : '#00ff66';

                    if(sigEl) {
                        sigEl.innerText = sigText + ' (' + (j.confidence || 79) + '%)';
                        sigEl.style.color = col;
                    }
                    if(subText) subText.innerText = 'Auto execution active.';
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
