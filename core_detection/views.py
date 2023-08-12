from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .machine_learning.extract import *
from config import *
from .machine_learning.classifiers.random_forest import RandomForest
from django.shortcuts import render
from django import forms
import pathlib
import json
import uuid

# Create your views here.

class Form(forms.Form):
    file = forms.FileField()

def healthy_check(request):
    return HttpResponse("This is a webshell detection api using machine learning")


@method_decorator(csrf_exempt)
def check_upload_file(request):
    file = request.FILES["file"]
    fs = FileSystemStorage()
    folder = "./storages/"
    file_name = uuid.uuid4().hex  
    filename = fs.save(folder + file_name, file)
    uploaded_file_url = fs.url(filename)
    extractor = ExtractFeatures(ROOT_DIR + uploaded_file_url)
    model_php = RandomForest('dataset/c_dataset_20.csv')
    model_asp = RandomForest('dataset/dataset_asp.csv')
    features = extractor.extract_function_names()
    features['longest'] = extractor.extract_longest_string()
    features['entropy'] = extractor.extract_entropy_file()
    ext = pathlib.Path(filename).suffix

    if (ext == 'asp' or ext == 'aspx'):   
        prediction = model_asp.predict_without_pca(features)
    else: 
        prediction = model_php.predict_without_pca(features)
    
    return JsonResponse(
        {
            "message": "Successfully",
            'class': ",".join(prediction),
            "entropy": extractor.extract_entropy_file(),
            "longest_string": extractor.extract_longest_string(),
            'function_names': extractor.extract_function_names()
        }
    )

def check_file(request):
    upload_form = Form()
    return render(request, "index.html", { 'form': upload_form})

def check_file_upload(request):
    file = request.FILES['file']
    fs = FileSystemStorage()
    folder = "./storages/"
    file_name = uuid.uuid4().hex
    filename = fs.save(folder + file_name, file)
    uploaded_file_url = fs.url(filename)
    extractor = ExtractFeatures(ROOT_DIR + uploaded_file_url)
    model_php = RandomForest('dataset/c_dataset_20.csv')
    model_asp = RandomForest('dataset/dataset_asp.csv')
    features = extractor.extract_function_names()
    features['longest'] = extractor.extract_longest_string()
    features['entropy'] = extractor.extract_entropy_file()
    ext = pathlib.Path(filename).suffix

    if (ext == 'asp' or ext == 'aspx'):   
        prediction = model_asp.predict_without_pca(features)
    else: 
        prediction = model_php.predict_without_pca(features)

    names = json.loads(json.dumps([{'name':key, 'value':value} for key,value in extractor.extract_function_names().items()], indent=2))
    
    return render(request, "result.html", {
            "message": "Successfully",
            'class': ",".join(prediction),
            "entropy": extractor.extract_entropy_file(),
            "longest_string": extractor.extract_longest_string(),
            'function_names': names[:5]
    })