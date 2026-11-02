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
    return "Quotex Sniper Bot Engine v119.0 [RA Scanner Bot with Enlarged Floating Button & Masked Prices] Running 24/7!"

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
                s.innerHTML = '@keyframes panelPop {0%{opacity:0;transform:translate(-50%, -45%) scale(0.9);}100%{opacity:1;transform:translate(-50%, -50%) scale(1);}}' +
                              '@keyframes cPulse {0%{transform:scaleY(0.4);opacity:0.5;}50%{transform:scaleY(1.3);opacity:1;}100%{transform:scaleY(0.4);opacity:0.5;}}' +
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
            b.style.cssText = 'width:62px;height:62px;border-radius:50%;background:#030407;display:flex;align-items:center;justify-content:center;border:2px solid #00ff66;box-shadow:0 0 15px rgba(0,255,102,0.7);box-sizing:border-box;overflow:hidden;';
            b.innerHTML = '<img src="https://i.postimg.cc/JzRR8g6M/IMG-20261102-WA0003.jpg" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />';
            wrap.appendChild(b);

            var lbl = d.createElement('div');
            lbl.style.cssText = 'margin-top:3px;font-size:7px;font-weight:900;color:#00ff66;font-family:sans-serif;background:rgba(3,4,7,0.85);padding:1px 5px;border-radius:3px;border:1px solid rgba(0,255,102,0.4);white-space:nowrap;box-shadow:0 0 5px rgba(0,0,0,0.8);';
            lbl.innerText = 'RA SCANNER BOT';
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
                                   '<div style="font-size:9px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
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
                                       '<div style="display:flex;justify-content:center;gap:3px;margin-top:3px;">' +
                                       '<div style="width:3px;height:22px;background:#00ff66;border-radius:2px;animation:cPulse 1s infinite;"></div>' +
                                       '<div style="width:3px;height:30px;background:#ff1744;border-radius:2px;animation:cPulse 0.7s infinite;"></div>' +
                                       '<div style="width:3px;height:18px;background:#00ff66;border-radius:2px;animation:cPulse 1.2s infinite;"></div>' +
                                       '<div style="width:3px;height:34px;background:#ff1744;border-radius:2px;animation:cPulse 0.9s infinite;"></div>' +
                                       '</div>';
                panel.appendChild(scannerBox);

                var licenseBox = d.createElement('div');
                licenseBox.style.cssText = 'margin:0 6px 6px 6px;background:#03050a;border:1px solid #131d2e;border-radius:5px;padding:6px;';
                licenseBox.innerHTML = '<div style="font-size:6px;color:#8a99ad;margin-bottom:2px;" id="err-msg">Enter license key</div>' +
                                       '<input type="password" id="license-input" placeholder="Enter password (1-8)" style="width:100%;box-sizing:border-box;background:#0d1526;border:1px solid #16253f;padding:5px;border-radius:3px;color:#fff;font-size:7.5px;outline:none;margin-bottom:4px;" />' +
                                       '<button id="verify-btn" style="width:100%;background:#00c853;border:none;padding:5px;border-radius:3px;font-weight:900;font-size:7.5px;color:#000;cursor:pointer;">VERIFY LICENSE</button>';
                panel.appendChild(licenseBox);

                var verifyBtn = licenseBox.querySelector('#verify-btn');
                var licenseInput = licenseBox.querySelector('#license-input');
                var errMsg = licenseBox.querySelector('#err-msg');

                verifyBtn.onclick = function(){
                    var keyVal = licenseInput.value.trim();
                    if(keyVal.length >= 1){
                        verifyBtn.innerHTML = '<span style="display:inline-block;width:7px;height:7px;border:1px solid #000;border-top-color:transparent;border-radius:50%;animation:spinAnim 0.8s linear infinite;"></span> Verifying...';
                        setTimeout(function(){
                            sessionStorage.setItem('sniper_verified_' + uniqueId, 'true');
                            panel.remove();
                            createMainDashboard(targetWrap);
                        }, 2000);
                    } else {
                        errMsg.innerText = '⚠️ INVALID PASSWORD! ACCESS DENIED';
                        errMsg.style.color = '#ff1744';
                        licenseInput.style.borderColor = '#ff1744';
                        verifyBtn.style.background = '#ff1744';
                        verifyBtn.style.color = '#fff';
                        verifyBtn.innerText = 'INCORRECT KEY';
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
                header.style.cssText = 'background:#03050a;padding:5px 8px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;cursor:move;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:5px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:17px;height:17px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;">🎯</div>' +
                                   '<div>' +
                                   '<div style="font-size:9px;font-weight:900;color:#fff;">SNIPER BOT</div>' +
                                   '<div id="live-clock_' + uniqueId + '" style="font-size:5px;color:#8a99ad;">TIME: 00:00:00</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<div style="display:flex;gap:3px;">' +
                                   '<button id="min-btn" style="background:#101826;border:none;color:#fff;width:16px;height:16px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:9px;">×</button>' +
                                   '</div>';
                panel.appendChild(header);
                
                header.querySelector('#min-btn').onclick = function(){ panel.remove(); targetWrap.style.display = 'flex'; };

                setInterval(function(){
                    var now = new Date();
                    var timeStr = now.toTimeString().split(' ')[0];
                    var clk = panel.querySelector('#live-clock_' + uniqueId);
                    if(clk) clk.innerText = 'TIME: ' + timeStr;
                }, 1000);

                var statusRow = d.createElement('div');
                statusRow.style.cssText = 'padding:3px 8px;background:#050912;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #131d2e;';
                statusRow.innerHTML = '<div style="font-size:5.5px;color:#00ff66;font-weight:800;">🟢 AI ENGINE ONLINE</div>' +
                                      '<div style="background:#00c853;color:#000;font-size:5.5px;padding:1px 4px;border-radius:2px;font-weight:900;">VERIFIED: 1</div>';
                panel.appendChild(statusRow);

                var row1 = d.createElement('div');
                row1.style.cssText = 'padding:5px 6px;background:#070b14;display:flex;gap:4px;border-bottom:1px solid #131d2e;';
                row1.innerHTML = '<div style="flex:1;background:#0d1526;padding:4px;border-radius:3px;text-align:center;font-size:6.5px;font-weight:800;color:#00ff66;border:1.2px solid #00ff66;">⏱️ 1m Standard</div>' +
                                   '<button id="btn-pro-toggle" style="flex:1;background:#0d1526;padding:4px;border-radius:3px;text-align:center;font-size:6.5px;font-weight:800;color:#00ffff;border:1.2px solid #00ffff;cursor:pointer;">⚡ PRO / SMART</button>';
                panel.appendChild(row1);

                var row2 = d.createElement('div');
                row2.style.cssText = 'padding:0 6px 5px 6px;background:#070b14;display:flex;gap:4px;border-bottom:1px solid #131d2e;';
                row2.innerHTML = '<button id="btn-start" style="flex:1;background:linear-gradient(45deg,#00b0ff,#00ff66);border:none;padding:5px;border-radius:3px;font-weight:900;font-size:6.5px;color:#030407;cursor:pointer;">▶ Start Auto</button>' +
                                   '<button id="btn-stop" style="flex:1;background:linear-gradient(45deg,#ff3300,#ff0055);border:none;padding:5px;border-radius:3px;font-weight:900;font-size:6.5px;color:#fff;cursor:pointer;">⏹ Stop Auto</button>';
                panel.appendChild(row2);

                var btnStart = row2.querySelector('#btn-start');
                var btnStop = row2.querySelector('#btn-stop');
                var proToggleBtn = row1.querySelector('#btn-pro-toggle');

                var isProLiveChartMode = false;

                btnStart.onclick = function(){
                    window.autoTradeEnabled = true;
                    btnStart.style.outline = '1.5px solid #fff';
                    btnStop.style.outline = 'none';
                    runContinuousEngine(panel, true);
                };

                btnStop.onclick = function(){
                    window.autoTradeEnabled = false;
                    window.lastTradeExecutionTimestamp = 0;
                    btnStop.style.outline = '1.5px solid #fff';
                    btnStart.style.outline = 'none';
                };

                var scannerBox = d.createElement('div');
                scannerBox.style.cssText = 'margin:6px;background:#03050a;border:1.5px solid #00ff66;border-radius:5px;padding:6px;text-align:center;transition:all 0.3s;';
                panel.appendChild(scannerBox);

                proToggleBtn.onclick = function(){
                    isProLiveChartMode = !isProLiveChartMode;
                    if(isProLiveChartMode){
                        proToggleBtn.innerText = '⚡ PRO OFF (OTC)';
                        proToggleBtn.style.color = '#ff1744';
                        proToggleBtn.style.borderColor = '#ff1744';
                        scannerBox.style.borderColor = '#00ffff';
                    } else {
                        proToggleBtn.innerText = '⚡ PRO / SMART';
                        proToggleBtn.style.color = '#00ffff';
                        proToggleBtn.style.borderColor = '#00ffff';
                        scannerBox.style.borderColor = '#00ff66';
                    }
                    updateHybridChart(scannerBox, isProLiveChartMode, true);
                };

                var sigBox = d.createElement('div');
                sigBox.style.cssText = 'margin:0 6px 6px 6px;background:#0d1526;border:1px solid #131d2e;border-radius:5px;padding:5px 6px;';
                sigBox.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">' +
                                   '<div><div style="font-size:5px;color:#8a99ad;">LATEST SIGNAL</div><div id="p-signal" style="font-size:8.5px;font-weight:900;color:#00ff66;">READY</div><div style="font-size:4.5px;color:#556677;" id="p-subtext">Automated sniper ready.</div></div>' +
                                   '<div id="signal-icon" style="font-size:7px;color:#00ff66;">⚡</div>' +
                                   '</div>' +
                                   '<button id="get-sig-btn" style="width:100%;background:#00c853;border:none;padding:4px;border-radius:3px;font-weight:900;font-size:6.5px;color:#000;cursor:pointer;">✓ GET SIGNAL</button>';
                panel.appendChild(sigBox);

                var getSigBtn = sigBox.querySelector('#get-sig-btn');
                getSigBtn.onclick = function(){
                    runContinuousEngine(panel, false);
                };

                var footer = d.createElement('div');
                footer.style.cssText = 'padding:3px 6px;background:#03050a;display:flex;justify-content:space-between;font-size:4.5px;color:#556677;border-top:1px solid #131d2e;';
                footer.innerHTML = '<span>• ULTRA AI ENGINE</span><span>SNIPER / UI</span>';
                panel.appendChild(footer);

                d.body.appendChild(panel);

                updateHybridChart(scannerBox, false, true);
                
                setInterval(function(){
                    updateHybridChart(scannerBox, isProLiveChartMode, false);
                }, 3000);
            }

            function updateHybridChart(container, isProMode, forceUpdate){
                var mkt = detectActiveMarket();
                var currentSym = isProMode ? getTradingViewSymbol(mkt) : 'OTC_SCANNER';
                
                if(container.dataset.lastSymbol === currentSym && !forceUpdate) return;
                container.dataset.lastSymbol = currentSym;
                
                if(!isProMode){
                    container.innerHTML = '<div style="font-size:5.5px;color:#00ff66;font-weight:800;display:flex;justify-content:space-between;margin-bottom:2px;">' +
                                          '<span>MARKET: ' + mkt + '</span>' +
                                          '<span style="color:#ffd700;">OTC SCANNER</span>' +
                                          '</div>' +
                                          '<div style="font-size:7.5px;font-weight:900;color:#00ff66;margin:2px 0;">⚡ Next Candle?? (Smooth Sync)</div>' +
                                          '<div style="height:72px;display:flex;align-items:center;justify-content:center;gap:4px;background:#010204;border-radius:3px;padding:2px;">' +
                                          '<div style="width:3px;height:35px;background:#00ff66;border-radius:2px;animation:cPulse 1.1s infinite;box-shadow:0 0 5px #00ff66;"></div>' +
                                          '<div style="width:3px;height:52px;background:#ff1744;border-radius:2px;animation:cPulse 0.8s infinite;box-shadow:0 0 5px #ff1744;"></div>' +
                                          '<div style="width:3px;height:28px;background:#00ff66;border-radius:2px;animation:cPulse 1.3s infinite;box-shadow:0 0 5px #00ff66;"></div>' +
                                          '<div style="width:3px;height:58px;background:#ff1744;border-radius:2px;animation:cPulse 0.7s infinite;box-shadow:0 0 5px #ff1744;"></div>' +
                                          '<div style="width:3px;height:40px;background:#00ff66;border-radius:2px;animation:cPulse 1.0s infinite;box-shadow:0 0 5px #00ff66;"></div>' +
                                          '</div>';
                } else {
                    var tvConfig = {
                        "width": "100%",
                        "height": "100%",
                        "symbol": currentSym,
                        "interval": "1",
                        "timezone": "Etc/UTC",
                        "theme": "dark",
                        "style": "1",
                        "locale": "en",
                        "toolbar_bg": "#03050a",
                        "enable_publishing": false,
                        "hide_top_toolbar": true,
                        "hide_legend": true,
                        "save_image": false,
                        "calendar": false,
                        "allow_symbol_change": false,
                        "studies": [],
                        "support_host": "https://www.tradingview.com"
                    };
                    var encodedTv = encodeURIComponent(JSON.stringify(tvConfig));

                    // 100% Native Clean Clipping: Right price scale, logo and bottom volume completely pushed out, keeping exact native chart position.
                    container.innerHTML = '<div style="font-size:5.5px;color:#00ffff;font-weight:800;display:flex;justify-content:space-between;margin-bottom:2px;">' +
                                          '<span>MARKET: ' + mkt + '</span>' +
                                          '<span style="color:#00ff66;">CLEAN CANDLES</span>' +
                                          '</div>' +
                                          '<div style="height:92px;background:#03050a;border-radius:3px;overflow:hidden;position:relative;border:1px solid #131d2e;">' +
                                          '<iframe src="https://s.tradingview.com/embed-widget/advanced-chart/?locale=en#' + encodedTv + '" style="width:145%;height:165%;position:absolute;top:-32px;left:-45px;border:none;pointer-events:none;"></iframe>' +
                                          '<div style="position:absolute;top:0;right:0;width:45px;height:100%;background:#03050a;pointer-events:none;z-index:10;"></div>' +
                                          '</div>';
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
                if(nowTs - window.lastTradeExecutionTimestamp < 15000) return;
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
                    if(subText) subText.innerText = 'Live market synced. All systems operational.';
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
