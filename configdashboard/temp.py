def report_json(request, pk):
    study = Study.objects.get(id=pk)
    package = study.package
    client = study.client
    # print('Inside the request for report json for id:', str(pk))
    logmsg = 'Sending the report json for id '+ str(pk)
    logger.info(logmsg)
    # obj = HistoryTableStudy(timestamp = datetime.datetime.now(), module = 'study.views.report_json', message = logmsg)
    # obj.save()
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
            return render(request, 'partials/report_config.html', context)
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
        client_name = study.client.client_name or 'Organisation Full Name'
        try:
            display_name = study.client.display_name or 'Display Name'
        except:
            display_name = 'Display Name'
        try:
            team_name = config['settings']['team_name']
        except:
            team_name = 'Team Name'

            print("GET")  
        
        # written
        genders = config['settings']['gender_keys'] 
        networks = list(zip(config['settings']['networks'],config['settings']['networks_display']))
        modules = config['settings']['modules']
        who_modules = config['settings']['who_modules'] 

        context = {'study_id': pk, 'asc': asc, 'dsc': dsc, 'hl_count': hl_count, 
            'tenure_text': tenure_text, 'tenure_date': tenure_date, 'msg': msg, 
            'org_name': client_name, 'ext_gen': extended_gender,
            'display_name': display_name, 'team_name': team_name, 'team_ONA': True,'table_exist':table_exist,
            'entity_dict':entity_dict,'entity_json':entity_json,"myObj":myObj_json,"myObject":myObj, "genders":genders,
            'networks':networks, 'modules':modules,'who_modules':who_modules}
        # print(context)
        # print('Now rendering')
        
        
        return render(request, 'partials/report_config.html', context)

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
        config['parent_entity_class_child'] =create_parent_entity(config['entity_class'])
        config['entity_class_child'] = create_entity_class(config['entity_class'])
        
        # Written by Pranjal 
        config['settings']['gender_keys'] = genders
        config['settings']['networks'] = [] 
        config['settings']['networks_display'] = [] 
        config['settings']['modules'] = []
        config['settings']['who_modules'] = []

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

        if extended_gender:
            print('saving the extended gender')
            config['settings']['extended_gender_calcs'] = True
            config['settings']['gender_keys'] = ['Male', 'Female', 'Intersex', 'Not-disclosed']
            extended_gender = 'checked'
        else:
            config['settings']['extended_gender_calcs'] = False
            config['settings']['gender_keys'] = ['Male', 'Female']
            extended_gender = ''


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



        context = {'study_id': pk, 'asc': asc, 'dsc': dsc, 'hl_count': hl_count,
            'tenure_text': tenure_text, 'tenure_date': tenure_date, 'team_ONA': True, 
            'org_name': client_name, 'display_name': display_name, 'team_name': team_name,
            'ext_gen': extended_gender, 'submitted': submitted, 'saved': saved,'table_exist':table_exist,
            'entity_dict':entity_dict,'entity_json':entity_json,"myObj":myObj_json,"myObject":myObj}
        msg = "Report rendered"
        

        tempid = None
        if(request.user.companys_type == 'Client'):
            tempid = request.user.company_id

        # hst.add(userid = request.user.id, event_type= 'REPORT_SAVED', event = msg, studyid = pk, clientid = tempid)

        logger.info("Report rendered")
        return render(request, 'partials/oldreport_config.html', context)    
