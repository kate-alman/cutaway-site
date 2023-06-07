from config import config
from runner import run

from tg_bot.poller import Poller
from tg_bot.sender import TgSender
from tg_bot.worker import BotWorker


if __name__ == "__main__":
    poller = Poller(cfg=config)
    worker = BotWorker(cfg=config)
    sender = TgSender(cfg=config)
    run(
        start_tasks=[poller.start, sender.start, worker.start],
        stop_tasks=[poller.stop, sender.stop, worker.stop],)
