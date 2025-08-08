from django.shortcuts import redirect
from .forms import JockeyForm, RacehorseForm, RaceForm, ParticipationForm
from .models import Jockey, Racehorse, Race, Participation
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.views import View
from django.utils.decorators import method_decorator
import json

class IndexView(View):
    def get(self, request):
        return JsonResponse({"message": "Welcome to the Racehorse ORM API"})

@method_decorator(csrf_exempt, name='dispatch')
class JockeyListView(View):
    # GET: Returns a list of the jockeys in json format
    def get(self, request):
        jockeys = Jockey.objects.all()
        return JsonResponse({"jockeys": [model_to_dict(jockey) for jockey in jockeys]})

@method_decorator(csrf_exempt, name='dispatch')
class JockeyDetailView(View):
    # GET: Returns the specific details of a jockey in json format
    def get(self, request, pk):
        try:
            jockey = Jockey.objects.get(pk=pk)
            jockey_data = model_to_dict(jockey)

            participations = Participation.objects.filter(jockey=jockey)
            participation_data = []
            for p in participations:
                participation_data.append({
                    "id": p.id,
                    "race_id": p.race.id,
                    "race_name": p.race.name,
                    "racehorse_id": p.racehorse.id,
                    "racehorse_name": p.racehorse.name,
                    "position": p.position,
                    "is_winner": p.is_winner
                })
            jockey_data["participations"] = participation_data
            return JsonResponse(jockey_data)
        except Jockey.DoesNotExist:
            raise Http404("Jockey not found")
    # POST: Updates a jockeys information and returns a copy in json format
    @csrf_exempt
    def post(self, request, pk):
        try:
            jockey = Jockey.objects.get(pk=pk)
            data = json.loads(request.body)
            form = JockeyForm(data, instance=jockey)
            if form.is_valid():
                form.save()
                return JsonResponse(model_to_dict(jockey))
            else:
                return JsonResponse(form.errors, status=400)
        except Jockey.DoesNotExist:
            raise Http404("Jockey not found")
    # DELETE: Deletes a jockey from database
    @csrf_exempt
    def delete(self, request, pk):
        try:
            jockey = Jockey.objects.get(pk=pk)
            jockey.delete()
            return JsonResponse({"message": "Jockey deleted successfully"})
        except Jockey.DoesNotExist:
            raise Http404("Jockey not found")
        
