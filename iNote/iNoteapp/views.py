from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from .models import conn
from bson import ObjectId


@csrf_exempt
def add_notes(request):
    if request.method == "POST":
        form_data = request.POST.dict()

        if form_data.get("important") == "on":
            form_data["important"] = True
        else:
            form_data["important"] = False

        note = conn.notes.notes.insert_one(dict(form_data))
        return render(request, "notes/result.html", {"message": "Added successfully!"})
    else:
        return render(request, "notes/index.html")


def get_notes(request):
    # client = MongoClient(settings.MONGODB_ATLAS_URI)
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        # print("doc:",doc)
        newDocs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
        })
    print(newDocs)
    return render(request, 'notes/getnotes.html', {'newDocs': newDocs})


def edit_note(request, id):
    print(" method called :" + str(id))
    docs = conn.notes.notes.find({})
    note = {}
    for doc in docs:
        if str(doc["_id"]) == id:
            # print(doc)
            note["id"] = doc["_id"]
            note["title"] = doc["title"]
            note["desc"] = doc["desc"]
            note["important"] = doc["important"]
    return render(request, 'notes/edit_notes.html', {"note": note})


@csrf_exempt
def update_note(request):
    if request.method == "POST":
        try:
            note_id = ObjectId(request.POST.get("noteId"))
            note_title = request.POST.get("noteTitle")
            note_desc = request.POST.get("noteDesc")
            # Update the note in MongoDB based on the converted noteId
            result = conn.notes.notes.update_one({"_id": note_id}, {"$set": {"title": note_title, "desc": note_desc}})

            if result.matched_count > 0:
                message = "Note updated successfully."
            else:
                message = "Note update failed."
        except Exception as e:
            message = f"Error: {str(e)}"

    return render(request, "notes/result.html", {"message": message})
