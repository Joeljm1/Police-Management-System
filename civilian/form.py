from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CivilianModel
from police.models import Crime


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(
        required=True, help_text="Enter in format YYYY-MM-DD"
    )
    city = forms.CharField(max_length=50, required=True)
    street = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=50, required=True)

    usable_password = None

    # def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.fields['password1'].help_text = 'give password'
    # do this if want to change help test in registration

    class Meta(
        UserCreationForm.Meta
    ):  #  changes it to subclass check if problems occur later
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'name', 'date_of_birth', 'city', 'street', 'state']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "Civilian"
        if commit:
            user.save()
            civilian_model = CivilianModel(
                name=self.cleaned_data["name"],
                date_of_birth=self.cleaned_data["date_of_birth"],
                city=self.cleaned_data["city"],
                street=self.cleaned_data["street"],
                state=self.cleaned_data["state"],
                user=user,
            )
            civilian_model.save()

        return user


class addCrime(forms.ModelForm):
    class Meta:
        model = Crime
        fields = ["crime_type", "description", "location", "station"]
        widgets = {
            'description': forms.Textarea(attrs={'rows':6, 'cols':35}),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        crime_report = super().save(commit=False)
        crime_report.submitted_by = CivilianModel.objects.get(user=self.request.user)
        crime_report.status = "Request Pending"  # added extra
        if commit:
            crime_report.save()

        return crime_report

