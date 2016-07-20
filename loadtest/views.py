# -*- coding: UTF-8 -*-
import json
import logging
import string

from django.http.response import HttpResponse
from django.shortcuts import render
import simplejson

from loadtest.models import LoadTestResult

logger = logging.getLogger(__name__)
logger.info("12345666666666666")

def about(request):
    return render(request, 'loadtest/about.html')

def show(request):
    # List = [{'color': '#FF0F00', 'Client': '7217', 'ResponseTime': '0-20'}, {'color': '#FF6600', 'Client': '288474', 'ResponseTime': '20-50'}, ];
    loadtest_results = LoadTestResult.objects.all();
    lastest_load_test_result = loadtest_results[0];
    index_results = _get_armcharts_column_list(lastest_load_test_result.test_result_index)
    bitrate_results = _get_armcharts_column_list(lastest_load_test_result.test_result_bitrate)
    test_errors = lastest_load_test_result.test_result_error
    print type(test_errors)
    
    return render(request, 'loadtest/loadtest_result.html', {
            'index_results': json.dumps(index_results), 'bitrate_results': json.dumps(bitrate_results),
            'test_errors': test_errors,
        })

def insert_test_result(request):
    logger.info("info")
    logger.error("error")
    logger.debug("debug")
    logger.warn("warn")
    '''
    dict = {}
    info = 'Data log save success'
    try:
        if request.method == 'POST':
            data = simplejson.loads(request.raw_post_data)
            # username = request['username']
            print data
            
    except Exception, e:
        logger.error('Failed to insert load test result', e)
 
    dict['message'] = info
    json = simplejson.dumps(dict)
    '''
    return HttpResponse("2000000")

def _get_armcharts_column_list(benchmark_result):
    convert_column_list = []
    for line in benchmark_result.split('\n'):
        if string.strip(line) == '':
            continue
        
        converted_dict = {}
        client_number = line.split(':')[1].replace('\r', '')
        
        if line.find('error') > 0:
            converted_dict['ResponseTime'] = '12000+'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#CD0D74'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('0    ~ 20   milliseconds') > 0:
            converted_dict['ResponseTime'] = '0-20'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FF0F00'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('20   ~ 50   milliseconds') > 0:
            converted_dict['ResponseTime'] = '20-50'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FF6600'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('50   ~ 200  milliseconds') > 0:
            converted_dict['ResponseTime'] = '50-200'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FF9E01'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('200  ~ 500  milliseconds') > 0:
            converted_dict['ResponseTime'] = '200-500'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FCD202'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('500  ~ 1000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '500-1000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#F8FF01'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('1000 ~ 2000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '1000-2000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#B0DE09'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('2000 ~ 3000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '3000-3000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#04D215'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('3000 ~ 4000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '3000-4000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#0D8ECF'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('4000 ~ 5000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '4000-5000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#0D52D1'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('5000 ~ 6000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '5000-6000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#2A0CD0'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('6000 ~ 12000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '6000-12000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#8A0CCF'
            convert_column_list.append(converted_dict)
            continue
        
    final_convert_column_list = convert_column_list[1:-1] + [convert_column_list[0]]
    return final_convert_column_list
