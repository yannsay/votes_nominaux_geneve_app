from django.shortcuts import render
from django_pandas.io import read_frame
from django.http import HttpResponse
from io import StringIO

from .models import RSGETaxonomieData, RSGEVotingsData, personsData, votesData
from .src.services import create_votes_table
# Create your views here.

def index(request):
    return render(request, "index.html")
def about(request):
    return render(request, "about.html")
def selection_rsge(request):
    rsge_query = RSGETaxonomieData.objects.all()
    rsge_data = read_frame(rsge_query)
    rsge_shorter =rsge_data[["intitule_rubrique","intitule_chapitre"]].drop_duplicates()
    rsge_dict = {}
    for rubrique in rsge_shorter["intitule_rubrique"].unique():
        rsge_dict[rubrique] = rsge_shorter[rsge_shorter["intitule_rubrique"] == rubrique]["intitule_chapitre"].tolist()

    return render(request, "selection-rsge.html", {'rsge_dict':rsge_dict})

def plot_votes_table(request):
    # Retrieve parameters from the request
    if request.method == "GET":
        param1 = request.GET.get('param1')
        param2 = request.GET.get('param2')
        param2 = [] if param2 is None else [param2]
    
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
    table_to_plot = create_votes_table(registre=[param1], 
                                       chapitre=param2,
                                       rsge_votings_data=rsge_votings_data,
                                       persons_data=persons_data,
                                       votes_data=votes_data)
    if request.GET.get('download'):
        # Create a response with the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="votes_table.csv"'
        table_to_plot.to_csv(path_or_buf=response, index=False)
        return response
    
    # Print the table
    table_as_dict = table_to_plot.to_dict(orient="tight",index = False)
    return render(request, "table-votes.html", {"table_as_dict":table_as_dict,
                                                "rubrique":param1,
                                                "chapitres":param2})
