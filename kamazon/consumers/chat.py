import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from apps.core.GPT4AllModel import GPT4AllModelSingleton
from kamazon.utils import filter_products_keywords, generate_json_response


class ChatBotConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None
        self.session_context = None

    async def connect(self):
        self.user_id = self.scope["user"].id if self.scope["user"].is_authenticated else self.channel_name
        self.session_context = {}
        await self.accept()

    async def disconnect(self, close_code):
        if self.user_id in self.session_context:
            del self.session_context[self.user_id]

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get("message", "")

        products = await sync_to_async(filter_products_keywords)(user_message)
        productos_json = await sync_to_async(generate_json_response)(products)

        intro_prompt = (
            "Eres un asistente virtual para un ecommerce. "
            "Tu tarea es ayudar a los clientes con preguntas sobre productos, como precios, disponibilidad, categorías, "
            "y enlaces de compra. Si el cliente pregunta por productos específicos y se encuentran coincidencias, "
            "proporciónales la lista de productos relevantes. Si no se encuentran coincidencias, informa que no hay productos disponibles.\n"
            "Responde de manera amigable y profesional, siendo breve pero informativo en cada respuesta.",
            "Responde sin ofrecer soluciones alternativas.",
        )

        if productos_json:
            prompt_productos = f"Lista de productos:\n{json.dumps(productos_json)}"
        else:
            prompt_productos = "No se encontraron productos relevantes."

        if self.user_id not in self.session_context:
            self.session_context[self.user_id] = []

        context_prompt = "\n".join(self.session_context[self.user_id])
        full_prompt = f"{intro_prompt}\n{context_prompt}\n{prompt_productos}\nUser: {user_message}\nBot:"

        response = await sync_to_async(GPT4AllModelSingleton().generate_response)(full_prompt)

        self.session_context[self.user_id].append(f"User: {user_message}")
        self.session_context[self.user_id].append(f"Bot: {response}")

        await self.send(text_data=json.dumps({
            "response": response
        }))
