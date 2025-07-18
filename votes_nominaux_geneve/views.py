from django.shortcuts import render, HttpResponse
from .models import RSGEChapter
from django_pandas.io import read_frame

# Create your views here.

def index(request):
    return render(request, "index.html")

def selection_rgse(request):
    rsge_query = RSGEChapter.objects.all()
    rsge_all = read_frame(rsge_query)
    rsge_shorter =rsge_all[["intitule_rubrique","intitule_chapitre"]].drop_duplicates()
    rsge_dict = {}
    for rubrique in rsge_shorter["intitule_rubrique"].unique():
        rsge_dict[rubrique] = rsge_shorter[rsge_shorter["intitule_rubrique"] == rubrique]["intitule_chapitre"].tolist()

    return render(request, "selection-rgse.html", {'rsge_dict':rsge_dict})

def create_votes_table(request):
    if request.method == "GET":
        # Retrieve parameters from the request
        param1 = request.GET.get('param1')
        param2 = request.GET.get('param2')

        # Logic to handle the parameters
        return HttpResponse(f'Received params: param1={param1}, param2={param2}')
    return render(request, "table-votes.html")
