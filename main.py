"""消息格式化插件 - 将动作描写和对话分开发送"""

from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.api import logger


@register("astrbot_plugin_starfate_message_formatter", "YHJM", "StarFate 消息格式化", "1.0.0")
class MessageFormatterPlugin(Star):

    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.name = "astrbot_plugin_starfate_message_formatter"
        logger.info("消息格式化插件已加载")

    @filter.on_llm_response()
    async def on_llm_response(self, event, *args, **kwargs):
        """拦截 LLM 回复，将动作描写和对话分开发送"""
        
        # 获取消息文本
        text = getattr(event, 'message_str', '') or ''
        
        # DEBUG：输出收到的原始文本
        logger.info(f"[DEBUG] 收到消息文本: '{text[:200]}'")

        if not text:
            logger.info("[DEBUG] 文本为空，跳过")
            return

        # 检查是否包含动作描写结尾符号
        if '）。' not in text:
            logger.info("[DEBUG] 不包含 '）。'，跳过")
            return

        # 按第一个 "）。" 分割
        parts = text.split('）。', 1)
        action = parts[0].strip() + '）。'
        dialogue = parts[1].strip()

        logger.info(f"[DEBUG] 动作描写: '{action}'")
        logger.info(f"[DEBUG] 对话内容: '{dialogue}'")

        # 如果对话部分为空，不做处理
        if not dialogue:
            logger.info("[DEBUG] 对话部分为空，跳过")
            return

        # 阻止原始消息
        event.stop_event()
        logger.info("[DEBUG] 已阻止原始消息")

        # 发送动作描写
        await event.send(action)
        logger.info("[DEBUG] 已发送动作描写")

        # 发送对话内容
        await event.send(dialogue)
        logger.info("[DEBUG] 已发送对话内容")

    async def terminate(self):
        logger.info("消息格式化插件已卸载")