@method_decorator(csrf_exempt, name='dispatch')
class JockeyCreateView(View):
    # POST: Adds a new jockey
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        form = JockeyForm(data)
        if form.is_valid():
            jockey = form.save()
            return JsonResponse(model_to_dict(jockey), status=201)
        else:
            return JsonResponse(form.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class RacehorseListView(View):
    # GET: Returns a list of the racehorses in json format
    def get(self, request):
        racehorses = Racehorse.objects.all()
        return JsonResponse({"racehorses": [model_to_dict(racehorse) for racehorse in racehorses]})

@method_decorator(csrf_exempt, name='dispatch')
class RacehorseDetailView(View):
    # GET: Returns the specific details of a racehorse in json format
    def get(self, request, pk):
        try:
            racehorse = Racehorse.objects.get(pk=pk)
            racehorse_data = model_to_dict(racehorse)

            participations = Participation.objects.filter(racehorse=racehorse)
            participation_data = []
            for p in participations:
                participation_data.append({
                    "id": p.id,
                    "race_id": p.race.id,
                    "race_name": p.race.name,
                    "jockey_id": p.jockey.id,
                    "jockey_name": p.jockey.name,
                    "position": p.position,
                    "is_winner": p.is_winner
                })
            racehorse_data["participations"] = participation_data
            return JsonResponse(racehorse_data)
        except Racehorse.DoesNotExist:
            raise Http404("Racehorse not found")
    # POST: Updates a racehorse's information and returns a copy in json format
    @csrf_exempt
    def post(self, request, pk):
        try:
            racehorse = Racehorse.objects.get(pk=pk)
            data = json.loads(request.body)
            form = RacehorseForm(data, instance=racehorse)
            if form.is_valid():
                form.save()
                return JsonResponse(model_to_dict(racehorse))
            else:
                return JsonResponse(form.errors, status=400)
        except Racehorse.DoesNotExist:
            raise Http404("Racehorse not found")
    # Deletes a racehorse from database
    @csrf_exempt
    def delete(self, request, pk):
        try:
            racehorse = Racehorse.objects.get(pk=pk)
            racehorse.delete()
            return JsonResponse({"message": "Racehorse deleted successfully"})
        except Racehorse.DoesNotExist:
            raise Http404("Racehorse not found")
        
@method_decorator(csrf_exempt, name='dispatch')
class RacehorseCreateView(View):
    # POST: Adds a new racehorse
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        form = RacehorseForm(data)
        if form.is_valid():
            racehorse = form.save()
            return JsonResponse(model_to_dict(racehorse), status=201)
        else:
            return JsonResponse(form.errors, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class RaceListView(View):
    # GET: Returns a list of the races in json format
    def get(self, request):
        races = Race.objects.all()
        return JsonResponse({'races' : [model_to_dict(race) for race in races]})
    
@method_decorator(csrf_exempt, name='dispatch')
class RaceDetailView(View):
    # GET: Returns the specific details of a racehorse in json format
    def get(self, request, pk):
        try:
            race = Race.objects.get(pk=pk)
            race_data = model_to_dict(race)
            
            participations = Participation.objects.filter(race=race)
            participation_data = []
            for p in participations:
                participation_data.append({
                    "id": p.id,
                    "racehorse_id": p.racehorse.id,
                    "racehorse_name": p.racehorse.name,
                    "jockey_id": p.jockey.id,
                    "jockey_name": p.jockey.name,
                    "position": p.position,
                    "is_winner": p.is_winner
                })
            race_data['participations'] = participation_data
            return JsonResponse(race_data)
        except Race.DoesNotExist:
            raise Http404("Race not found")
    # POST: Updates a race's information and returns a copy in json format
    @csrf_exempt
    def post(self, request, pk):
        try:
            race = Race.objects.get(pk=pk)
            data = json.loads(request.body)
            form = RaceForm(data, instance=race)
            if form.is_valid():
                form.save()
                return JsonResponse(model_to_dict(race))
            else:
                return JsonResponse(form.errors, status=400)
        except Race.DoesNotExist:
            raise Http404("Race not found")
    # DELETE: Deletes a racehorse from database
    @csrf_exempt
    def delete(self, request, pk):
        try:
            race = Race.objects.get(pk=pk)
            race.delete()
            return JsonResponse({"message": "Race deleted successfully"})
        except Race.DoesNotExist:
            raise Http404("Race not found")

@method_decorator(csrf_exempt, name='dispatch')
class RaceCreateView(View):
    # POST: Adds a new racehorse
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        form = RaceForm(data)
        if form.is_valid():
            race = form.save()
            return JsonResponse(model_to_dict(race), status=201)
        else:
            return JsonResponse(form.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ParticipationListView(View):
    # GET: List of participations
    def get(self, request):
        participations = Participation.objects.all()
        return JsonResponse({"participations": [model_to_dict(participation) for participation in participations]})

@method_decorator(csrf_exempt, name='dispatch')
class ParticipationDetailView(View):
    # GET: Detail of a participation
    def get(self, request, pk):
        try:
            participation = Participation.objects.get(pk=pk)
            return JsonResponse(model_to_dict(participation))
        except Participation.DoesNotExist:
            raise Http404("Participation not found")
    
    @csrf_exempt
    # POST: Updates participation info
    def post(self, request, pk):
        try:
            participation = Participation.objects.get(pk=pk)
            data = json.loads(request.body)
            form = ParticipationForm(data, instance=participation)
            if form.is_valid():
                form.save()
                return JsonResponse(model_to_dict(participation))
            else:
                return JsonResponse(form.errors, status=400)
        except Participation.DoesNotExist:
            raise Http404("Participation not found")
    # DELETE: Delete participation
    @csrf_exempt
    def delete(self, request, pk):
        try:
            participation = Participation.objects.get(pk=pk)
            participation.delete()
            return JsonResponse({"message": "Participation deleted successfully"})
        except Participation.DoesNotExist:
            raise Http404("Participation not found")

@method_decorator(csrf_exempt, name='dispatch')
class ParticipationCreateView(View):
    # POST: Add a new participation
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        form = ParticipationForm(data)
        if form.is_valid():
            participation = form.save()
            return JsonResponse(model_to_dict(participation), status=201)
        else:
            return JsonResponse(form.errors, status=400)



# def index(request):
#     return render(request, 'horses/index.html')

# def jockey_list(request):
#     jockeys = Jockey.objects.all()
#     return render(request, 'horses/jockey_list.html', {'jockeys': jockeys})

# def racehorse_list(request):
#     racehorses = Racehorse.objects.all()
#     return render(request, 'horses/racehorse_list.html', {'racehorses': racehorses})

# def race_list(request):
#     races = Race.objects.all()
#     return render(request, 'horses/race_list.html', {'races': races})

# def participation_list(request):
#     participations = Participation.objects.all()
#     return render(request, 'horses/participation_list.html', {'participations': participations})

# def jockey_detail(request, id):
#     jockey = Jockey.objects.get(id=id)
#     return render(request, 'horses/jockey_detail.html', {'jockey': jockey})

# def racehorse_detail(request, id):
#     racehorse = Racehorse.objects.get(id=id)
#     return render(request, 'horses/racehorse_detail.html', {'racehorse': racehorse})

# def race_detail(request, id):
#     race = Race.objects.get(id=id)
#     return render(request, 'horses/race_detail.html', {'race': race})

# def participation_detail(request, id):
#     participation = Participation.objects.get(id=id)
#     return render(request, 'horses/participation_detail.html', {'participation': participation})

# def jockey_add(request):
#     if request.method == 'POST':
#         form = JockeyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('jockey_list')
#     else:
#         form = JockeyForm()
#     return render(request, 'horses/jockey_form.html', {'form': form})

# def racehorse_add(request):
#     if request.method == 'POST':
#         form = RacehorseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('racehorse_list')
#     else:
#         form = RacehorseForm()
#     return render(request, 'horses/racehorse_form.html', {'form': form})

# def race_add(request):
#     if request.method == 'POST':
#         form = RaceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('race_list')
#     else:
#         form = RaceForm()
#     return render(request, 'horses/race_form.html', {'form': form})

# def participation_add(request):
#     if request.method == 'POST':
#         form = ParticipationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('participation_list')
#     else:
#         form = ParticipationForm()
#     return render(request, 'horses/participation_form.html', {'form': form})

# def jockey_edit(request, id):
#     jockey = Jockey.objects.get(id=id)
#     if request.method == 'POST':
#         form = JockeyForm(request.POST, instance=jockey)
#         if form.is_valid():
#             form.save()
#             return redirect('jockey_detail', id=id)
#     else:
#         form = JockeyForm(instance=jockey)
#     return render(request, 'horses/jockey_form.html', {'form': form})

# def racehorse_edit(request, id):
#     racehorse = Racehorse.objects.get(id=id)
#     if request.method == 'POST':
#         form = RacehorseForm(request.POST, instance=racehorse)
#         if form.is_valid():
#             form.save()
#             return redirect('racehorse_detail', id=id)
#     else:
#         form = RacehorseForm(instance=racehorse)
#     return render(request, 'horses/racehorse_form.html', {'form': form})

# def race_edit(request, id):
#     race = Race.objects.get(id=id)
#     if request.method == 'POST':
#         form = RaceForm(request.POST, instance=race)
#         if form.is_valid():
#             form.save()
#             return redirect('race_detail', id=id)
#     else:
#         form = RaceForm(instance=race)
#     return render(request, 'horses/race_form.html', {'form': form})

# def participation_edit(request, id):
#     participation = Participation.objects.get(id=id)
#     if request.method == 'POST':
#         form = ParticipationForm(request.POST, instance=participation)
#         if form.is_valid():
#             form.save()
#             return redirect('participation_detail', id=id)
#     else:
#         form = ParticipationForm(instance=participation)
#     return render(request, 'horses/participation_form.html', {'form': form})

# def jockey_delete(request, id):
#     jockey = Jockey.objects.get(id=id)
#     if request.method == 'POST':
#         jockey.delete()
#         return redirect('jockey_list')
#     return render(request, 'horses/jockey_confirm_delete.html', {'jockey': jockey})

# def racehorse_delete(request, id):
#     racehorse = Racehorse.objects.get(id=id)
#     if request.method == 'POST':
#         racehorse.delete()
#         return redirect('racehorse_list')
#     return render(request, 'horses/racehorse_confirm_delete.html', {'racehorse': racehorse})

# def race_delete(request, id):
#     race = Race.objects.get(id=id)
#     if request.method == 'POST':
#         race.delete()
#         return redirect('race_list')
#     return render(request, 'horses/race_confirm_delete.html', {'race': race})

# def participation_delete(request, id):
#     participation = Participation.objects.get(id=id)
#     if request.method == 'POST':
#         participation.delete()
#         return redirect('participation_list')
#     return render(request, 'horses/participation_confirm_delete.html', {'participation': participation})


# Create your views here.
