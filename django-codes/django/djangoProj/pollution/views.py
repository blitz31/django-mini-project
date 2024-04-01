import requests
from django.shortcuts import render
from .forms import CityForm
from .forms import AQIForm

def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            country_code = form.cleaned_data['country_code']

            api_url = f'https://api.openaq.org/v1/latest?country={country_code}'
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    measurements = get_measurements_by_city(data, city)
                    if measurements:
                        pm25_value = get_parameter_value(measurements, 'pm25')
                        aqi_class = get_aqi_class(pm25_value)
                        aqi_description = get_aqi_description(pm25_value)
                        return render(request, 'home.html', {'city': city, 'pm25_value': pm25_value, 'aqi_class': aqi_class, 'aqi_description': aqi_description})
                    else:
                        error_message = f"No air quality data available for {city}. Please try another city."
                else:
                    error_message = f"Failed to fetch air quality data for {country_code}. Please try again later."
                    return render(request, 'base.html', {'form': form, 'error_message': error_message})
            except requests.RequestException as e:
                error_message = f"Error occurred while fetching data: {str(e)}"
                return render(request, 'base.html', {'form': form, 'error_message': error_message})
                
            return render(request, 'base.html', {'form': form, 'error_message': error_message})
    else:
        form = CityForm()
        return render(request, 'base.html', {'form': form})
    
def get_measurements_by_city(data, city):
    for result in data.get('results', []):
        if result.get('location') == city:
            return result.get('measurements', [])
    return []

def get_parameter_value(measurements, parameter):
    try:
        for measurement in measurements:
            if 'parameter' in measurement and measurement['parameter'] == parameter and 'value' in measurement:
                return measurement['value']
    except (KeyError, TypeError):
        pass  # Handle missing or invalid data gracefully
    return None

def get_aqi_class(pm25_value):
    if pm25_value is None:
        return ''
    elif pm25_value <= 12.0:
        return 'good'
    elif pm25_value <= 35.4:
        return 'moderate'
    elif pm25_value <= 55.4:
        return 'unhealthy'
    elif pm25_value <= 150.4:
        return 'very-unhealthy'
    else:
        return 'hazardous'

def get_aqi_description(pm25_value):
    if pm25_value is None:
        return 'No data available'
    elif pm25_value <= 12.0:
        return 'Good'
    elif pm25_value <= 35.4:
        return 'Moderate'
    elif pm25_value <= 55.4:
        return 'Unhealthy for Sensitive Groups'
    elif pm25_value <= 150.4:
        return 'Unhealthy'
    else:
        return 'Hazardous'

    
def calculate_aqi(self, request):
        if request.method == 'POST':
            form = AQIForm(request.POST)
            if form.is_valid():
                pm10_value = form.cleaned_data['pm10']
                pm25_value = form.cleaned_data['pm25']
                
                # Calculate AQI and interpret quality using JavaScript functions
                
                return render(request, 'base.html', {'pm10_value': pm10_value, 'pm25_value': pm25_value})
        else:
            form = AQIForm()
        return render(request, 'base.html', {'form': form})