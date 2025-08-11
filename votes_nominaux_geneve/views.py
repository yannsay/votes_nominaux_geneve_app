from django.shortcuts import render
from .models import RSGETaxonomieData, RSGEVotingsData, personsData, votesData
from django_pandas.io import read_frame
from .src.services import filter_rsge_voting, filter_persons, create_persons_votes, create_table_to_plot
# Create your views here.
import numpy as np

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

def create_votes_table(request):

    rsge_votings_query = RSGEVotingsData.objects.all()
    rsge_votings_data = read_frame(rsge_votings_query)

    if request.method == "GET":
        # Retrieve parameters from the request
        param1 = request.GET.get('param1')
        param2 = request.GET.get('param2')
        param2 = [] if param2 is None else [param2]
    
    # if param1 == None:
    #     return render(request, "/")


    # filter voting
    votings_table = filter_rsge_voting(voting_table=rsge_votings_data, 
                            selected_rubriques=[param1], 
                            selected_chapitre=param2)


    # filter persons
    persons_query = personsData.objects.all()
    persons_data = read_frame(persons_query)
    persons_table = filter_persons(persons_data, [],[],[])

    # create persons_votes table
    votes_query = votesData.objects.all()
    votes_data = read_frame(votes_query)

    persons_votes_table = create_persons_votes(votes_data, persons_table)

    # Creat table to plot   
    table_to_plot = create_table_to_plot(voting_table=votings_table, persons_votes_table=persons_votes_table)
    table_to_plot = table_to_plot.replace(np.nan, "")
    # Print the table
    table_as_dict = table_to_plot.to_dict(orient="tight",index = False)
    return render(request, "table-votes.html", {"table_as_dict":table_as_dict})
    
