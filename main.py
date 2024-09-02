import signal
import sys
import asyncio
from bot import Bot

# Create an instance of your bot
bot = Bot()

async def main():
    await bot.start()
    print("Bot is running...")
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Bot is shutting down...")
    finally:
        await bot.stop()
        print("Bot stopped.")

async def stop_loop_after_cancellation(loop):
    # Wait for all tasks to be cancelled
    await asyncio.gather(*asyncio.all_tasks(loop=loop), return_exceptions=True)
    loop.stop()

def handle_sigterm(signum, frame):
    print("Received SIGTERM. Shutting down gracefully...")
    loop = asyncio.get_event_loop()

    # Cancel all tasks and schedule loop to stop after cancellation is done
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()

    asyncio.ensure_future(stop_loop_after_cancellation(loop))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Register signal handler for SIGTERM
    signal.signal(signal.SIGTERM, handle_sigterm)

    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Exception during loop: {e}")
    finally:
        # Ensure all tasks are completed
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop=loop), return_exceptions=True))
        loop.close()
