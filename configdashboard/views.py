from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import GenderForm, NetworkForm, ModuleForm
from configdashboard.commons.utils import dashboardUtils

# Create your views here.
def configDashboard(request):

    static_data = dashboardUtils.static_data()
    
    try:
        with open("configdashboard/jsons/config.json", "r") as f:
            json_data = json.load(f)    
    except IOError as e:
            return render(request, "configdash/index.html", { "message":"Failed to load configuration"})
    

    # Forms
    genderForm = GenderForm()
    networkForm = NetworkForm(static_data['networks'],static_data['networks_display'],json_data['settings']['networks'])
    moduleForm = ModuleForm(static_data['modules'],json_data['modules'])
    context = {
        "config":json_data,
        "static_data":static_data,
        "genderForm":genderForm,
        "networkForm":networkForm,
        "moduleForm":moduleForm
        }
    
    if request.method == "GET":
        return render(request,"configdash/index.html", context)

def add_gender(request):
     
    if request.method == "POST":
        try:
            with open("configdashboard/jsons/config.json", "r") as f:
                json_data = json.load(f)    
        except IOError as e:
                return render(request, "configdash/index.html", { "message":"Failed to load configuration"})
        
        genderForm = GenderForm(request.POST)
        if genderForm.is_valid():
            gender = genderForm.cleaned_data["gender"]

            temp = [gen.lower() for gen in json_data['settings']['gender_keys']]

            if gender.lower() not in temp:
                json_data['settings']['gender_keys'].append(gender)
        try:
            with open("configdashboard/jsons/config.json", "w") as f:
                json_object = json.dumps(json_data)
                f.write(json_object)
        except IOError as e:
            print("Failed to write json", e)

    return redirect("/configdashboard")

def remove_gender(request, gender):
     
    if request.method == "POST":

        try:
            with open("configdashboard/jsons/config.json", "r") as f:
                json_data = json.load(f)    
        except IOError as e:
                return render(request, "configdash/index.html", { "message":"Failed to load configuration"})
        
        json_data['settings']['gender_keys'].remove(gender)

        try:
            with open("configdashboard/jsons/config.json", "w") as f:
                json_object = json.dumps(json_data)
                f.write(json_object)
        except IOError as e:
            print("Failed to write json", e)

    return redirect("/configdashboard")

def toggle_modules(request,module,name):

    try:
        with open("configdashboard/jsons/config.json", "r") as f:
            json_data = json.load(f)    
    except IOError as e:
            return JsonResponse({"status":-1, "message":"Failed to load settings"})

    if module == "who":
        module_type = "who_modules"
    
    module = list(filter(lambda x : x['name'] == name, json_data["settings"][module_type]))

    if len(module_type) > 0:
        if module[0]['enabled'] == 1:
            module[0]['enabled'] = 0
        else:
            module[0]['enabled'] = 1
    
    try:
        with open("configdashboard/jsons/config.json", "w") as f:
            json_object = json.dumps(json_data)
            f.write(json_object)
    except IOError as e:
        JsonResponse({"status":-1, "message":"Failed to update settings"})

    return JsonResponse({"status":0, "message":"Updated Successfully", "value":module[0]['enabled'] })

def remove_network(request,network):

    if request.method == "POST":
        
        try:
            with open("configdashboard/jsons/config.json", "r") as f:
                json_data = json.load(f)    
        except IOError as e:
            return render(request, "configdash/index.html", { "message":"Failed to load configuration"})
        
        networks = json_data['settings']['networks']

        networkIndex = networks.index(network)
        json_data['settings']['networks'].pop(networkIndex)
        json_data['settings']['networks_display'].pop(networkIndex)

        try:
            with open("configdashboard/jsons/config.json", "w") as f:
                json_object = json.dumps(json_data)
                f.write(json_object)
        except IOError as e:
            print("Failed to write json", e)

    return redirect("/configdashboard") 
        

def add_network(request):

    if request.method == "POST":
        try:
            with open("configdashboard/jsons/config.json", "r") as f:
                json_data = json.load(f)    
        except IOError as e:
            return render(request, "configdash/index.html", { "message":"Failed to load configuration"})
        
        static_data = dashboardUtils.static_data()
        
        networkForm = NetworkForm(static_data['networks'],static_data['networks_display'],json_data['settings']['networks'],request.POST)

        if networkForm.is_valid():
            network_value = networkForm.cleaned_data['networks']
            try:
                networkIndex = static_data["networks"].index(network_value)
                json_data['settings']['networks'].append(static_data['networks'][networkIndex])
                json_data['settings']['networks_display'].append(static_data['networks_display'][networkIndex])
            except ValueError as ve:
                print(ve)
        
        try:
            with open("configdashboard/jsons/config.json", "w") as f:
                json_object = json.dumps(json_data)
                f.write(json_object)
        except IOError as e:
            print("Failed to write json", e)
    return redirect("/configdashboard") 

def add_module(request):

    if request.method == "POST":
        try:
            with open("configdashboard/jsons/config.json", "r") as f:
                json_data = json.load(f)    
        except IOError as e:
            return render(request, "configdash/index.html", { "message":"Failed to load configuration"})

        static_data = dashboardUtils.static_data()
        moduleForm = ModuleForm(static_data["modules"],json_data["modules"],request.POST)

        if moduleForm.is_valid():
            if moduleForm.cleaned_data["modules"] != "None":
                json_data["modules"].append(moduleForm.cleaned_data["modules"])
        
        try:
            with open("configdashboard/jsons/config.json", "w") as f:
                json_object = json.dumps(json_data)
                f.write(json_object)
        except IOError as e:
            print("Failed to write json", e)
    
    return redirect("/configdashboard") 
    

def remove_module(request, module):
    
    if request.method == "POST":
        try:
            with open("configdashboard/jsons/config.json", "r") as f:
                json_data = json.load(f)    
        except IOError as e:
            return render(request, "configdash/index.html", { "message":"Failed to load configuration"})

        
        json_data["modules"].remove(module)

        try:
            with open("configdashboard/jsons/config.json", "w") as f:
                json_object = json.dumps(json_data)
                f.write(json_object)
        except IOError as e:
            print("Failed to write json", e)
        
    return redirect("/configdashboard") 

        
          