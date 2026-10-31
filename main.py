import asyncio
import logging
import os
from pyquotex.stable_api import Quotex
from app import run_flask

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("SniperBotMasterRunner")

async def main():
    logger.info("🌐 Starting Flask Keep-Alive Server...")
    try:
        client = Quotex(
            email=os.environ.get("QX_EMAIL", "your_quotex_email@gmail.com"), 
            password=os.environ.get("QX_PASSWORD", "your_quotex_password"),
            lang="en",
            host="qxbroker.com"
        )
        check, reason = await client.connect()
        if check:
            logger.info("✅ SUCCESS: Connected to Quotex Direct Live Data Stream!")
            await client.subscribe_candles("EURUSD_otc", 60)
    except Exception as e:
        logger.warning(f"⚠️ Notice: {e}")

    while True:
        try:
            await asyncio.sleep(10)
        except Exception:
            await asyncio.sleep(5)

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped manually.")
