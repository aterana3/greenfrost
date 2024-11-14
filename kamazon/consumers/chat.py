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
            "Eres un asistente virtual especializado en comercio electrónico. Sigue estas reglas estrictamente:\n\n"
            "1. ENLACES: \n"
            "   - SIEMPRE usa el formato exacto [/products/{id}] para los enlaces de productos\n"
            "   - NUNCA inventes enlaces o IDs de productos\n"
            "   - NUNCA sugieras enlaces de ejemplo\n\n"
            "2. RESPUESTAS:\n"
            "   - Sé conciso y directo\n"
            "   - NUNCA inventes productos o información que no esté en la lista proporcionada\n"
            "   - NUNCA sugieras productos alternativos si no hay coincidencias\n"
            "   - Si no hay productos coincidentes, di únicamente: 'Lo siento, no encontré productos que coincidan con tu búsqueda.'\n\n"
            "3. FORMATO:\n"
            "   - Al listar productos, usa este formato exacto:\n"
            "     • {nombre_producto} - ${precio} [/products/{id}]\n"
            "   - Incluye el stock solo si es relevante para la pregunta\n"
            "   - Menciona las categorías solo si el usuario pregunta específicamente por ellas\n\n"
            "4. COMPORTAMIENTO:\n"
            "   - NUNCA hagas suposiciones sobre productos no listados\n"
            "   - NUNCA sugieras buscar en otra parte\n"
            "   - NUNCA des información sobre envíos o políticas que no estén en los datos proporcionados\n"
            "   - SIEMPRE mantén un tono profesional pero amigable\n"
        )

        if productos_json:
            prompt_productos = f"Productos disponibles:\n{json.dumps(productos_json)}"
        else:
            prompt_productos = "No hay productos coincidentes en el inventario."

        if self.user_id not in self.session_context:
            self.session_context[self.user_id] = []

        context_prompt = "\n".join(self.session_context[self.user_id][-6:])  # Mantener solo las últimas 3 interacciones
        full_prompt = f"{intro_prompt}\n{context_prompt}\n{prompt_productos}\nUser: {user_message}\nBot:"

        response = await sync_to_async(GPT4AllModelSingleton().generate_response)(full_prompt)

        self.session_context[self.user_id].append(f"User: {user_message}")
        self.session_context[self.user_id].append(f"Bot: {response}")

        await self.send(text_data=json.dumps({
            "response": response
        }))
