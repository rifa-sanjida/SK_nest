from django import forms
from .models import Service, ProviderAvailability, BlockedDate, Division, City, Area


class ServiceForm(forms.ModelForm):
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
        model = Service
        fields = [
            'category',
            'title',
            'description',
            'price',
            'duration_minutes',
            'division_obj',
            'city_obj',
            'area_obj',
            'address',
            'image',
            'is_active',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
        service = super().save(commit=False)

        division = self.cleaned_data.get('division_obj')
        city = self.cleaned_data.get('city_obj')
        area = self.cleaned_data.get('area_obj')

        service.division = division.name if division else ''
        service.city = city.name if city else ''
        service.area = area.name if area else ''

        if commit:
            service.save()
        return service


class ProviderAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ProviderAvailability
        fields = ['day_of_week', 'start_time', 'end_time']
        widgets = {
            'day_of_week': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }


class BlockedDateForm(forms.ModelForm):
    class Meta:
        model = BlockedDate
        fields = ['blocked_date', 'reason']
        widgets = {
            'blocked_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }