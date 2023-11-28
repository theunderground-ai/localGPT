from queue import Queue
from queue import Empty
from threading import Thread
import time
from typing import Any, Dict, List, Union
from langchain.callbacks.base import BaseCallbackHandler
from llama_cpp import Generator
from langchain.schema import AgentAction, AgentFinish

class QueueCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue):
        super()
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # print(f'on_llm_new_token: {token}')
        self.queue.put(
            {
                "event": "message",
                "id": "message_id",
                "retry": 1,
                "data": token,
            }
        )

    def on_llm_end(self, *args, **kwargs) -> Any:
        # print('on_llm_end')
        return self.queue.empty()

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # print('on_llm_start')
        """Run when LLM starts running."""

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        # print('on_llm_error')
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        # print('on_chain_start')
        """Run when chain starts running."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        # print('on_chain_end')

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Run when chain errors."""
        # print('on_chain_error')

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Run when tool starts running."""
        # print('on_tool_start')

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        pass

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Run when tool ends running."""
        # print('on_tool_end')

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        # print('on_tool_error')
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run on arbitrary text."""
        # print('on_text')

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""
        # print('on_agent_finish')


def stream(cb: Any, input, queue: Queue) -> Generator:
    job_done = object()
    def task(input):
        x = cb(input)
        # print('job done')
        queue.put(job_done)

    t = Thread(target=task, args=[input])
    t.start()

    while True:
        try:
            item = queue.get(True, timeout=1)
            if item is job_done:
                # print('got job done')
                break

            # print(f'yield with None: {item is None}')
            yield item
        except Empty:
            # print('queue is empty')
            continue
