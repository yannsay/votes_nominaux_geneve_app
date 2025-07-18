from django.shortcuts import render
from .models import RSGETaxonomieData, RSGEVotingsData, personsData, votesData
from django_pandas.io import read_frame
from .src.services import filter_rsge_voting
from great_tables import GT
# Create your views here.

def index(request):
    return render(request, "index.html")

def selection_rgse(request):
    rsge_query = RSGETaxonomieData.objects.all()
    rsge_data = read_frame(rsge_query)
    rsge_shorter =rsge_data[["intitule_rubrique","intitule_chapitre"]].drop_duplicates()
    rsge_dict = {}
    for rubrique in rsge_shorter["intitule_rubrique"].unique():
        rsge_dict[rubrique] = rsge_shorter[rsge_shorter["intitule_rubrique"] == rubrique]["intitule_chapitre"].tolist()

    return render(request, "selection-rgse.html", {'rsge_dict':rsge_dict})

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

    print(type(param1))
    print(param2)

    # filter voting
    filtered_votings_data = filter_rsge_voting(voting_table=rsge_votings_data, 
                            selected_rubriques=[param1], 
                            selected_chapitre=param2)

    print(filtered_votings_data.shape)
    # filter votes
    filtered_votes = None
    # join

    #print
    gt_tbl = GT(filtered_votings_data)
    gt_tbl_html = gt_tbl.as_raw_html()
    return render(request, "table-votes.html", {"gt_tbl_html":gt_tbl_html})
    
