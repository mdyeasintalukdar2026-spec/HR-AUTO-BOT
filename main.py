import asyncio
import logging
import os
from pyquotex.stable_api import Quotex
from app import start_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("SniperBotMasterRunner")

async def main():
    start_server()
    logger.info("🌐 Flask Keep-Alive Server Started Successfully on Port 8080.")
    
    client = Quotex(
        email=os.environ.get("QX_EMAIL", "your_quotex_email@gmail.com"), 
        password=os.environ.get("QX_PASSWORD", "your_quotex_password"),
        lang="en",
        host="qxbroker.com"
    )
    
    logger.info("📡 Connecting to Quotex WebSocket Live Server...")
    check, reason = await client.connect()
    
    if check:
        logger.info("✅ SUCCESS: Connected to Quotex Direct Live Data Stream!")
        
        asset = "EURUSD_otc"
        await client.subscribe_candles(asset, 60)
        
        while True:
            try:
                live_candles = client.get_realtime_candles(asset)
                if live_candles:
                    logger.info(f"🕯️ Verified Real-Time Candle Feed [{asset}]: {live_candles}")
                else:
                    logger.info("⚠️ Waiting for stable candle stream synchronization...")
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Error in Live Data Loop: {e}")
                await asyncio.sleep(2)
    else:
        logger.error(f"❌ Connection Failed: {reason}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped manually by user.")
