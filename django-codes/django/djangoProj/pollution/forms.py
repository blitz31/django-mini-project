from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label="Name", max_length=200)
    country_code = forms.CharField(label='Country Code', max_length=2)


class AQIForm(forms.Form):
    pm10 = forms.FloatField(label="Enter the PM10 value")
    pm25 = forms.FloatField(label="Enter the PM2.5 value")
