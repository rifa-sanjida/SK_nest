from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, ProviderProfile, LearnerProfile, PasswordRecoveryRequest
from services.models import Division, City, Area


PUBLIC_ROLE_CHOICES = [
    ('learner', 'Learner'),
    ('provider', 'Provider'),
]


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=PUBLIC_ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    division_obj = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        empty_label='Select Division',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    city_obj = forms.ModelChoiceField(
        queryset=City.objects.none(),
        empty_label='Select City',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    area_obj = forms.ModelChoiceField(
        queryset=Area.objects.none(),
        empty_label='Select Area',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'division_obj',
            'city_obj',
            'area_obj',
            'address',
            'password1',
            'password2',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        if 'division_obj' in self.data:
            try:
                division_id = int(self.data.get('division_obj'))
                self.fields['city_obj'].queryset = City.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['city_obj'].queryset = City.objects.none()

        if 'city_obj' in self.data:
            try:
                city_id = int(self.data.get('city_obj'))
                self.fields['area_obj'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['area_obj'].queryset = Area.objects.none()

    def save(self, commit=True):
        user = super().save(commit=False)

        division = self.cleaned_data.get('division_obj')
        city = self.cleaned_data.get('city_obj')
        area = self.cleaned_data.get('area_obj')

        user.role = self.cleaned_data['role']
        user.division = division.name if division else ''
        user.city = city.name if city else ''
        user.area = area.name if area else ''

        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ['certifications', 'skill_description', 'contact_info', 'visibility_status']
        widgets = {
            'certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skill_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'visibility_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LearnerProfileForm(forms.ModelForm):
    class Meta:
        model = LearnerProfile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class UserUpdateForm(forms.ModelForm):
    division_obj = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        empty_label='Select Division',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    city_obj = forms.ModelChoiceField(
        queryset=City.objects.none(),
        empty_label='Select City',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    area_obj = forms.ModelChoiceField(
        queryset=Area.objects.none(),
        empty_label='Select Area',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'division_obj',
            'city_obj',
            'area_obj',
            'address',
            'profile_picture',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            division = Division.objects.filter(name=self.instance.division).first()
            city = City.objects.filter(name=self.instance.city).first()
            area = Area.objects.filter(name=self.instance.area).first()

            if division:
                self.fields['division_obj'].initial = division
                self.fields['city_obj'].queryset = City.objects.filter(division=division).order_by('name')

            if city:
                self.fields['city_obj'].initial = city
                self.fields['area_obj'].queryset = Area.objects.filter(city=city).order_by('name')

            if area:
                self.fields['area_obj'].initial = area

        if 'division_obj' in self.data:
            try:
                division_id = int(self.data.get('division_obj'))
                self.fields['city_obj'].queryset = City.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['city_obj'].queryset = City.objects.none()

        if 'city_obj' in self.data:
            try:
                city_id = int(self.data.get('city_obj'))
                self.fields['area_obj'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['area_obj'].queryset = Area.objects.none()

    def save(self, commit=True):
        user = super().save(commit=False)

        division = self.cleaned_data.get('division_obj')
        city = self.cleaned_data.get('city_obj')
        area = self.cleaned_data.get('area_obj')

        user.division = division.name if division else ''
        user.city = city.name if city else ''
        user.area = area.name if area else ''

        if commit:
            user.save()
        return user


class PasswordRecoveryRequestForm(forms.ModelForm):
    class Meta:
        model = PasswordRecoveryRequest
        fields = []