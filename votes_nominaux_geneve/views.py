from django.shortcuts import render
from django_pandas.io import read_frame
from django.http import HttpResponse

from .models import RSGEData, RSGEVotingsData, personsData, votesData
from .src.services import create_votes_table, create_rsge_dict, create_parti_votes_table
# Create your views here.

def index(request):
    return render(request, "index.html")

def selection_rsge(request):
    rsge_query = RSGEData.objects.all()
    rsge_data = read_frame(rsge_query)
    rsge_dict = create_rsge_dict(rsge_data)

    return render(request, "selection-rsge.html", {'rsge_dict':rsge_dict})

def plot_votes_table(request):
    # Retrieve parameters from the request
    if request.method == "GET":
        registre = request.GET.get('registre')
        chapitre = request.GET.get('chapitre')
        chapitre = [] if chapitre is None else [chapitre]
    
    # Get votings
    rsge_votings_query = RSGEVotingsData.objects.all()
    rsge_votings_data = read_frame(rsge_votings_query)
    # Get persons
    persons_query = personsData.objects.all()
    persons_data = read_frame(persons_query)

    # Get votes
    votes_query = votesData.objects.all()
    votes_data = read_frame(votes_query)

    # Create table to plot
    table_to_plot = create_votes_table(registre=[registre], 
                                       chapitre=chapitre,
                                       rsge_votings_data=rsge_votings_data,
                                       persons_data=persons_data,
                                       votes_data=votes_data)
    
    parti_votes_table = create_parti_votes_table(table_to_plot)

    if request.GET.get('download'):
        # Create a response with the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="votes_table.csv"'
        table_to_plot.to_csv(path_or_buf=response, index=False)
        return response

    
    parti_votes_table_as_dict = parti_votes_table.to_dict(orient="tight",index = False)
    table_as_dict = table_to_plot.to_dict(orient="tight",index = False)

    return render(request, "table-votes.html", {"table_as_dict":table_as_dict,
                                                "rubrique":registre,
                                                "chapitres":chapitre,
                                                "parti_votes_table_as_dict":parti_votes_table_as_dict})
