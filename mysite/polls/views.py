from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from polls.models import Poll, Choice
from polls.utils import ViewNames

def index(request):
	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	return render(request, ViewNames.polls_index, {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
	return render(request, ViewNames.polls_detail, {'poll':get_poll(poll_id)})

def results(request, poll_id):
    return HttpResponse("You're looking at te results of poll %s." %poll_id)

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except KeyError, Choice.DoesNotExist:
		return render(request, 'polls/detail.html', {'poll':p, 'error_message':"You didn't choose"})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))