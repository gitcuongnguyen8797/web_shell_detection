from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .machine_learning.extract import *
from config import *
from .machine_learning.classifiers.random_forest import RandomForest
from django.shortcuts import render
from django import forms
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
    filename = fs.save(folder + file.name, file)
    uploaded_file_url = fs.url(filename)
    extractor = ExtractFeatures(ROOT_DIR + uploaded_file_url)
    model = RandomForest('./dataset/Q_dataset_ps_loctu_tfidf_200.csv')
    prediction_without_pca = model.predict_without_pca(extractor.extract_function_names())
    
    return JsonResponse(
        {
            "message": "Successfully",
            'class_without_pca': ",".join(prediction_without_pca),
            "entropy": extractor.extract_entropy_file(),
            "longest_string": extractor.extract_longest_string(),
            'function_names': extractor.extract_function_names()
        }
    )

def check_file(request):
    upload_form = Form()
    return render(request, "result.html", { 'form': upload_form})

def check_file_upload(request):
    file = request.FILES['file']
    fs = FileSystemStorage()
    folder = "./storages/"
    filename = fs.save(folder + file.name, file)
    uploaded_file_url = fs.url(filename)
    extractor = ExtractFeatures(ROOT_DIR + uploaded_file_url)
    model = RandomForest('./dataset/Q_dataset_ps_loctu_tfidf_200.csv')
    prediction_without_pca = model.predict_without_pca(extractor.extract_function_names())

    return render(request, "result.html", {
        "message": "Successfully",
        'class_without_pca': ",".join(prediction_without_pca),
        "entropy": extractor.extract_entropy_file(),
        "longest_string": extractor.extract_longest_string(),
        'function_names': extractor.extract_function_names()
    })