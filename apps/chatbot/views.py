
from django.shortcuts import render
from django.http import JsonResponse

# Importaciones locales solo dentro de la función para evitar ciclos de importación
def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        
        # Importar las funciones y el archivo de intents desde predictor.py
        from .predictor import predict_class, get_response, intents
        
        # Usar las funciones predict_class y get_response para obtener la respuesta
        inst = predict_class(user_message)  # Predicción de la intención del mensaje
        response_message = get_response(inst, intents)  # Obtención de la respuesta según la intención
        
        # Retornar la respuesta en formato JSON
        return JsonResponse({"response": response_message})
        
    # Si no es una solicitud POST, renderizar la plantilla del chatbot
    return render(request, "chatbot/chatbot.html")
