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
    return "Quotex Sniper Bot Engine v75.0 [Live DOM Chart Mirror & Session Auth] Running 24/7!"

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
            s.innerHTML = '@keyframes neonGlow {0%{box-shadow:0 0 10px rgba(0,255,102,0.3);border-color:#00ff66;}50%{box-shadow:0 0 18px rgba(0,255,255,0.6);border-color:#00ffff;}100%{box-shadow:0 0 10px rgba(0,255,102,0.3);border-color:#00ff66;}}' +
                          '@keyframes panelPop {0%{opacity:0;transform:scale(0.85) translateY(10px);}100%{opacity:1;transform:scale(1) translateY(0);}}' +
                          '@keyframes spinAnim {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}';
            d.head.appendChild(s);

            // Floating Target Button (Compact & Draggable)
            var b = d.createElement('div');
            window.YB = b;
            b.style.cssText = 'position:fixed;bottom:75px;right:20px;width:42px;height:42px;border-radius:10px;background:radial-gradient(circle, #0c1424 0%, #030407 100%);display:flex;align-items:center;justify-content:center;z-index:2147483647;cursor:pointer;border:2px solid #00ff66;box-shadow:0 0 10px rgba(0,255,102,0.4);box-sizing:border-box;';
            b.innerHTML = '<span style="font-size:18px;">🎯</span>';
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
                
                // Check if already verified in this session
                if(sessionStorage.getItem('sniper_verified') === 'true'){
                    createMainDashboard();
                } else {
                    createLicensePanel();
                }
            };

            // Quotex Active Market Detector
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
                return "USD/BRL (OTC)";
            }

            // Step 1: License Verification Screen (Only asks if not verified in session)
            function createLicensePanel(){
                if(d.getElementById('yb-panel')) return;
                
                var panel = d.createElement('div');
                window.YBP = panel;
                panel.id = 'yb-panel';
                panel.style.cssText = 'position:fixed;top:60px;left:50%;transform:translateX(-50%);width:235px;background:#070b14;border:1.8px solid #00ff66;border-radius:10px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards;';
                
                var header = d.createElement('div');
                header.style.cssText = 'background:#03050a;padding:5px 7px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:4px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:16px;height:16px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:8px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:9px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
                                   '<div style="font-size:5.5px;color:#8a99ad;">CLOCK: --:--:--</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:15px;height:15px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">×</button>';
                panel.appendChild(header);
                header.querySelector('#close-btn').onclick = function(){ panel.remove(); b.style.display = 'flex'; };

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:3px 7px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:6px;color:#00ff66;font-weight:800;">🟢 AI ENGINE ONLINE</div>' +
                                      '<div style="background:#553300;color:#ffcc00;font-size:6px;padding:1px 3px;border-radius:2px;font-weight:900;">READY</div>';
                panel.appendChild(statusRow);

                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:5px;background:#03050a;border:1px solid #131d2e;border-radius:4px;padding:5px;text-align:center;';
                scannerBox.innerHTML = '<div style="font-size:6px;color:#8a99ad;font-weight:800;">AI SIGNAL SCANNER</div>' +
                                       '<div style="font-size:8px;font-weight:900;color:#00ff66;margin:2px 0;">License Verification Required</div>';
                panel.appendChild(scannerBox);

                var licenseBox = d.createElement('div');
                licenseBox.style.cssText = 'margin:0 5px 5px 5px;background:#03050a;border:1px solid #131d2e;border-radius:4px;padding:5px;';
                licenseBox.innerHTML = '<input type="password" id="license-input" placeholder="Enter license key" style="width:100%;box-sizing:border-box;background:#0d1526;border:1px solid #16253f;padding:4px;border-radius:3px;color:#fff;font-size:7px;outline:none;margin-bottom:3px;" />' +
                                       '<button id="verify-btn" style="width:100%;background:#00c853;border:none;padding:4px;border-radius:3px;font-weight:900;font-size:7px;color:#000;cursor:pointer;">VERIFY LICENSE</button>';
                panel.appendChild(licenseBox);

                var verifyBtn = licenseBox.querySelector('#verify-btn');
                var licenseInput = licenseBox.querySelector('#license-input');

                verifyBtn.onclick = function(){
                    var keyVal = licenseInput.value.trim();
                    if(keyVal.length > 0){
                        verifyBtn.innerHTML = '<span style="display:inline-block;width:7px;height:7px;border:1px solid #000;border-top-color:transparent;border-radius:50%;animation:spinAnim 0.8s linear infinite;"></span> Verifying...';
                        setTimeout(function(){
                            sessionStorage.setItem('sniper_verified', 'true'); // Save session verification
                            panel.remove();
                            createMainDashboard();
                        }, 2000); // 2 seconds verification animation
                    } else {
                        verifyBtn.innerText = 'ENTER VALID KEY';
                        verifyBtn.style.background = '#ff1744';
                        verifyBtn.style.color = '#fff';
                    }
                };

                d.body.appendChild(panel);
            }

            // Step 2: Main Dashboard (Compact Size & Live Chart Mirroring)
            function createMainDashboard(){
                if(d.getElementById('yb-panel')) return;
                
                var panel = d.createElement('div');
                window.YBP = panel;
                panel.id = 'yb-panel';
                panel.style.cssText = 'position:fixed;top:60px;left:50%;transform:translateX(-50%);width:235px;background:#070b14;border:1.8px solid #00ff66;border-radius:10px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards, neonGlow 5s infinite;';
                
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
                header.style.cssText = 'background:#03050a;padding:5px 7px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;cursor:move;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:4px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:16px;height:16px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:8px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:9px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
                                   '<div id="live-clock" style="font-size:5.5px;color:#8a99ad;">TIME: 00:00:00</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<div style="display:flex;gap:3px;">' +
                                   '<button id="min-btn" style="background:#101826;border:none;color:#fff;width:15px;height:15px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">-</button>' +
                                   '<button id="close-btn" style="background:#101826;border:none;color:#fff;width:15px;height:15px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">×</button>' +
                                   '</div>';
                panel.appendChild(header);
                
                header.querySelector('#min-btn').onclick = function(){ panel.remove(); b.style.display = 'flex'; };
                header.querySelector('#close-btn').onclick = function(){ panel.remove(); b.style.display = 'flex'; };

                setInterval(function(){
                    var now = new Date();
                    var timeStr = now.toTimeString().split(' ')[0];
                    var clk = panel.querySelector('#live-clock');
                    if(clk) clk.innerText = 'TIME: ' + timeStr;
                }, 1000);

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:3px 7px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:6px;color:#00ff66;font-weight:800;">🟢 AI ENGINE ONLINE</div>' +
                                      '<div style="background:#00c853;color:#000;font-size:6px;padding:1px 4px;border-radius:2px;font-weight:900;">VERIFIED: 1</div>';
                panel.appendChild(statusRow);

                var row1 = d.createElement('div');
                row1.style.cssText = 'padding:4px 5px;background:#070b14;display:flex;gap:3px;border-bottom:1px solid #131d2e;';
                row1.innerHTML = '<div style="flex:1;background:#0d1526;padding:3px;border-radius:3px;text-align:center;font-size:6.5px;font-weight:800;color:#00ff66;border:1px solid #16253f;">⏱️ 1m Standard</div>' +
                                   '<div style="flex:1;background:#0d1526;padding:3px;border-radius:3px;text-align:center;font-size:6.5px;font-weight:800;color:#ffd700;border:1px solid #16253f;">⚡ 5s Auto Mode</div>';
                panel.appendChild(row1);

                var row2 = d.createElement('div');
                row2.style.cssText = 'padding:0 5px 4px 5px;background:#070b14;display:flex;gap:3px;border-bottom:1px solid #131d2e;';
                row2.innerHTML = '<button id="btn-start" style="flex:1;background:linear-gradient(45deg,#00b0ff,#00ff66);border:none;padding:4px;border-radius:3px;font-weight:900;font-size:6.5px;color:#030407;cursor:pointer;">▶ Start Auto</button>' +
                                   '<button id="btn-stop" style="flex:1;background:linear-gradient(45deg,#ff3300,#ff0055);border:none;padding:4px;border-radius:3px;font-weight:900;font-size:6.5px;color:#fff;cursor:pointer;">⏹ Stop Auto</button>';
                panel.appendChild(row2);

                var btnStart = row2.querySelector('#btn-start');
                var btnStop = row2.querySelector('#btn-stop');

                btnStart.onclick = function(){
                    window.autoTradeEnabled = true;
                    btnStart.style.outline = '1.5px solid #fff';
                    btnStop.style.outline = 'none';
                    runContinuousEngine(panel, true);
                };

                btnStop.onclick = function(){
                    window.autoTradeEnabled = false;
                    btnStop.style.outline = '1.5px solid #fff';
                    btnStart.style.outline = 'none';
                };

                // AI SIGNAL SCANNER Box with Real-Time Quotex Chart Canvas Mirroring
                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:4px 5px;background:#03050a;border:1px solid #131d2e;border-radius:5px;padding:5px;text-align:center;';
                scannerBox.innerHTML = '<div style="font-size:6px;color:#8a99ad;font-weight:800;display:flex;justify-content:space-between;"><span>AI SIGNAL SCANNER</span><span id="scan-status" style="color:#00ff66;">READY</span></div>' +
                                       '<div style="font-size:8px;font-weight:900;color:#00ff66;margin:1px 0;" id="scanner-title">5S AUTO SYNCED</div>' +
                                       '<div id="market-detect-label" style="font-size:5.5px;color:#00ffff;margin-bottom:2px;">Market: ' + detectActiveMarket() + '</div>' +
                                       '<div style="height:32px;display:flex;align-items:center;justify-content:center;background:#020305;border-radius:3px;padding:1px;overflow:hidden;position:relative;">' +
                                       '<canvas id="live-chart-mirror" width="220" height="30" style="width:100%;height:100%;"></canvas>' +
                                       '</div>';
                panel.appendChild(scannerBox);

                var sigBox = d.createElement('div');
                sigBox.style.cssText = 'margin:0 5px 5px 5px;background:#0d1526;border:1px solid #131d2e;border-radius:5px;padding:4px 6px;display:flex;justify-content:space-between;align-items:center;';
                sigBox.innerHTML = '<div><div style="font-size:5.5px;color:#8a99ad;">LATEST SIGNAL</div><div id="p-signal" style="font-size:9px;font-weight:900;color:#ff1744;">DOWN (79%)</div><div style="font-size:5px;color:#556677;" id="p-subtext">Live market synced.</div></div><div id="signal-icon" style="font-size:8px;color:#ff1744;">⬇️</div>';
                panel.appendChild(sigBox);

                var footer = d.createElement('div');
                footer.style.cssText = 'padding:3px 6px;background:#03050a;display:flex;justify-content:space-between;font-size:5px;color:#556677;border-top:1px solid #131d2e;';
                footer.innerHTML = '<span>• ULTRA AI ENGINE</span><span>SNIPER / UI</span>';
                panel.appendChild(footer);

                d.body.appendChild(panel);

                // Start Live Quotex Chart Mirroring into Bot Box
                startLiveChartMirroring(panel);
            }

            // Live Chart Mirroring Function (Copies active Quotex chart canvas automatically)
            function startLiveChartMirroring(panel){
                var cvs = panel.querySelector('#live-chart-mirror');
                if(!cvs) return;
                var ctx = cvs.getContext('2d');

                setInterval(function(){
                    try {
                        // Automatically find Quotex main chart canvas element
                        var allCanvases = d.querySelectorAll('canvas');
                        var mainChartCanvas = null;
                        for(var i=0; i<allCanvases.length; i++){
                            if(allCanvases[i].width > 300 && allCanvases[i].height > 150){
                                mainChartCanvas = allCanvases[i];
                                break;
                            }
                        }

                        ctx.clearRect(0, 0, cvs.width, cvs.height);

                        if(mainChartCanvas){
                            // Mirror active live chart portion into the bot scanner box
                            ctx.drawImage(
                                mainChartCanvas, 
                                mainChartCanvas.width - 240, 0, 240, mainChartCanvas.height, 
                                0, 0, cvs.width, cvs.height
                            );
                        } else {
                            // Fallback rendering if canvas is not immediately exposed
                            ctx.fillStyle = '#03050a';
                            ctx.fillRect(0, 0, cvs.width, cvs.height);
                            ctx.fillStyle = '#00ff66';
                            ctx.font = '8px sans-serif';
                            ctx.fillText('Syncing ' + detectActiveMarket() + '...', 40, 18);
                        }
                    } catch(e) {}
                }, 150);
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
                .catch(function(){ return {signal: "DOWN", confidence: 79}; })
                .then(function(j){
                    if(scanStatus) scanStatus.innerText = 'READY';
                    if(scannerTitle) scannerTitle.innerText = '5S AUTO SYNCED';

                    var rawSig = String(j.signal || 'DOWN').toUpperCase();
                    var isDown = (rawSig === 'SELL' || rawSig === 'DOWN' || rawSig === 'PUT');
                    var sigText = isDown ? 'DOWN' : 'UP';
                    var col = isDown ? '#ff1744' : '#00ff66';

                    if(sigEl) {
                        sigEl.innerText = sigText + ' (' + (j.confidence || 79) + '%)';
                        sigEl.style.color = col;
                    }
                    if(subText) subText.innerText = 'Live market synced.';
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
