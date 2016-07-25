# -*- coding: UTF-8 -*-
import json
import logging
import string

from django.http.response import HttpResponse
from django.shortcuts import render

from loadtest.froms import VexLoadTestInsertionForm
from loadtest.models import LoadTestResult, get_test_type_json_list


logger = logging.getLogger(__name__)

def about(request):
    return render(request, 'loadtest/about.html')

# 展示最新的压力测试结果
def show_latest(request):
    # List = [{'color': '#FF0F00', 'Client': '7217', 'ResponseTime': '0-20'}, {'color': '#FF6600', 'Client': '288474', 'ResponseTime': '20-50'}, ];
    lastest_load_test_result = LoadTestResult.objects.latest(field_name='test_date');
    index_result = _get_armcharts_column_list(lastest_load_test_result.test_result_index)
    bitrate_result = _get_armcharts_column_list(lastest_load_test_result.test_result_bitrate)
    test_error = lastest_load_test_result.test_result_error
    
    index_benchmark_summary = _get_benchmark_number(lastest_load_test_result.test_result_index, '_index')
    bitrate_benchmark_summary = _get_benchmark_number(lastest_load_test_result.test_result_bitrate, '_bitrate')
    
    context = {'index_results': json.dumps(index_result), 'bitrate_results': json.dumps(bitrate_result), 'test_errors': test_error, 'test_date':lastest_load_test_result.test_date}
    context.update(index_benchmark_summary)
    context.update(bitrate_benchmark_summary)
    
    return render(request, 'loadtest/latestResult.html', context)

# 显示所有的压力测试类型。如果参数中包含测试类型，则显示最近10次的压力测试数据时间
def show_all_load_test_results(request, test_type=None):
    if test_type is not None:
        logger.debug("Show all %s test results", test_type)
    else:
        logger.debug("Show all test results for both linear/vod/cdvr")
    
    load_test_results = LoadTestResult.objects.all()[0:10] if test_type is None else LoadTestResult.objects.filter(test_type=test_type);
    context = {} if test_type is None else {'selected_test_type': test_type}
    context['test_type_list'] = get_test_type_json_list()
    
    if len(load_test_results) > 0:
        latest_load_test_result = load_test_results[0]
        index_results = _get_armcharts_column_list(latest_load_test_result.test_result_index)
        bitrate_results = _get_armcharts_column_list(latest_load_test_result.test_result_bitrate)
        test_errors = load_test_results[0].test_result_error
        
        context.update({'load_test_results':load_test_results,
                        'selected_test_id': latest_load_test_result.id,
                       'index_results': json.dumps(index_results),
                       'bitrate_results': json.dumps(bitrate_results),
                       'test_errors': test_errors,
                       'test_date': latest_load_test_result.test_date})
        
        index_benchmark_summary = _get_benchmark_number(latest_load_test_result.test_result_index, '_index')
        bitrate_benchmark_summary = _get_benchmark_number(latest_load_test_result.test_result_bitrate, '_bitrate')
        context.update(index_benchmark_summary)
        context.update(bitrate_benchmark_summary)
        
    logger.debug("Context is: %s", context)
    return render(request, 'loadtest/testResults.html', context)

# 显示某一次压力测试结果    
def show_one_load_test_result(request, test_type, test_id):
    logger.debug("Show test results for %s[test_id: %s]", test_type, test_id)
    
    load_test_results = LoadTestResult.objects.filter(test_type=test_type);
    load_test_result = load_test_results.get(id=test_id);
    
    context = {}
    context['selected_test_type'] = test_type
    context['selected_test_id'] = test_id
    context['test_type_list'] = get_test_type_json_list()
    
    index_results = _get_armcharts_column_list(load_test_result.test_result_index)
    bitrate_results = _get_armcharts_column_list(load_test_result.test_result_bitrate)
    test_errors = load_test_result.test_result_error
        
    context.update({'load_test_results':load_test_results,
                   'index_results': json.dumps(index_results),
                   'bitrate_results': json.dumps(bitrate_results),
                   'test_errors': test_errors,
                   'test_date': load_test_result.test_date })

    index_benchmark_summary = _get_benchmark_number(load_test_result.test_result_index, '_index')
    bitrate_benchmark_summary = _get_benchmark_number(load_test_result.test_result_bitrate, '_bitrate')
    context.update(index_benchmark_summary)
    context.update(bitrate_benchmark_summary)
    
    return render(request, 'loadtest/testResults.html', context)

# 获取所有的压力测试结果信息
def get_all_load_test_results(request, test_type):
    loadtest_results = LoadTestResult.objects.filter(test_type=test_type);
    results = [ob.as_json() for ob in loadtest_results]
    logger.debug("Load test result for %s is %s", test_type, str(results))
    return HttpResponse(json.dumps(results), content_type="application/json")



