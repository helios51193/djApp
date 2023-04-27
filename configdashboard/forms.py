from django import forms

class GenderForm(forms.Form):
    gender = forms.CharField(max_length=20,
                             widget=forms.TextInput(attrs={"placeholder": "Add Gender","class":"form-control"}))

class NetworkForm(forms.Form):
    def __init__(self, networks,network_display,selectedNetworks, *args, **kwargs):
        super(NetworkForm, self).__init__(*args, **kwargs)

        choices = list(zip(networks,network_display))
        choices.insert(0,("None","Select Network"))
        filtered_choices = filter(lambda x:x[0] not in selectedNetworks,choices)
        self.fields['networks'] = forms.ChoiceField(choices=filtered_choices,initial=choices[0],widget=forms.Select(attrs={'class': 'form-select'}))

class ModuleForm(forms.Form):
    def __init__(self,modules,selectedModules, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)

        choices = list(zip(modules,modules))
        choices.insert(0,("None","Select Network"))
        filtered_choices = filter(lambda x:x[0] not in selectedModules ,choices)
        self.fields['modules'] = forms.ChoiceField(choices=filtered_choices,initial=choices[0],widget=forms.Select(attrs={'class': 'form-select'}))
    