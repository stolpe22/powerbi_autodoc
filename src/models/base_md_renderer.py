from abc import ABC, abstractmethod

class BaseMDRenderer(ABC):
    """
    Classe base abstrata para renderizadores de Markdown.
    """
    @abstractmethod
    def render(self, *args, **kwargs) -> str:
        pass