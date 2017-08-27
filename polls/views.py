from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Question
from django.shortcuts import get_object_or_404,redirect
from .models import Choice
from .forms import MyForm
from .forms import VoteForm
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import resolve_url
from django.contrib import messages
from django.urls import reverse



# Create your views here.
def index(request):
    return render(request,'polls/index.html',{
        'questions': Question.objects.all(),
    })


def vote(request,pk):
    question = get_object_or_404(Question,pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'poll/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return redirect(reverse('polls:poll_results'), pk=pk)
    # return redirect('results_url', pk=pk)


def results(request,pk):
    obj = get_object_or_404(Question,pk=pk)
    return render(request,'polls/results.html',{
        'question':obj,
    })

class FormTest(FormView):
   form_class = MyForm
   template_name = 'polls/form.html'
   success_url = reverse_lazy('polls:index')
form_test = FormTest.as_view()

class Detail(SingleObjectMixin,FormView):
    model = Question
    form_class = VoteForm
    context_object_name = 'question'
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question'] = self.object
        return kwargs

    def form_valid(self, form):
        form.vote()
        choice = form.cleaned_data['choice']
        messages.success(self.request,'"%s"に投票しました' % choice)
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('polls:results',self.kwargs['pk'])

detail = Detail.as_view()


