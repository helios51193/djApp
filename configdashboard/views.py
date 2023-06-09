from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import GenderForm, NetworkForm, ModuleForm
from configdashboard.commons.utils import dashboardUtils
import logging as logger
import re
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

def read_report_json(s):
    try:
        with open("configdashboard/jsons/config.json", "r") as f:
            json_data = json.load(f) 
            print(json_data)   
            return json_data
    except IOError as e:
        return {}
def update_report_json(pk,config):
    try:
        with open("configdashboard/jsons/config.json", "w") as f:
                json_object = json.dumps(config)
                f.write(json_object)
                print("updated")
                return True
    except IOError as e:
            return False


def report_json(request):
    #study = Study.objects.get(id=pk)
    #package = study.package
    #client = study.client
    # print('Inside the request for report json for id:', str(pk))
    #logmsg = 'Sending the report json for id '+ str(pk)
    #logger.info(logmsg)
    # obj = HistoryTableStudy(timestamp = datetime.datetime.now(), module = 'study.views.report_json', message = logmsg)
    # obj.save()

    # written by pranjal
    config_folder= ""
    pk =""
    print("stating request checking")
    try:
        available_column_mapping_file_path = config_folder+"/study_"+str(pk)+"/available_column_mapping.json"
        f = open(available_column_mapping_file_path, "r")
        available_column_mapping = json.loads(f.read())
        f.close()
        myObj = available_column_mapping
        myObj.pop("first_name")
        myObj.pop("last_name")
        myObj.pop("email")
        myObj.pop("gender")
        myObj.pop("designation")
        myObj.pop("joining_date")
        myObj.pop("reporting_manager")
        myObj_json = json.dumps(myObj)

        
    except Exception as e:
        myObj = {"department":"Department/Function", "legal_entity":"Legal Entity/Business Unit", "hierarchy_level":"Hierarchy Level",
                        "location":"Location","group_name1":"Custom Field 1","group_name2":"Custom Field 2",
                        "group_name3":"Custom Field 3","group_name4":"Custom Field 4","group_name5":"Custom Field 5"}
        myObj_json = json.dumps(myObj)          


        print(e)
    
    
    if request.method=='GET':
        entity_dict = {}
        table_exist = 100
        entity_json = ""
        try:
            config = read_report_json(pk) #, package)
            msg = 'safe'
        except Exception as e:
            msg = str(e)
            # print('Error during reading report json:', e)
            context = {'study_id': pk, 'asc': '', 'dsc': '', 'hl_count': 'NA',
                'tenure_text': 'NA', 'tenure_date': 'NA', 'org_name': 'NA',
                'display_name': 'NA', 'team_name': 'NA', 'team_ONA': False, 'msg': msg}
            # print('Now rendering')
            #return render(request, 'partials/report_config.html', context)
            return render(request, '')
        try:            
            
            entity_class = config['entity_class'] or []
            if 'organisation' in entity_class:
                entity_class.remove('organisation')
            entity_class_disp = config['entity_class_disp'] or []
            if 'Organisation' in entity_class_disp:
                entity_class_disp.remove('Organisation') 
            entity_class_short_disp = config['entity_class_short_disp'] or []
            if 'Org' in entity_class_short_disp:
                entity_class_short_disp.remove('Org')

            # myObj = {"department":"Department/Function", "legal_entity":"Legal Entity/Business Unit", "hierarchy_level":"Hierarchy Level",
            #             "location":"Location","group_name1":"Custom Field 1","group_name2":"Custom Field 2",
            #             "group_name3":"Custom Field 3","group_name4":"Custom Field 4","group_name5":"Custom Field 5"}

        # Pankaj added this upto 'end' to convert extra columns acc to corresponding col name in sheet
            # Check for extra cols json in the study folder
            
        # end
            print(len(entity_class))
            
            if entity_class[0] == '':
                print("AA")
                table_exist = 0
                entity_dict = {}
                entity_json = {}

            else:    
                table_exist = 1
                entity_dict = {myObj[entity_class[i]]:[entity_class_disp[i], entity_class_short_disp[i],entity_class[i]] for i in range(len(entity_class))} 
                entity_json = json.dumps(entity_dict)
        except Exception as e:
            print(e)        
        
        hl_order = config['settings']['hl_order']
        if hl_order == 'ASC':
            asc = 'checked'
            dsc = ''
        elif hl_order == 'DSC':
            asc = ''
            dsc = 'checked'
        else:
            asc = ''
            dsc = ''
        hl_count = config['settings']['hl_count']
        # print('hl count', hl_count)
        try:
            tenure_text = config['settings']['tenure_text']
        except:
            tenure_text = 'Two Years'
        try:
            extended_gender = config['settings']['extended_gender_calcs']

            if extended_gender:
                extended_gender = 'checked'
        except:
            extended_gender = ''

        # print('tenure text', tenure_text)
        tenure_date = config['settings']['tenurecalc_date']
        # print('tenure date', tenure_date)
        #client_name = study.client.client_name or 'Organisation Full Name'
        client_name = "Hello"
        try:
            display_name = study.client.display_name or 'Display Name'
        except:
            display_name = 'Display Name'
        try:
            team_name = config['settings']['team_name']
        except:
            team_name = 'Team Name'

            print("GET")  
        
        # written Pranjal
        genders = config['settings']['gender_keys'] 
        networks = list(zip(config['settings']['networks'],config['settings']['networks_display']))
        modules = config['modules']
        who_modules = config['settings']['who_modules'] 

        context = {'study_id': pk, 'asc': asc, 'dsc': dsc, 'hl_count': hl_count, 
            'tenure_text': tenure_text, 'tenure_date': tenure_date, 'msg': msg, 
            'org_name': client_name, 'ext_gen': extended_gender,
            'display_name': display_name, 'team_name': team_name, 'team_ONA': True,'table_exist':table_exist,
            'entity_dict':entity_dict,'entity_json':entity_json,"myObj":myObj_json,"myObject":myObj, "genders":genders,
            'networks':networks, 'modules':modules,'who_modules':who_modules}
        # print(context)
        # print('Now rendering')
        
        
        return render(request, "configdash/index.html", context)

    elif request.method=='POST':
        print("POST")
        try:
            print("POST")
            config = read_report_json(pk) #, package)
            # msg = 'safe'
        except Exception as e:
            # msg = str(e)
            # print(e)
            # write_report_json(pk, package, client)
            # print('Caught an exception.')
            client_comp = ClientCompany.objects.get(client_name = client)
            tenure_dt = str((date.today() - timedelta(days=int(2*365.2425))).strftime('%Y-%m-%d'))
            settings_dict = {"is_parent": True, "loglevel": "info", "is_generate_onps": False,
                "is_generate_observation": True, "is_generate_report": True, "remove_defaulters": False,
                "hl_order": "ASC", "hl_count": 3, "parent": "org", "parent_class": "Organisation"}
            settings_dict['product_name'] = str(package)
            settings_dict['org_name'] = str(client)
            settings_dict['URL'] = 'http://localhost/orglens/public/study_report/' + str(pk)
            tenure_dt = str((date.today() - timedelta(days=int(2*365.2425))).strftime('%Y-%m-%d'))
            settings_dict['tenurecalc_date'] = tenure_dt
            settings_dict['tenure_text'] = 'Two Years'
            settings_dict['team_name'] = 'Team Name'
            try:
                disp_name = client_comp.display_name
            except:
                disp_name = 'Display Name'
            settings_dict['display_name'] = str(disp_name)
            settings_dict['study_id'] = str(pk)

            # config['settings'] = settings_dict
            config = {'ver': '1.0', 'settings': settings_dict}
            print('Config Dict', config)
            
        print('In report json POST request')
        post_data = request.POST.items()
        form_data = dict()
        for keys, values in post_data:
            form_data[keys] = values
            print(keys, values)

        entity_values = form_data['entityvalues'].split(",")
        fields_array = form_data['fields'].split(",")
        display_name_table = form_data['display_name_table'].split(",") 
        short_display_name = form_data['short_display_name'].split(",")

        print(entity_values)
        print(display_name_table)
        print(short_display_name) 

        hl_order = form_data['hl_order']
        hl_count = form_data['leader_level']
        tenure_date = form_data['tenure_date']
        tenure_text = form_data['tenure_text']
        org_name = form_data['org_name']
        display_name = form_data['display_name']
        #table_data = form_data['table_data']
    
        #print(table_data,"Table Data")
        if 'extended_gender' in form_data:
            extended_gender = True
        else:
            extended_gender = False
        print('X gen', extended_gender)
        if 'team_name' in form_data:
            team_name = form_data['team_name']
        else:
            team_name = 'Team Name'

        print('converting to main json')

        config['settings']['hl_order'] = hl_order
        config['settings']['hl_count'] = hl_count
        config['settings']['tenurecalc_date'] = tenure_date
        config['settings']['tenure_text'] = tenure_text
        config['settings']['org_name'] = org_name
        config['settings']['display_name'] = display_name
        config['settings']['team_name'] = team_name
        config['settings']['study_id'] = pk
        config['entity_class'] = entity_values
        config['entity_class_disp'] =display_name_table
        config['entity_class_short_disp'] = short_display_name
        short_name = [x.replace(' ', '-').lower()  for x in short_display_name]
        config['entity_class_short'] = [re.sub('[^a-zA-Z0-9-]+', '', _) for _ in short_name]
        config['child_class'] = config['entity_class']
        config['child_class_short'] = config['entity_class_short']
        config['child_class_disp'] = config['entity_class_disp']
        config['child_class_short_disp'] = config['entity_class_short_disp']
        #config['parent_entity_class_child'] =create_parent_entity(config['entity_class'])
        #config['entity_class_child'] = create_entity_class(config['entity_class'])
        
        # Written by Pranjal 
        config['settings']['gender_keys'] = form_data['genders'].split(",")
        config['settings']['networks'] = form_data['networks'].split(",")
        config['settings']['networks_display'] = form_data['networks_display'].split(",")
        config['modules'] = form_data['modules'].split(",")


        print(config['settings']['gender_keys'])
        
        # it is in the form ["name","status","name","status".....]
        who_modules = form_data['who_modules'].split(",")
        who_modules_data = {
            "name": who_modules[0::2], 
            "status":who_modules[1::2]
        }
        for module,status in zip(who_modules_data['name'],who_modules_data['status']):
            module = list(filter(lambda x : x['name'] == module,config['settings']['who_modules']))
            module[0]['enabled'] = 1 if status == "1" else 0


        try:            
            entity_class = config['entity_class'] or []
            if 'organisation' in entity_class:
                entity_class.remove('organisation')
            entity_class_disp = config['entity_class_disp'] or []
            if 'Organisation' in entity_class_disp:
                entity_class_disp.remove('Organisation') 
            entity_class_short_disp = config['entity_class_short_disp'] or []
            if 'Org' in entity_class_short_disp:
                entity_class_short_disp.remove('Org')


            # myObj = {"department":"Department/Function", "legal_entity":"Legal Entity/Business Unit", "hierarchy_level":"Hierarchy Level",
            #             "location":"Location","group_name1":"Custom Field 1","group_name2":"Custom Field 2",
            #             "group_name3":"Custom Field 3","group_name4":"Custom Field 4","group_name5":"Custom Field 5"}

            print(len(entity_class))
            
            if entity_class[0] == '':
                print("AA")
                table_exist = 0    
                entity_dict = {}
                entity_json = {}
            else:    
                table_exist = 1
                entity_dict = {myObj[entity_class[i]]:[entity_class_disp[i], entity_class_short_disp[i],entity_values[i]] for i in range(len(entity_class))} 
                entity_json = json.dumps(entity_dict)
        except Exception as e:
            print(e)

        # commented by Pranjal
        # if extended_gender:
        #     print('saving the extended gender')
        #     config['settings']['extended_gender_calcs'] = True
        #     config['settings']['gender_keys'] = ['Male', 'Female', 'Intersex', 'Not-disclosed']
        #     extended_gender = 'checked'
        # else:
        #     config['settings']['extended_gender_calcs'] = False
        #     config['settings']['gender_keys'] = ['Male', 'Female']
        #     extended_gender = ''

        if update_report_json(pk, config):
            submitted = True
            saved = True
            msg = "Report saved for study id = " + str(pk)
            # obj = HistoryTableStudy(timestamp = datetime.datetime.now(), module = "study.views.report_json", message = msg)
            # obj.save()

            tempid = None
            if(request.user.companys_type == 'Client'):
                tempid = request.user.company_id

            hst.add(userid = request.user.id, event_type= 'REPORT_SAVED', event = msg, studyid = pk, clientid = tempid)

        else:
            submitted = True
            saved = False
            msg = "Report not saved for study id = " + str(pk)
            
            tempid = None
            if(request.user.companys_type == 'Client'):
                tempid = request.user.company_id

            hst.add(userid = request.user.id, event_type= 'REPORT_SAVED', event = msg, studyid = pk, clientid = tempid)

        asc = dsc = ''
        if hl_order == 'ASC':
            asc = 'checked'
            dsc = ''
        elif hl_order == 'DSC':
            asc = ''
            dsc = 'checked'
        client_name = org_name

        # written Pranjal
        genders = config['settings']['gender_keys'] 
        networks = list(zip(config['settings']['networks'],config['settings']['networks_display']))
        modules = config['modules']
        who_modules = config['settings']['who_modules'] 

        context = {'study_id': pk, 'asc': asc, 'dsc': dsc, 'hl_count': hl_count,
            'tenure_text': tenure_text, 'tenure_date': tenure_date, 'team_ONA': True, 
            'org_name': client_name, 'display_name': display_name, 'team_name': team_name,
            'ext_gen': extended_gender, 'submitted': submitted, 'saved': saved,'table_exist':table_exist,
            'entity_dict':entity_dict,'entity_json':entity_json,"myObj":myObj_json,"myObject":myObj,
            'genders':genders,'networks':networks,'modules':modules,'who_modules':who_modules}
        msg = "Report rendered"
        

        tempid = None
        if(request.user.companys_type == 'Client'):
            tempid = request.user.company_id

        # hst.add(userid = request.user.id, event_type= 'REPORT_SAVED', event = msg, studyid = pk, clientid = tempid)

        logger.info("Report rendered")
        return render(request, 'partials/oldreport_config.html', context)    
    
def helpConfig(request):
    return redirect("/configdashboard") 

def client_permissions(request):
    #print(f'Received {request.method} request for study id {pk}')

    if request.method == 'GET':
        try:
            with open("configdashboard/jsons/client_permissions.json", "r") as f:
                json_data = json.load(f)    
                return JsonResponse({'success': True, 'data': json_data})
        except IOError as e:
            pass
        
        # try:
        #     client_permissions_json = Study.objects.get(id=pk).client_permission
        #     # print(client_permissions_json['upload_data'])
        #     # print('Client Permissions:', client_permissions_json, type(client_permissions_json))
        #     return JsonResponse({'success': True, 'data': client_permissions_json})

        # except Exception as e:
        #     pass

        
          