# 插入一条压力测试结果(通过form验证)
def insert_test_result_with_form(request):
    if request.method == 'POST':
        
        # 标准的从网页提交的数据会直接被django将数据转换到了requst.POST中，表现为QueryDict. 
        # form = VexLoadTestInsertionForm(request.POST)
        # 我们这里是从request body中post过去的，因此需要转换request.body中的数据到dict，才能使用form的validation
        # 且validation要求UI上的post对象的名称和model中的对象的名称完全一致。因此需要转换index_results和bitrate_results为test_result_index和test_result_bitrate
        data = request.POST if request.POST else _convert_request_body_to_form_validation(request)
        form = VexLoadTestInsertionForm(data)
        errors = {}
        # 验证表单是否正确
        if form.is_valid():
            form.save()
            return HttpResponse("Test result has been saved.")
        else:
            errors.update(form.errors)
            return HttpResponse(json.dumps({"errors": errors}), content_type="application/json")
    else:   
        return HttpResponse("Must be post with body")

# 插入一条压力测试结果(不通过form验证)
def insert_test_result(request):
    if request.method == 'POST':
        logger.debug("insert load test request with body:" + request.body)
        
        received_json_data = json.loads(request.body)
        
        index_results = received_json_data['index_results']
        bitrate_results = received_json_data['bitrate_results'] 
        test_errors = received_json_data['test_errors'] if received_json_data.has_key('test_errors') else ''
        test_date = received_json_data['test_date'] if received_json_data.has_key('test_date') else ''
        logger.debug(index_results, bitrate_results, test_errors, test_date)
        
        # 这里没有验证。如果需要验证，可以采用form验证的方式
        result = LoadTestResult()
        result.test_result_index = index_results
        result.test_result_bitrate = bitrate_results
        result.save()
        return HttpResponse("Test result has been saved.")
    else:   
        return HttpResponse("Must be post with body")

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

def _get_benchmark_number(benchmark_result, tag=''):
    average_response = 0
    benchmark_time = 0
    request_number = 0
    error_number = 0
    
    for line in benchmark_result.split('\n'):
        if string.strip(line) == '':
            continue
        
        m_number = line.split(':')[1].replace('\r', '')
        if line.find('error') > 0:
            error_number = int(m_number)
            continue
        
        if line.find('Average response') > 0:
            average_response = int(m_number)
            continue
        
        if line.find('Total request') > 0:
            request_number = int(m_number)
            continue
        
        if line.find('Total cost') > 0:
            benchmark_time = int(m_number)
            continue
    
    results = {"average_response":0, "benchmark_time":0, "concurrent_session":0, "error_rate":0}
    results["average_response" + tag] = average_response
    results["benchmark_time" + tag] = "{} Hour {} Minutes".format(str(benchmark_time / 3600), str((59 + benchmark_time - 3600 * (benchmark_time / 3600)) / 60))
    results["concurrent_session" + tag] = request_number / benchmark_time
    results["error_rate" + tag] = round((float(error_number) / request_number) * 100, 2)
    print results
    return results

'''<?xml version="1.0"?>
<loadtest_data>
    <index_results>
    Index request report:
      Average response (milliseconds):23
      Total cost time             :5419
      Total request number        :1082677
      Total response error number :0
        0    ~ 20   milliseconds :550512
        20   ~ 50   milliseconds :470302
        50   ~ 200  milliseconds :60111
        200  ~ 500  milliseconds :1447
        500  ~ 1000 milliseconds :114
        1000 ~ 2000 milliseconds :191
        2000 ~ 3000 milliseconds :0
        3000 ~ 4000 milliseconds :0
        4000 ~ 5000 milliseconds :0
        5000 ~ 6000 milliseconds :0
        6000 ~ 12000 milliseconds :0
    </index_results>
    <bitrate_results>
    Bit rate request report:
      Average response (milliseconds):23
      Total cost time             :5419
      Total request number        :1082677
      Total response error number :0
        0    ~ 20   milliseconds :550512
        20   ~ 50   milliseconds :470302
        50   ~ 200  milliseconds :60111
        200  ~ 500  milliseconds :1447
        500  ~ 1000 milliseconds :114
        1000 ~ 2000 milliseconds :191
        2000 ~ 3000 milliseconds :0
        3000 ~ 4000 milliseconds :0
        4000 ~ 5000 milliseconds :0
        5000 ~ 6000 milliseconds :0
        6000 ~ 12000 milliseconds :0
    </bitrate_results>
    <test_type>VOD</test_type>
    <test_version>2.7</test_version>
</loadtest_data>'''
def _convert_request_body_to_form_validation(request):
    logger.debug("insert load test request with body:" + request.body)
    
    import xml.etree.ElementTree as ET
    root = ET.XML(request.body)
    bitrate_results_element = root.find('bitrate_results')
    index_results_element = root.find('index_results')
    test_type_element = root.find('test_type') 
    test_version_element = root.find('test_version')
    
    data = {}
    data['test_type'] = test_type_element.text if test_type_element is not None else ''
    data['test_version'] = test_version_element.text if test_version_element is not None else ''
    data['test_result_index'] = index_results_element.text if index_results_element is not None else ''
    data['test_result_bitrate'] = bitrate_results_element.text if bitrate_results_element is not None else ''
    logger.debug("Converted form data is:" + str(data))
    return data
