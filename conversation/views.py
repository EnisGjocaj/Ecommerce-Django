from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def new_conversation(request, item_pk):
	item = get_object_or_404(Item, pk=item_pk)

	if item.created_by == request.user:
		return redirect('dashboard:index')

	conversation = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

	if conversation:
		redirect('conversation:detail', pk=conversation.first().id)
	
	if request.method == "POST":
		form = ConversationMessageForm(request.POST)

		if form.is_valid():
			conversation = Conversation.objects.create(item=item)
			conversation.members.add(request.user)
			conversation.members.add(item.created_by)
			conversation.save()

			conversation_message = form.save(commit=False)
			conversation_message.conversation = conversation
			conversation_message.created_by = request.user
			# conversation.save()
			conversation_message.save()

			return redirect('item:detail', pk=item_pk)
	else:
			form = ConversationMessageForm()

	return render(request, 'conversation/new.html', {
		'form': form,
	})

# @login_required
# def index(request):
# 	conversation = Conversation.objects.filter(members__in=[request.user.id])

# 	return render(request, 'conversation/inbox.html', {
# 		'conversation': conversation,
# 	})

@login_required
def index(request):
    if request.user.is_staff:
        # If the user is an admin, fetch all conversations
        conversations = Conversation.objects.all()
    else:
        # If the user is a regular user, fetch conversations initiated by the user
        conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })


@login_required
def detail(request, pk):
    conversation = Conversation.objects.get(pk=pk)

    # Ensure that the user is a member of the conversation or is an admin
    if request.user.is_staff or request.user in conversation.members.all():
        messages = conversation.messages.all()  # Use the correct related_name here
        return render(request, "conversation/detail.html", {
            'conversation': conversation,
            'messages': messages,
        })
    else:
        # Redirect or display an error message if the user does not have permission to view this conversation
        return HttpResponse("You do not have permission to view this conversation.")




# @login_required
# def detail(request, pk):
# 	conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

# 	if request.method == "POST":
# 		form = ConversationMessageForm(request.POST)

# 		if form.is_valid():
# 			conversation_message = form.save(commit=False)
# 			conversation_message.conversation = conversation
# 			conversation_message.created_by = request.user
# 			conversation_message.save()

# 			conversation.save()

# 			return redirect('conversation:detail', pk=pk)
# 	else:
# 		form = ConversationMessageForm()


# 	return render(request, "conversation/detail.html", {
# 		'conversation': conversation,
# 		'form': form,
# 	})
