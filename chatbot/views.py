import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ChatSession, ChatMessage
from timetables.models import Timetable
from timetables.scheduler import get_timetable_context_for_ai


def get_groq_client():
    try:
        from groq import Groq
        return Groq(api_key=settings.GROQ_API_KEY)
    except Exception:
        return None


SYSTEM_PROMPT = """You are SchedualAI Assistant, an expert AI chatbot for school and college timetable management.
You help users:
- Understand their timetable structure and scheduling
- Answer questions about class schedules, faculty assignments, conflicts
- Suggest improvements to scheduling
- Explain how the system works
- Analyze workload distribution

Be concise, helpful, and friendly. When given timetable context, use it to give specific answers.
If asked about conflicts, check the provided data carefully.
Format responses clearly using bullet points or numbered lists when helpful.
"""


@login_required
def chatbot_home(request):
    timetables = Timetable.objects.filter(owner=request.user)
    sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')[:10]
    active_tt_id = request.GET.get('timetable')
    active_tt = None
    if active_tt_id:
        active_tt = Timetable.objects.filter(pk=active_tt_id, owner=request.user).first()

    session = None
    if active_tt:
        session, _ = ChatSession.objects.get_or_create(
            user=request.user,
            timetable=active_tt,
            defaults={}
        )

    ctx = {
        'timetables': timetables,
        'sessions': sessions,
        'active_tt': active_tt,
        'session': session,
        'messages': session.messages.all() if session else [],
    }
    return render(request, 'chatbot/home.html', ctx)


@login_required
def send_message(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_message = data.get('message', '').strip()
    session_id = data.get('session_id')
    timetable_id = data.get('timetable_id')

    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    # Get or create session
    if session_id:
        try:
            session = ChatSession.objects.get(pk=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(user=request.user)
    else:
        tt = None
        if timetable_id:
            tt = Timetable.objects.filter(pk=timetable_id, owner=request.user).first()
        session = ChatSession.objects.create(user=request.user, timetable=tt)

    # Save user message
    ChatMessage.objects.create(session=session, role='user', content=user_message)

    # Build message history for Groq
    history = list(session.messages.order_by('created_at')[:20])
    groq_messages = []

    # Add timetable context if available
    if session.timetable:
        tt_context = get_timetable_context_for_ai(session.timetable)
        groq_messages.append({
            'role': 'user',
            'content': f"[TIMETABLE CONTEXT]\n{tt_context}\n[END CONTEXT]\n\nPlease use this context to answer my questions."
        })
        groq_messages.append({
            'role': 'assistant',
            'content': f"I have loaded the timetable '{session.timetable.name}'. I'm ready to answer your questions about it!"
        })

    # Add conversation history (skip first 2 if context was added)
    start_idx = 0
    for msg in history[start_idx:-1]:  # exclude the message we just saved
        groq_messages.append({
            'role': msg.role,
            'content': msg.content
        })
    groq_messages.append({'role': 'user', 'content': user_message})

    # Call Groq API
    client = get_groq_client()
    if not client:
        reply = "⚠️ AI service unavailable. Please set GROQ_API_KEY in your environment."
    else:
        try:
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[{'role': 'system', 'content': SYSTEM_PROMPT}] + groq_messages,
                max_tokens=1024,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Error calling AI: {str(e)}"

    # Save assistant reply
    ChatMessage.objects.create(session=session, role='assistant', content=reply)

    return JsonResponse({
        'reply': reply,
        'session_id': session.id,
    })


@login_required
def clear_session(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
    session.messages.all().delete()
    return JsonResponse({'ok': True})
