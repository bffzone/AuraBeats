    async def play_now(self, track: dict, bot_client=None) -> bool:
        try:
            if bot_client:
                await self.ensure_assistant(bot_client)
            url = get_stream_url(track["url"], video_id=track.get("video_id"))
            calls_manager = _calls()
            await calls_manager.play(self.chat_id, url)
            await queue_manager.set_current(self.chat_id, track)
            logger.info(f"Now playing: {track['title'][:40]}")
            return True
        except Exception as e:
            logger.error(f"play_now: {e}")
            raise
